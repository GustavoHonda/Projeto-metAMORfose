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

### Abilitar copy paste do Pyperclip
```bash
sudo apt update
sudo apt install xclip
```

### Execução pela linha de comando no Windows com ambiente já instalado
```bash
cd C:\Users\DLG\Documents\v1.0\Projeto-metAMORfose-main
venv\Scripts\activate
python main.py
```

### Antes de rodar o programa certifique-se de que:
1. Tenha conexão com a internet.
2. A sua conta do whatsapp web esteja conectada.
3. Não Mexer o mouse durante a execução do código.
4. Ter certeza que os contatos dos profissionais estão adicionados no whatsapp logado no Whatsapp web.
5. Mantenha a janela do navegador com whatsapp vizível.
6. Ter certeza que o caps lock não está ativo.
7. Tomar cuidado com utilização de mais de um monitor.
