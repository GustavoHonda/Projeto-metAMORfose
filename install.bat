@echo off
echo Detectando sistema operacional...

REM Só roda no Windows mesmo, então não precisa verificar SO

setlocal enabledelayedexpansion

REM Define o diretório do projeto atual
set "PROJECT_DIR=%cd%"

REM Verifica se o venv já existe
if exist "venv\Scripts\activate.bat" (
    echo ? venv já existe (Windows)
) else (
    echo ? venv não encontrado (Windows). Criando...
    py -3.12 -m venv venv
)

REM Baixar instalador do Python 3.12 (se necessário)
if not exist python-3.12.10-amd64.exe (
    echo Baixando Python 3.12...
    curl --ssl-no-revoke -o python-3.12.10-amd64.exe https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe
    echo Instalando Python 3.12...
    python-3.12.10-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
)

REM Verifica versão do Python
py -3.12 --version

REM Ativa venv e instala dependências
call venv\Scripts\activate.bat
pip install -r requirements.txt

REM Rodar pyinstaller
setlocal enabledelayedexpansion
set "PYTHONPATH=!PYTHONPATH!;%cd%\src"
pyinstaller --onefile --icon=img/logo.png --paths=src --log-level=INFO main.py

REM Criar atalho na área de trabalho usando VBS
echo ?? Criando atalho no Windows...

set "SHORTCUT=%USERPROFILE%\Desktop\MetAMORfose.lnk"
set "TARGET=%PROJECT_DIR%\dist\main.exe"
set "WORKDIR=%PROJECT_DIR%"

echo Set oWS = WScript.CreateObject("WScript.Shell") > create_shortcut.vbs
echo sLinkFile = "%SHORTCUT%" >> create_shortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> create_shortcut.vbs
echo oLink.TargetPath = "%TARGET%" >> create_shortcut.vbs
echo oLink.WorkingDirectory = "%WORKDIR%" >> create_shortcut.vbs
echo oLink.Save >> create_shortcut.vbs

cscript //nologo create_shortcut.vbs

del create_shortcut.vbs

echo ? Instalação concluída! Atalho criado na área de trabalho.
echo Qualquer dúvida entrar em contato com: gustavo.honda10@gmail.com

endlocal
