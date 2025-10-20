#!/bin/bash

echo "Detectando sistema operacional..."

if [[ "$OSTYPE" == "linux-gnu"* ]]; then

    echo "Linux detectado"
    PROJECT_DIR="$(pwd)"

    # Verifica Python 3.12
    if ! command -v python3.12 &> /dev/null; then
        echo "❌ Python 3.12 não encontrado. Instale usando seu gerenciador de pacotes ou pyenv."
        exit 1
    else
        python3.12 --version
    fi
    
    cd "$PROJECT_DIR" || exit 1

    if [[ -f "venv/bin/activate" ]]; then
        echo "✅ venv já existe (Linux/macOS)"
    else
        python3.12 -m venv venv

        echo "pip está localizado em: $(which pip)"
        sleep 2
        echo "Instalando dependências..."
        pip install -r requirements.txt
    fi

    source venv/bin/activate
    # pyinstaller --onefile --name=production --icon=img/logo.png main.py
    echo "✅ Instalação concluída! Atalho criado na área de trabalho."
    echo "Qualquer dúvida entrar em contato com gustavo.honda10@gmail.com"

else
    echo "⚠️ Este script é para Linux."
    exit 1
fi
