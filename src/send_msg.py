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
    
    
def open_page()->web:
    enable_localhost_execution()
    urls = ["https://web.whatsapp.com"]

    browsers = [web, "/usr/bin/google-chrome", r"C:\Program Files (x86)\Mozilla Firefox\firefox"]
    response = None

    for browser in browsers:
        if browser == web:
            response = web.open(urls[0]) 
        else:
            response = web.get(browser).open(urls[0])

        if response:
            print("Connection established")
            break

    if not response:
        raise ConnectionError("Não consegui acessar a página.")    

    return response


def locate_img(path)-> tuple:
    try:
        screenshot = pg.screenshot()
        screenshot.save("print_debug.png")
        search_bar = pg.locateOnScreen(path, confidence=0.8) 
        return search_bar
    except Exception as e:
        print(f"Exception: in locating {path}")
        return None


def locate_search_bar():
    path_img = Path(base_path, "img","search_bar")
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


def locate_new_chat():
    path_img = Path(base_path, "img", "new_chat")
    for path in path_img.iterdir():
        path = str(path)
        new_chat = locate_img(path)
        if new_chat is not None:
            break
    if new_chat is None:
        print("Error: new chat not found")
        exit_webpg()
        return -1
    search_bar_x, search_bar_y = pg.center(new_chat) 
    print(search_bar_x, search_bar_y)
    return search_bar_x, search_bar_y
    
   
def human_write(texto):
    def precisa_clipboard(char):
        return char in 'áàâãäéèêëíìîïóòôõöúùûüÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜç👤📞💰📋'
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
        
    
def send_msg(phone, message, search_bar_pos,new_chat_pos):
    time.sleep(5) 
    pg.click(new_chat_pos[0], new_chat_pos[1])
    # time.sleep(2) 
    # pg.click(search_bar_pos[0], search_bar_pos[1])
    pg.write(str(phone))
    time.sleep(5)
    pg.press('enter')
    time.sleep(7)
    for line in message:
        human_write(line)
        pg.hotkey('shift', 'enter')
    time.sleep(5)
    pg.press("enter")


def send_batch(df):
    response = open_page(),
    time.sleep(60)
    pos_search_bar = locate_search_bar()
    pos_new_chat = locate_new_chat()
    print(df.columns)
    for index, row in df.iterrows():
        text = text_message(row)
        send_msg(row["phone_professional"], text, pos_search_bar, pos_new_chat)
        print(f"{index + 1} de {len(df)} mensagens enviadas")
    print("Sent all messages")
    exit_webpg()


def text_message(row):
    name_paciente, name_professional, area,phone,description,price_min,price_max = row["name_paciente"], row["name_professional"],row["area"], row["phone_paciente"], row["description"], row["price_min"],row["price_max"]
    print(name_paciente,area,name_professional,phone,description,price_min,price_max)
    text = (
            f"Olá {name_professional}, tudo bem? Sou a MetAMORfose!",
            f"Você foi conectado com um paciente da área de {area}:",
            f"",
            f"👤Nome: {name_paciente}",
            f"📞Contato: wa.me/{phone}",
            f"📋Descrição: {description}",
            f"💰Valor proposto pelo paciente: R${price_min} à R${price_max}",
            f"",
            f"Obrigada! Até a próxima!",)
    return text


if __name__ == '__main__':
    df = open_mock()
    send_batch(df)