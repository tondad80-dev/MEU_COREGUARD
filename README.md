# MEU_COREGUARD (Node v1)

MEU_COREGUARD je experimentální implementace hardwarově akcelerovaného hybridního spínaného řídicího systému. Projekt slouží jako výzkumný prototyp pro verifikaci stability nelineárních systémů v reálném čase.

## Technická specifikace
Jádro systému je postaveno na virtuálním stroji (SCIR-VM v1) s integrovanou dohledovou vrstvou (Supervisor), která zajišťuje bezpečnostní bariéry v souladu s metodikou Ljapunovovy stability.

* **Architektura:** Switched LQR Coprocessor
* **Bezpečnostní limity:**
    * W_max: 60 (Saturační mez)
    * W_min: 5 (Havarijní práh)
    * tau_d: 6 taktů (Zeno Inhibition)

## Struktura projektu
- `test_coreguard_vm.py`: Hlavní verifikační model (Golden Model).
- `COREGUARD_VISUAL_DEMO.html`: Interaktivní inženýrský demonstrátor pro vizuální validaci.
- `test_stress_validation.py`: Protokol zátěžových testů (Fuzzing, Zeno-Storm).

## Verifikace
Systém je plně validován pomocí rámce `pytest`. Pro spuštění kompletní sady testů:
```bash
pytest -s