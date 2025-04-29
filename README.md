# Projeto-metAMORfose

### Para criar o ambiente de desenvolvimento
```bash

cd /caminho/para/Projeto-metAMORfose/ 

pytho -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp -r ~/Downloads/key/ /caminho/para/Projeto-metAMORfose/
```

### Execução dos módulos
```bash
cd /caminho/para/Projeto-metAMORfose/
pytho -m src.qualer_um_dos_modulos_dentro_de_src
```

### Testes
```bash
cd /caminho/para/Projeto-metAMORfose/
pytest ./test
``` 

### Criação de um executável
```bash
cd /caminho/para/Projeto-metAMORfose/
pyinstaller --onefile main.py 

# ou também sem linha de comando

pyinstaller --onefile --noconsole main.py 
```