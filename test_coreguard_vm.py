#!/usr/bin/env python3
import pytest

class ScirVmEmulator:
    def __init__(self):
        self.MODE_NOMINAL = 0
        self.MODE_POLICY = 1
        self.MODE_DEADLOCK = 2
        self.MIN_DWELL_TIME = 6
        self.W_NOM = 15
        self.W_MAX = 60
        self.W_MIN = 5
        self.reset()

    def reset(self):
        self.vm_phase = "FETCH"
        self.dwell_counter = self.MIN_DWELL_TIME
        self.active_mode = self.MODE_NOMINAL
        self.target_mode = self.MODE_NOMINAL
        self.shadow_e = 0
        self.shadow_dw = 0
        self.fetched_opcode = 0
        self.computed_w = self.W_NOM
        self.trap_active = False
        self.supervisor_status = 0x0
        self.comp_guard_val = 0
        self.comp_clf_energy = 0
        self.comp_control_u = 0
        self.lmi_residual = 0

    def step_pipeline(self, bytecode, i_error, i_dw, i_fault_code):
        if self.dwell_counter < 255:
            self.dwell_counter += 1

        self.vm_phase = "FETCH"
        self.shadow_e = i_error
        self.shadow_dw = i_dw
        self.fetched_opcode = (bytecode >> 24) & 0xFF
        self.target_mode = i_fault_code

        self.vm_phase = "EXECUTE"
        if self.fetched_opcode == 0x12:
            pass
        elif self.fetched_opcode == 0x34:
            mat_H11 = (bytecode >> 16) & 0xFF
            mat_H12 = (bytecode >> 8) & 0xFF
            if mat_H11 >= 128: mat_H11 -= 256
            if mat_H12 >= 128: mat_H12 -= 256
            self.comp_guard_val = (self.shadow_e * mat_H11) + (self.shadow_dw * mat_H12)
        elif self.fetched_opcode == 0x56:
            mat_P11 = (bytecode >> 16) & 0xFF
            mat_P22 = (bytecode >> 8) & 0xFF
            self.comp_clf_energy = (self.shadow_e * self.shadow_e * mat_P11) + (self.shadow_dw * self.shadow_dw * mat_P22)
            self.lmi_residual = self.comp_clf_energy - 0xFFFF
        elif self.fetched_opcode == 0x78:
            gain_k1 = (bytecode >> 12) & 0xFFF
            gain_k2 = bytecode & 0xFFF
            if gain_k1 >= 2048: gain_k1 -= 4096
            if gain_k2 >= 2048: gain_k2 -= 4096
            self.comp_control_u = -(gain_k1 * self.shadow_e + gain_k2 * self.shadow_dw)

        self.vm_phase = "COMMIT"
        if self.trap_active:
            self.computed_w = 4
            return

        if self.fetched_opcode == 0x12:
            mapped_mode = self.MODE_NOMINAL
            if self.target_mode == 0x2: mapped_mode = self.MODE_POLICY
            if self.target_mode == 0x4: mapped_mode = self.MODE_DEADLOCK

            if mapped_mode != self.active_mode:
                if self.target_mode == 0x4 or self.dwell_counter >= self.MIN_DWELL_TIME:
                    self.active_mode = mapped_mode
                    self.dwell_counter = 0
                else:
                    self.trap_active = True
                    self.supervisor_status = 0xC

        elif self.fetched_opcode == 0x34:
            vec_b1 = bytecode & 0xFF
            if self.comp_guard_val > (vec_b1 << 8):
                self.trap_active = True
                self.supervisor_status = 0xA

        elif self.fetched_opcode == 0x56:
            if self.lmi_residual > 0:
                self.trap_active = True
                self.supervisor_status = 0xB

        elif self.fetched_opcode == 0x78:
            delta_w = self.comp_control_u >> 8
            self.computed_w += delta_w
            if self.computed_w > self.W_MAX: self.computed_w = self.W_MAX
            if self.computed_w < self.W_MIN: self.computed_w = self.W_MIN

def test_tc_nom_01_nominal_lqr():
    vm = ScirVmEmulator()
    bytecode = (0x78 << 24) | (2 << 12) | 1
    vm.step_pipeline(bytecode, i_error=10, i_dw=0, i_fault_code=0x0)
    assert vm.trap_active is False
    assert vm.supervisor_status == 0x0
    assert vm.computed_w < 15

def test_tc_hyst_02_hysteresis_gate():
    vm = ScirVmEmulator()
    bytecode_switch = (0x12 << 24)
    vm.step_pipeline(bytecode_switch, i_error=45, i_dw=0, i_fault_code=0x2)
    assert vm.active_mode == vm.MODE_POLICY
    assert vm.trap_active is False
    vm.dwell_counter = 2 
    vm.step_pipeline(bytecode_switch, i_error=35, i_dw=0, i_fault_code=0x0)
    assert vm.trap_active is True
    assert vm.supervisor_status == 0xC

def test_tc_inter_03_deadlock_dominance():
    vm = ScirVmEmulator()
    bytecode_switch = (0x12 << 24)
    vm.step_pipeline(bytecode_switch, i_error=0, i_dw=0, i_fault_code=0x4)
    assert vm.active_mode == vm.MODE_DEADLOCK
    assert vm.trap_active is False

def test_tc_trap_04_lmi_divergence():
    vm = ScirVmEmulator()
    bytecode_assert = (0x56 << 24) | (5 << 16) | (5 << 8)
    vm.step_pipeline(bytecode_assert, i_error=120, i_dw=50, i_fault_code=0x0)
    assert vm.trap_active is True
    assert vm.supervisor_status == 0xB
    bytecode_gain = (0x78 << 24) | (2 << 12) | 1
    vm.step_pipeline(bytecode_gain, i_error=10, i_dw=0, i_fault_code=0x0)
    assert vm.computed_w == 4
