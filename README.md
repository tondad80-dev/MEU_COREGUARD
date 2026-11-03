# MEU_COREGUARD (Node v1)

MEU_COREGUARD is an experimental software model of a hybrid switched control system. The repository contains a Python SCIR-VM emulator, internal functional tests and an interactive demonstrator.

## Technical Specification
The model represents a bytecode-driven virtual machine (SCIR-VM v1) with supervisory checks inspired by Lyapunov stability methodology. These checks describe emulator behavior; they do not establish hardware acceleration, real-time guarantees or physical-system safety.

* **Modeled architecture:** Switched LQR controller
* **Model parameters:**
    * W_max: 60 (Saturation limit)
    * W_min: 5 (Emergency threshold)
    * tau_d: 6 emulator steps (minimum dwell counter)

## Project Structure
- `test_coreguard_vm.py`: Core verification model (Golden Model).
- `COREGUARD_VISUAL_DEMO.html`: Interactive engineering demonstrator.
- `test_stress_validation.py`: Software stress tests (Fuzzing, Zeno-Storm).
- `test_coreguard_v4_hil.py`: Software jitter simulation; despite the filename, it does not connect to physical hardware.
- `REPORT_TEST_RESULTS.txt`: Historical internal functional-test summary, not a safety certification.

## Verification
The `pytest` suite checks selected behaviors of the software model. The host-timing assertion in `test_coreguard_v3.py` is not a worst-case execution-time guarantee. These tests do not establish hardware-in-the-loop validation or safety for a deployed physical controller.

To run the test suite in an environment with `pytest` installed:

```bash
pytest -s
```
