#!/usr/bin/env python3
import pytest
import random

class ScirVmEmulatorHIL:
    def __init__(self):
        self.MIN_DWELL_TIME = 6
        self.GUARD_BAND = 0.5
        self.dwell_counter = self.MIN_DWELL_TIME

    def step_hil(self, jitter_factor):
        if (self.dwell_counter + jitter_factor) < (self.MIN_DWELL_TIME - self.GUARD_BAND):
            return "VIOLATION"
        return "STABLE"

def test_hil_jitter_stability():
    vm = ScirVmEmulatorHIL()
    for _ in range(100):
        jitter = random.uniform(-0.4, 0.4)
        status = vm.step_hil(jitter_factor=jitter)
        assert status == "STABLE"
