import os
import subprocess
from datetime import datetime

def run_tests_and_log():
    test_dir = "./tests"
    log_file = "log.md"

    with open(log_file, "w") as log:
        log.write(f"# Log de Testes\n")
        log.write(f"Data e Hora: {datetime.now()}\n\n")

        for filename in os.listdir(test_dir):
            if filename.endswith(".py"):
                filepath = os.path.join(test_dir, filename)
                log.write(f"## Executando {filename}\n\n")
                log.write("```\n")

                result = subprocess.run(["python", filepath], capture_output=True, text=True)
                log.write(result.stdout)
                log.write(result.stderr)

                log.write("```\n\n")

if __name__ == "__main__":
    run_tests_and_log()
