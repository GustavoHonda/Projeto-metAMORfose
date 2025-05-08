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

# com logo fica

pyinstaller --onefile --icon=img/logo.png  main.py 

```


teste2

# adicionar no pacote 

git add README.md

# salvar na maquina a versao do pacote

 git commit -m "Edited README.md"

# 

 git status 

# download 

 git clone

 # caminho do arquivo


 git add README.md

 # O pacote deve estar salvo para enviar 
 git commit -m "Atualiza README.md"

 # enviar pacote na internet no grupo

 git push 

 # 

 git pull 

python src/exercicio2.py

# python src/exercicio2.py

# python -m src.matching

# pytest : Verifica todos os testes que estao passando
