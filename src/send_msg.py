import pyautogui as pg
import webbrowser as web
import time
from src.get_data import open_profissional, open_respostas, open_mock
import bs4, requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import subprocess
from pathlib import Path


# Erros/implementações que tem pra fazer/corrigir nesse módulo:
# 1. (FEITO) Ao buscar a imagem search_bar na tela do usuário o tamanho da imagem é levado em consideração
# 2. check_load() acessa web.whatsapp.com e retorna apenas a tela de loading da aplicação e não sabemos se a tela carregou ou não 
# 3. Utilizar o editacódigo para fazer o envio de mensagens
# 4. Tomar cuidade para a conta não ser bloqueada por utilização de chatbot (colocar timers e mimetizar o comportamento de um usuário real) 
# 5. Melhorar a função de enviar mensagens para que ela não dependa de uma imagem


def enable_localhost_execution():
    subprocess.run("xhost + local:", shell = True, executable="/bin/bash")


def exit_webpg():
    try:
        time.sleep(2)
        pg.keyDown('ctrl')
        pg.press('w')
        pg.keyUp('ctrl')
    except RuntimeError:
        print("Exit error")
        return -1


def direct_msg(phone, message):
    web.open("https://web.whatsapp.com/send?phone="+phone+"&text="+message)
    time.sleep(5)
    pg.press("enter")
    
    
def open_page():
    enable_localhost_execution()
    response = web.open("https://web.whatsapp.com")
    if not response:
        raise ConnectionError
    else:
        print("Connection established")    
    return response


def check_load(): # Ainda não funcional
    chrome_options = Options()
    chrome_options.binary_location = "/usr/local/bin/google-chrome"
    service = Service(executable_path="/usr/bin/chromedriver") 
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://web.whatsapp.com")
    try:
        print("Aguardando carregamento do WhatsApp Web...")
        search_box = WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
        )
        print("Carregado! Pode começar a enviar as mensagens.")
    except Exception as e:
        print("Erro ao aguardar carregamento:", e)
    driver.quit()
    
    
def locate_serch_bar():
    try:
        path = Path("./img/").resolve()
        for path in path.iterdir():
            path = str(path)
            search_bar = pg.locateOnScreen(path) 
            if search_bar is not None:
                break
        search_bar_x, search_bar_y = pg.center(search_bar) 
        return search_bar_x, search_bar_y
    except Exception as e:
        print("Error:", e)
        print("Error in locate_serch_bar")
        exit_webpg()
        return -1
    
    
def send_msg(phone, message, search_bar_pos):
    try:
        pg.click(search_bar_pos[0], search_bar_pos[1])
        pg.write(phone) 
        pg.press('enter') 
        time.sleep(1)
        for line in message:
            pg.write(line)
            pg.hotkey('shift', 'enter')
        time.sleep(1)
        pg.press("enter") 
        pg.click(search_bar_pos[0] + 250, search_bar_pos[1])
    except Exception as e:
        print("Error:", e)
        print("Error in send_msg")
        exit_webpg()
        return -1

def send_batch(df):
    response = open_page()
    time.sleep(7)
    pos = locate_serch_bar()
    print(pos)
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
    print("Suceessfully sent all messages")
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
