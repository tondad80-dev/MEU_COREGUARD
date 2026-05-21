#!/usr/bin/env python3
import pytest
import random
from test_coreguard_vm import ScirVmEmulator

RANDOM_SEED = 42

def test_stress_zeno_storm_deterministic():
    random.seed(RANDOM_SEED)
    vm = ScirVmEmulator()
    violations = 0
    for _ in range(10000):
        fault = random.choice([0, 2, 4])
        vm.step_pipeline(0x12000000, i_error=random.randint(0, 100), i_dw=0, i_fault_code=fault)
        if vm.trap_active:
            violations += 1
    assert violations >= 10

def test_stress_corrupted_bytecode_fixed():
    random.seed(RANDOM_SEED)
    vm = ScirVmEmulator()
    for i in range(1000):
        vm.reset()
        corrupted_bc = random.randint(0, 0xFFFFFFFF)
        vm.step_pipeline(corrupted_bc, i_error=50, i_dw=50, i_fault_code=0)
        assert 4 <= vm.computed_w <= 60
