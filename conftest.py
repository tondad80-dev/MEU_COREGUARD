import os

def pytest_sessionfinish(session, exitstatus):
    # Spustí se input() pouze pokud NEJSME v cloudu (GitHub automaticky nastavuje proměnnou CI=true)
    if not os.getenv("CI"):
        try:
            input("\nTesty dokončeny. Stiskněte Enter pro zavření okna...")
        except EOFError:
            pass