import pyautogui as pg
import webbrowser as web
import time
from get_data import open_profissional, open_respostas
import bs4, requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import subprocess

# Erros/implementações que tem pra fazer/corrigir nesse módulo:
# 1.Ao buscar a imagem search_bar na tela do usuário o tamanho da imagem é levado em consideração
# 2.check_load() acessa web.whatsapp.com e retorna apenas a tela de loading da aplicação e não sabemos se a tela carregou ou não 


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
    
def send_msg(phone, message):
    search_bar = pg.locateOnScreen('search_bar.png') 
    search_bar_x, search_bar_y = pg.center(search_bar) 
    pg.click(search_bar_x, search_bar_y)
    pg.write(phone) 
    pg.press('enter') 
    time.sleep(1)
    pg.write(message) 
    pg.press("enter") 
    pg.click(search_bar_x + 250, search_bar_y) 


if __name__ == '__main__':
    df_respostas = open_respostas()
    df_profissional = open_profissional()
    
    phone = "1150440023"
    message = "bhjkbbkjlkl"
    response = open_page()
    # status = check_load()
    time.sleep(7)
    send_msg(phone, message)
    time.sleep(3)
    # exit_webpg()
    
    