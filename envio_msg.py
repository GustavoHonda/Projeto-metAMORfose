import pyautogui as pg
import webbrowser as web
import time
import pandas as pd

data = pd.read_csv("contatos.csv", sep=";")



data_dict = data.to_dict('list')

messages = data_dict['WhatsApp']
lead = data_dict['msg']
first = True
web.open("https://web.whatsapp.com/send?phone="+lead+"&text="+message)