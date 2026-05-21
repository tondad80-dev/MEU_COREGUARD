# MEU_COREGUARD (Node v1)

MEU_COREGUARD is an experimental implementation of a hardware-accelerated hybrid switched control system. The project serves as a research prototype for real-time stability verification of non-linear systems.

## Technical Specification
The system core is built on a bytecode-driven virtual machine (SCIR-VM v1) with an integrated supervisory layer (Supervisor) that ensures safety barriers in compliance with Lyapunov stability methodology.

* **Architecture:** Switched LQR Coprocessor
* **Safety Envelopes:**
    * W_max: 60 (Saturation limit)
    * W_min: 5 (Emergency threshold)
    * tau_d: 6 clock cycles (Zeno Inhibition)

## Project Structure
- `test_coreguard_vm.py`: Core verification model (Golden Model).
- `COREGUARD_VISUAL_DEMO.html`: Interactive engineering demonstrator for visual validation.
- `test_stress_validation.py`: Stress testing protocol (Fuzzing, Zeno-Storm).

## Verification
The system is fully validated using the `pytest` framework. To execute the complete test suite, run:
```bash
pytest -s