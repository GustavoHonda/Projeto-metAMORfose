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
import mss
from PIL import Image

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import time
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

base_path = get_project_root()
os.environ.setdefault("DISPLAY", ":0")


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

    def locate_img(self, path: str) -> tuple | None:
        """
        Localiza uma imagem na tela com confiança de 80% usando MSS.
        """
        try:
            # Captura a tela com mss
            with mss.mss() as sct:
                monitor = sct.monitors[1]  # tela inteira
                sct_img = sct.grab(monitor)

            # Converte para uma imagem PIL
            img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)

            # (Opcional) salvar para debug
            img.save("print_debug.png")

            # Usa pyautogui.locate() passando a imagem manualmente
            match = pg.locate(path, img, confidence=0.8)

            return match

        except Exception as e:
            print(f"❌ Exception while locating image '{path}': {e}")
            return None


    def locate_new_chat(self) -> tuple | int:
        """
        Percorre as imagens da pasta 'img/new_chat' e localiza a primeira encontrada na tela.
        """
        try:
            # Salva um screenshot geral para debug
            debug_img_path = Path(base_path) / "img" / "screenshot_debug.png"
            screenshot = pg.screenshot()
            screenshot.save(debug_img_path)

            path_img_dir = Path(base_path) / "img" / "new_chat"
            new_chat = None

            for path in path_img_dir.iterdir():
                if path.is_file():
                    new_chat = self.locate_img(str(path))
                    if new_chat is not None:
                        break

            if new_chat is None:
                print("❌ Error: new chat not found on screen.")
                self.exit_webpg()
                return -1

            x, y = pg.center(new_chat)
            print(f"✅ New chat found at: ({x}, {y})")
            return x, y

        except Exception as e:
            print(f"❌ Unexpected error in locate_new_chat(): {e}")
            return -1
    

    def locate_chat_bar(self) -> tuple | int:
        """
        Percorre as imagens da pasta 'img/chat_bar' e localiza a primeira encontrada na tela.
        """
        try:
            # Salva um screenshot geral para debug
            debug_img_path = Path(base_path) / "img" / "screenshot_debug_chat_bar.png"
            screenshot = pg.screenshot()
            screenshot.save(debug_img_path)

            path_img_dir = Path(base_path) / "img" / "chat_bar"
            new_chat = None

            for path in path_img_dir.iterdir():
                if path.is_file():
                    new_chat = self.locate_img(str(path))
                    if new_chat is not None:
                        break

            if new_chat is None:
                print("❌ Error: new chat not found on screen.")
                self.exit_webpg()
                return -1

            x, y = pg.center(new_chat)
            print(f"✅ New chat found at: ({x}, {y})")
            return x, y

        except Exception as e:
            print(f"❌ Unexpected error in locate_new_chat(): {e}")
            return -1
        
    
    def human_write(self, texto)-> None:
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

    def send_msg(self,phone, message,new_chat_pos)-> None:
        time.sleep(3) 
        pg.click(new_chat_pos[0], new_chat_pos[1])
        pg.click(new_chat_pos[0], new_chat_pos[1])
        pg.click(new_chat_pos[0], new_chat_pos[1])
        time.sleep(3)
        self.human_write(phone)
        time.sleep(10)
        pg.press('enter')
        pg.press('enter')
        time.sleep(3)
        chat_bar_x, chat_bar_y = self.locate_chat_bar()
        pg.click(chat_bar_x, chat_bar_y)
        time.sleep(3)
        for line in message:
            print(line)
            self.human_write(line)
            pg.hotkey('shift', 'enter')
        time.sleep(3)
        pg.press("enter")


    def send_batch(self,df)-> None:
        response = self.open_page(),
        time.sleep(10)
        # pos_search_bar = self.locate_search_bar()
        pos_new_chat = self.locate_new_chat()
        print(df.columns)
        df = df.reset_index(drop=True)
        for  index, row in df.iterrows():
            text = text_message(row)
            self.send_msg(row["phone_professional"], text, pos_new_chat)
            print(f"{index + 1} de {len(df)} mensagens enviadas")
        print("Sent all messages")
        self.exit_webpg()



class Selenium_sender(SendMsg):

    def exit_webpg(self, driver)-> None:
        driver.close()
        

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
        print(df)
        for index, row in df.iterrows():
            text = text_message(row)
            f.write(f"Mensagem {index + 1}:\n")
            f.write(f"{row["phone_professional"]}:\n")
            f.write("\n".join(text) + "\n\n")
        f.close()    


def text_message(row)-> tuple:
    name_paciente, name_professional, area,phone,description,price_min,price_max = row["name_paciente"], row["name_professional"],row["area"], row["phone_paciente"], row["description"], row["price_min"],row["price_max"]
    text = (
            f"Olá {name_professional}, tudo bem? Sou a Inteligência Artificial da MetAMORfose!",
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
    sender = Pyautogui_sender()
    sender.send_batch(df)