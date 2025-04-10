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

# xhost + local:

def exit_webpg():
    time.sleep(2)
    pg.keyDown('ctrl')
    pg.press('w')
    pg.keyUp('ctrl')

def direct_msg(phone, message):
    web.open("https://web.whatsapp.com/send?phone="+phone+"&text="+message)
    time.sleep(5)
    pg.press("enter")
    
def open_page():
    chrome = web.Chrome()
    # response = chrome.open("https://web.whatsapp.com")
    response = web.open("https://web.whatsapp.com")
    if not response:
        raise ConnectionError
    else:
        print("Connection established")    
    
    return response

def check_load():
    chrome_options = Options()
    chrome_options.binary_location = "/usr/local/bin/google-chrome"

    service = Service(executable_path="/usr/bin/chromedriver") 

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://web.whatsapp.com")

    # Espera até que a barra de busca esteja presente (indicando que a interface carregou)
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
    search_bar = pg.locateOnScreen('search_bar.png') #Search in printscreen for search_bar
    search_bar_x, search_bar_y = pg.center(search_bar) #Get coordinates
    pg.click(search_bar_x, search_bar_y)
    pg.write(phone) #Search phone number
    pg.press('enter') #Select first match
    time.sleep(1)
    pg.write(message) #Write message
    pg.press("enter") #Send
    pg.click(search_bar_x + 250, search_bar_y) #Erase phone number from searchbar


if __name__ == '__main__':
    df_respostas = open_respostas()
    df_profissional = open_profissional()
    
    phone = "11950440023"
    message = "Hello pyautogui!"
    response = open_page()
    status = check_load()
    # time.sleep(10)
    # send_msg(phone, message)
    # time.sleep(3)
    # exit_webpg()