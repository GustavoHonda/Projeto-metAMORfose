### Instalação no windows

1. Abrir o prompt de comando como admin

2. Baixar versão do python 3.12.10:

curl --ssl-no-revoke -o python-3.12.10-amd64.exe https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe

python-3.12.10-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

py -3.12 --version

3. Criar o ambiente virtual:

cd ambiente\do\projeto
py -3.12 -m venv venv
venv\Scripts\activate

obs: não esquecer de fazer o download das chaves privadas do google drive

4. instalar requirements

pip install -r requirements.txt

5. executar pyinstaller

pyinstaller --onefile main.py

6. testar execução

dist\main.exe

### Execução

1. Garante que sua conta comercial esteja logada no whatsappweb

2. Execute primeiramente o arquivo de teste para se certificar que
o whatsapp não mudou nada que altere o funcionamento correto do código

3. Qualquer dúvida entrar em contato com: gustavo.honda10@gmail.com

# if __name__=="__main__":
#     """Entry point for the script.
#     """
#     try:
#         BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
#         os.chdir(BASE_DIR)
#         main()
#     except Exception as e:
#         with open("erro.log", "w", encoding="utf-8") as f:
#             traceback.print_exc(file=f)
#         sys.exit(1)