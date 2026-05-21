#!/usr/bin/env python3
import pytest
import time
from test_coreguard_vm import ScirVmEmulator

def test_tc_latency_v3():
    vm = ScirVmEmulator()
    start_time = time.perf_counter_ns()
    vm.step_pipeline(0x12000000, i_error=0, i_dw=0, i_fault_code=0x4)
    end_time = time.perf_counter_ns()
    assert vm.active_mode == vm.MODE_DEADLOCK
    assert (end_time - start_time) < 1000000 # Real-time threshold check
