# Projeto-metAMORfose

### Para criar o ambiente de desenvolvimento
cd /caminho/para/Projeto-metAMORfose/
pytho -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp -r ~/Downloads/key/ /caminho/para/Projeto-metAMORfose/


### Execução dos módulos
cd /caminho/para/Projeto-metAMORfose/
pytho -m src.qualer_um_dos_modulos_dentro_de_src


### Testes
cd /caminho/para/Projeto-metAMORfose/
pytest ./test


### Criação de um executável
cd /caminho/para/Projeto-metAMORfose/
pyinstaller --onefile main.py 

ou também sem linha de comando

pyinstaller --onefile --noconsole main.py 