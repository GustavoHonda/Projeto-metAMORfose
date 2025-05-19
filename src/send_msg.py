import pyautogui as pg
import webbrowser as web
import time
from src.get_data import open_profissional, open_respostas, open_mock
import subprocess
from pathlib import Path
import platform
from src.utils.path import get_project_root
import sys

base_path = get_project_root()

# Erros/implementações que tem pra fazer/corrigir nesse módulo:
# 1. (FEITO) Ao buscar a imagem search_bar na tela do usuário o tamanho da imagem é levado em consideração
# 2. check_load() acessa web.whatsapp.com e retorna apenas a tela de loading da aplicação e não sabemos se a tela carregou ou não 
# 3. Utilizar o editacódigo para fazer o envio de mensagens
# 4. Tomar cuidade para a conta não ser bloqueada por utilização de chatbot (colocar timers e mimetizar o comportamento de um usuário real) 
# 5. Melhorar a função de enviar mensagens para que ela não dependa de uma imagem


def enable_localhost_execution():
    os_name = platform.system()
    if os_name == "Linux":
        subprocess.run("xhost + local:", shell=True, executable="/bin/bash")
        print("linux")
    elif os_name == "Windows":
        print("windows")
        return 0
    else:
        print("Sistema operacional não suportado")
        return -1


def exit_webpg():
    try:
        time.sleep(2)
        pg.keyDown('ctrl')
        pg.press('w')
        pg.keyUp('ctrl')
    except RuntimeError:
        print("Exit error")
        return -1
    sys.exit(0)


def direct_msg(phone, message):
    web.open("https://web.whatsapp.com/send?phone="+phone+"&text="+message)
    time.sleep(5)
    pg.press("enter")
    
    
def open_page():
    enable_localhost_execution()
    google = "/usr/bin/google-chrome" if platform.system() == "Linux" else "C:/Program Files/Google/Chrome/Application/chrome.exe"
    response = web.get(google).open("https://web.whatsapp.com")
    if not response:
        raise ConnectionError
    else:
        print("Connection established")    
    return response


def locate_img(path):
    try:
        search_bar = pg.locateOnScreen(path, confidence=0.8) 
        return search_bar
    except Exception as e:
        print(f"Exception: in locating {path}")
        return None


def locate_search_bar():
    path_img = Path(base_path, "img")
    for path in path_img.iterdir():
        path = str(path)
        search_bar = locate_img(path)
        if search_bar is not None:
            break
    if search_bar is None:
        print("Error: search_bar not found")
        exit_webpg()
        return -1
    search_bar_x, search_bar_y = pg.center(search_bar) 
    print(search_bar_x, search_bar_y)
    return search_bar_x, search_bar_y
    
    
def send_msg(phone, message, search_bar_pos):
    try:
        time.sleep(1) 
        pg.click(search_bar_pos[0], search_bar_pos[1])
        pg.write(phone)
        pg.press('enter') 
        
        time.sleep(2)
        for line in message:
            pg.write(line)
            pg.hotkey('shift', 'enter')
        
        time.sleep(2)
        pg.press("enter") 
        # pg.click(search_bar_pos[0] + 250, search_bar_pos[1])
    except Exception as e:
        print("Error:", e)
        print("Error in send_msg()")
        exit_webpg()
        return -1


def send_batch(df):
    response = open_page()
    time.sleep(40)
    pos = locate_search_bar()
    try:
        df = df[['name','phone_professional','phone_pacient','description','price']]
        n_total = len(df)
        for index, row in df.iterrows():
            text = text_message(row["name"], row["phone_pacient"], row["description"], row["price"])
            send_msg(row["phone_professional"], text, pos)
            print(f"{index + 1} de {n_total} mensagens enviadas")
    except Exception as e:
        print("Error:", e)
        print("Error in send_batch")
        exit_webpg()
        return -1
    print("Sent all messages")
    exit_webpg()


def text_message(name, phone, description, price):
    text = (f"Segue indicação de paciente:",
            f"Nome: {name}",
            f"Contato: {phone}",
            f"Problemas: {description}",
            f"Valor sugerido: {price}R$")
    return text


if __name__ == '__main__':
    df_respostas = open_respostas()
    df_profissional = open_profissional()
    df = open_mock()
    send_batch(df)
