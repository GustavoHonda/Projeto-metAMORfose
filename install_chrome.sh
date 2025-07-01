#!/bin/bash

set -e

echo "Atualizando repositórios..."
sudo apt update

echo "Instalando dependências necessárias..."
sudo apt install -y wget unzip curl

echo "Baixando o Google Chrome estável..."
wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

echo "Instalando o Google Chrome..."
sudo dpkg -i google-chrome-stable_current_amd64.deb || sudo apt-get install -f -y

echo "Removendo arquivo .deb para limpeza..."
rm google-chrome-stable_current_amd64.deb

echo "Detectando versão do Google Chrome instalado..."
CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+\.\d+')
echo "Versão do Chrome detectada: $CHROME_VERSION"

# Extrair a parte principal da versão (ex: 123.0.6312)
CHROME_VERSION_BASE=$(echo $CHROME_VERSION | grep -oP '^\d+\.\d+\.\d+')

echo "Versão base para chromedriver: $CHROME_VERSION_BASE"

# Construir URL para baixar ChromeDriver compatível
CHROMEDRIVER_BASE_URL="https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing"

echo "Buscando lista de versões disponíveis para download..."

# Pega a lista completa de versões disponíveis
VERSIONS_JSON=$(curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json)

# Extrai a versão de chromedriver mais próxima da versão do chrome instalada
CHROMEDRIVER_VERSION=$(echo "$VERSIONS_JSON" | grep -oP "\"version\":\s*\"$CHROME_VERSION_BASE[^\"]*\"" | head -1 | grep -oP '\d+\.\d+\.\d+\.\d+')

if [ -z "$CHROMEDRIVER_VERSION" ]; then
  echo "Não encontrou versão exata para o chromedriver, usando a versão mais recente disponível..."
  CHROMEDRIVER_VERSION=$(echo "$VERSIONS_JSON" | grep -oP "\"version\":\s*\"\d+\.\d+\.\d+\.\d+\"" | head -1 | grep -oP '\d+\.\d+\.\d+\.\d+')
fi

echo "Versão do chromedriver escolhida: $CHROMEDRIVER_VERSION"

# Montar URL de download
CHROMEDRIVER_URL="$CHROMEDRIVER_BASE_URL/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip"

echo "Baixando chromedriver: $CHROMEDRIVER_URL"
wget -q $CHROMEDRIVER_URL -O chromedriver.zip

echo "Extraindo chromedriver..."
unzip -q chromedriver.zip

echo "Movendo chromedriver para /usr/local/bin..."
sudo mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver
sudo chmod +x /usr/local/bin/chromedriver

echo "Limpando arquivos temporários..."
rm -rf chromedriver-linux64 chromedriver.zip

echo "Instalação concluída!"
echo "Google Chrome versão: $CHROME_VERSION"
echo "ChromeDriver versão: $(chromedriver --version)"
