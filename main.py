from src.pipeline import main

from pathlib import Path
from datetime import datetime
import sys


def get_project_root():
    if getattr(sys, 'frozen', False):
        # Executável gerado por PyInstaller
        exe_path = Path(sys.executable)
        if exe_path.parent.name == "dist":
            return exe_path.parent.parent
        return exe_path.parent
    else:
        # Execução como script Python
        return Path(__file__).resolve().parent

def redirecionar_saida_para_log():
    log_dir = get_project_root() / "logs"
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / f"{datetime.now():%Y-%m-%d_%H-%M-%S}.log"
    err_file = log_dir / f"{datetime.now():%Y-%m-%d_%H-%M-%S}.err"
    log = open(log_file, "w", encoding="utf-8")
    err = open(err_file, "w", encoding="utf-8")
    sys.stderr = err
    sys.stdout = log

    return log, err  # para poder fechar depois, se quiser



if __name__ == "__main__":
    log, err = redirecionar_saida_para_log()

    try:
        main()
    except Exception as e:
        print("Erro:", e)
    finally:
        log.close()
        err.close()
