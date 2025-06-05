import pyautogui as pg
import webbrowser as web
import random
import time
from src.get_data import open_mock
import subprocess
from pathlib import Path
import platform
from src.utils.path import get_project_root
import sys
import pyperclip


base_path = get_project_root()

# Erros/implementações que tem pra fazer/corrigir nesse módulo:
# 1. (FEITO) Ao buscar a imagem search_bar na tela do usuário o tamanho da imagem é levado em consideração
# 2. (ANALIZAR)check_load() acessa web.whatsapp.com e retorna apenas a tela de loading da aplicação e não sabemos se a tela carregou ou não 
# 3. Acrescenta Selenium para fazer o envio de mensagens
# 4. (FEITO) Tomar cuidade para a conta não ser bloqueada por utilização de chatbot (colocar timers e mimetizar o comportamento de um usuário real) 
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
    
    
def open_page():
    enable_localhost_execution()
    google = "/usr/bin/google-chrome" if platform.system() == "Linux" else "C:/Program Files/Google/Chrome/Application/chrome.exe"
    response = web.get(google).open("https://web.whatsapp.com")
    if not response:
        firefox = r"C:\Program Files (x86)\Mozilla Firefox\firefox"
        response = web.get(firefox).open("https://web.whatsapp.com")
    if not response:
        response = web.open("https://web.whatsapp.com")
    if not response:
        raise ConnectionError
    else:
        print("Connection established")    
    return response


def locate_img(path):
    try:
        screenshot = pg.screenshot()
        screenshot.save("print_debug.png")
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
    
   
def human_write(texto):
    def precisa_clipboard(char):
        return char in 'áàâãäéèêëíìîïóòôõöúùûüÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜ👤📞💰📋'
    for char in texto:
        if random.random() < 0.05:  
            erro = random.choice('abcdefghijklmnopqrstuvwxyz')
            pg.write(erro)
            time.sleep(random.uniform(0.05, 0.2))
            pg.press('backspace')

        if precisa_clipboard(char):
            pyperclip.copy(char)
            pg.hotkey('ctrl', 'v')
        else:
            pg.write(char)
        time.sleep(random.uniform(0.035, 0.009))  
        
    
def send_msg(phone, message, search_bar_pos):
    time.sleep(2) 
    pg.click(search_bar_pos[0], search_bar_pos[1])
    pg.write(str(phone))
    time.sleep(3) 
    pg.press('enter') 
    
    time.sleep(5)
    for line in message:
        human_write(line)
        pg.hotkey('shift', 'enter')
    
    time.sleep(5)
    pg.press("enter") 


def send_batch(df):
    response = open_page()
    time.sleep(10)
    pos = locate_search_bar()
    for index, row in df.iterrows():
        text = text_message(row)
        send_msg(row["phone_professional"], text, pos)
        print(f"{index + 1} de {len(df)} mensagens enviadas")
    print("Sent all messages")
    exit_webpg()

def text_message(row):
    name_paciente, name_professional, area,phone,description,price = row["name_paciente"], row["name_professional"],row["area"], row["phone_paciente"], row["description"], row["price"]

    text = (
            f"Olá {name_professional}, tudo bem?",
            f"Você foi conectado com um paciente da área de {area}:",
            f"",
            f"👤Nome: {name_paciente}",
            f"📞Contato: {phone}",
            f"📋Descrição: {description}",
            f"💰Valor proposto: R${price}",
            f"",
            f"Entre em contato caso deseje continuar com o atendimento.",
            f"Obrigado!")
    return text


if __name__ == '__main__':
    df = open_mock()
    send_batch(df)