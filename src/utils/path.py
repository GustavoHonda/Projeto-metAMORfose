import os
import sys
from pathlib import Path

def get_project_root():
    if getattr(sys, 'frozen', False):
        # Executável gerado pelo PyInstaller
        exe_path = Path(sys.executable)
        if exe_path.parent.name == "dist":
            return exe_path.parent.parent  # volta do dist/ para a raiz
        return exe_path.parent
    else:
        # Execução normal do script
        return Path(__file__).resolve().parent.parent.parent

