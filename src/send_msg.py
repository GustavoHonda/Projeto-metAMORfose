from typing import Any
import pyautogui as pg
import webbrowser as web
import random
import time
import subprocess
from pathlib import Path
import platform
from src.get_data import open_mock
from src.utils.path import get_project_root
from abc import ABC, abstractmethod
import sys
import pyperclip
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import time
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

base_path = get_project_root()

# Erros/implementações que tem pra fazer/corrigir nesse módulo:
# 1. (FEITO) Ao buscar a imagem search_bar na tela do usuário o tamanho da imagem é levado em consideração
# 2. (ANALIZAR)check_load() acessa web.whatsapp.com e retorna apenas a tela de loading da aplicação e não sabemos se a tela carregou ou não 
# 3. Acrescenta Selenium para fazer o envio de mensagens
# 4. (FEITO) Tomar cuidade para a conta não ser bloqueada por utilização de chatbot (colocar timers e mimetizar o comportamento de um usuário real) 
# 5. Melhorar a função de enviar mensagens para que ela não dependa de uma imagem


def enable_localhost_execution()-> int:
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

class SendMsg(ABC):
    @abstractmethod
    def open_page(self)-> Any:
        pass

    @abstractmethod
    def send_msg(self, phone, message, search_bar_pos, new_chat_pos)-> None:
        pass

    @abstractmethod
    def send_batch(self, df)-> None:
        pass


class Pyautogui_sender(SendMsg):
    def exit_webpg(self)-> int:
        try:
            time.sleep(2)
            pg.keyDown('ctrl')
            pg.press('w')
            pg.keyUp('ctrl')
        except RuntimeError:
            print("Exit error")
            return -1
        sys.exit(0)
        
        
    def open_page(self)->web:
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


    def locate_img(self,path)-> tuple:
        try:
            screenshot = pg.screenshot()
            screenshot.save("print_debug.png")
            search_bar = pg.locateOnScreen(path, confidence=0.8) 
            return search_bar
        except Exception as e:
            print(f"Exception: in locating {path}")
            return None


    def locate_search_bar(self)-> tuple:
        path_img = Path(base_path, "img","search_bar")
        for path in path_img.iterdir():
            path = str(path)
            search_bar = self.locate_img(path)
            if search_bar is not None:
                break
        if search_bar is None:
            print("Error: search_bar not found")
            self.exit_webpg()
            return -1
        search_bar_x, search_bar_y = pg.center(search_bar) 
        print(search_bar_x, search_bar_y)
        return search_bar_x, search_bar_y


    def locate_new_chat(self)-> tuple:
        path_img = Path(base_path, "img", "new_chat")
        for path in path_img.iterdir():
            path = str(path)
            new_chat = self.locate_img(path)
            if new_chat is not None:
                break
        if new_chat is None:
            print("Error: new chat not found")
            self.exit_webpg()
            return -1
        search_bar_x, search_bar_y = pg.center(new_chat) 
        print(search_bar_x, search_bar_y)
        return search_bar_x, search_bar_y
        
    
    def human_write(texto)-> None:
        def precisa_clipboard(char)-> bool:
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
            
        
    def send_msg(self,phone, message, search_bar_pos,new_chat_pos)-> None:
        time.sleep(5) 
        pg.click(new_chat_pos[0], new_chat_pos[1])
        pg.write(str(phone))
        time.sleep(5)
        pg.press('enter')
        time.sleep(7)
        for line in message:
            self.human_write(line)
            pg.hotkey('shift', 'enter')
        time.sleep(5)
        pg.press("enter")


    def send_batch(self,df)-> None:
        response = self.open_page(),
        time.sleep(60)
        pos_search_bar = self.locate_search_bar()
        pos_new_chat = self.locate_new_chat()
        print(df.columns)
        for index, row in df.iterrows():
            text = text_message(row)
            self.send_msg(row["phone_professional"], text, pos_search_bar, pos_new_chat)
            print(f"{index + 1} de {len(df)} mensagens enviadas")
        print("Sent all messages")
        self.exit_webpg()



class Selenium_sender(SendMsg):
    def open_page(self)-> webdriver:
        try: 
            # (Opcional) executa em modo "headless":
            # chrome_options.add_argument("--headless")
            # driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", options=chrome_options)

            chrome_options = Options()
            chrome_options.binary_location = "/usr/bin/google-chrome" 
            driver = webdriver.Chrome(options=chrome_options)
            # driver.get('https://web.whatsapp.com/')
        except Exception as e:
            print(f"Erro ao abrir a página: {e}")
            return None
        return driver


    def send_msg(self, phone, message, driver)-> None:
        print("send_msg")
        msg = "\n".join(message)
        print(phone)
        phone = phone.replace(" ", "").replace("-", "")
        link = f"https://web.whatsapp.com/send?phone={phone}&text={msg}"
        print(link)
        driver.get(link)
        try:
            print("try")
            caixa_texto = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@contenteditable="true" and @role="textbox"]')
                )
            )
            time.sleep(10)
            botao_enviar = WebDriverWait(driver, 300).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Enviar"]'))
            )
            # caixa_texto.send_keys(message)
            botao_enviar.click()
            print(f"Mensagem enviada para {phone}")

        except Exception as e:
            print(f"Erro ao enviar mensagem para {phone}: {e}")

    def send_batch(self, df)-> None:
        driver = self.open_page()
        print("send_batch")
        for index, row in df.iterrows():
            text = text_message(row)
            self.send_msg(phone=row["phone_professional"], message=text, driver=driver)
            print(f"{index + 1} de {len(df)} mensagens enviadas")
        print("Sent all messages")
        self.exit_webpg()



def write_message(df)-> None:
    print("Printing messages to file...")
    with open("messages.txt", "w") as f:
        for index, row in df.iterrows():
            text = text_message(row)
            f.write(f"Mensagem {index + 1}:\n")
            f.write(f"{row["phone_professional"]}:\n")
            f.write("\n".join(text) + "\n\n")
        f.close()    


def text_message(row)-> tuple:
    name_paciente, name_professional, area,phone,description,price_min,price_max = row["name_paciente"], row["name_professional"],row["area"], row["phone_paciente"], row["description"], row["price_min"],row["price_max"]
    text = (
            f"Olá {name_professional}, tudo bem? Sou a MetAMORfose!",
            f"Você foi conectado com um paciente da área de {area}:",
            f"",
            f"👤Nome: {name_paciente}",
            f"📞Contato: wa.me/{phone}",
            f"📋Descrição: {description}",
            f"💰Valor proposto pelo paciente: R${price_min} à R${price_max}",
            f"",
            f"Obrigada! Até a próxima!")
    return text


if __name__ == '__main__':
    df = open_mock()
    sender = Selenium_sender()
    sender.send_batch(df)