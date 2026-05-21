#!/usr/bin/env python3
import pytest
from test_coreguard_vm import ScirVmEmulator

def test_visual_demo_deterministic_sequence():
    vm = ScirVmEmulator()
    bytecode_switch = (0x12 << 24)
    vm.step_pipeline(bytecode_switch, i_error=45, i_dw=0, i_fault_code=0x2)
    assert vm.active_mode == vm.MODE_POLICY
    for _ in range(3):
        vm.step_pipeline(bytecode_switch, i_error=30, i_dw=0, i_fault_code=0x2)
    vm.step_pipeline(bytecode_switch, i_error=10, i_dw=0, i_fault_code=0x0)
    assert vm.trap_active is True
    assert vm.supervisor_status == 0xC
    vm.step_pipeline(bytecode_switch, i_error=0, i_dw=0, i_fault_code=0x0)
    assert vm.computed_w == 4
