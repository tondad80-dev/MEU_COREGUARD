#!/usr/bin/env python3
import pytest
from test_coreguard_vm import ScirVmEmulator

def test_lmi_boundary_fuzzing():
    vm = ScirVmEmulator()
    for e in range(-100, 100, 20):
        for dw in range(-100, 100, 20):
            vm.reset()
            bytecode_assert = (0x56 << 24) | (1 << 16) | (1 << 8)
            vm.step_pipeline(bytecode_assert, i_error=e, i_dw=dw, i_fault_code=0)
            if vm.lmi_residual > 0:
                assert vm.trap_active is True
