import sys

def pytest_sessionfinish(session, exitstatus):
    # Spustí se input() pouze v případě, že je připojen interaktivní terminál (TTY)
    if sys.stdout.isatty():
        try:
            input("\nTesty dokončeny. Stiskněte Enter pro zavření okna...")
        except EOFError:
            pass