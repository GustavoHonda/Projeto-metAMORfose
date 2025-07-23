from typing import Any
from src.get_data import open_mock
from src.utils.path import get_project_root
from abc import ABC, abstractmethod
import os
import time
base_path = get_project_root()
os.environ.setdefault("DISPLAY", ":0")


# Whapi imports
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv


# Erros/implementações que tem pra fazer/corrigir nesse módulo:
# 1. (FEITO) Ao buscar a imagem search_bar na tela do usuário o tamanho da imagem é levado em consideração
# 2. (ANALIZAR)check_load() acessa web.whatsapp.com e retorna apenas a tela de loading da aplicação e não sabemos se a tela carregou ou não 
# 3. Acrescenta Selenium para fazer o envio de mensagens
# 4. (FEITO) Tomar cuidade para a conta não ser bloqueada por utilização de chatbot (colocar timers e mimetizar o comportamento de um usuário real) 
# 5. Melhorar a função de enviar mensagens para que ela não dependa de uma imagem



class SendMsg(ABC):

    @abstractmethod
    def send_msg(self, phone, message, search_bar_pos, new_chat_pos)-> None:
        pass

    @abstractmethod
    def send_batch(self, df)-> None:
        pass


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

class Whapi_sender(SendMsg):
    def __init__(self):
        load_dotenv()
        self.whapi_url = os.getenv("WHAPI_URL")
        self.app = Flask(__name__)
        self.session = requests.Session()


    def send_msg(self,phone, message)-> None:
        message = "\n".join(message)
        phone = str(phone).replace(" ", "").replace("", "")
        # print(phone, message)

        url = "https://gate.whapi.cloud/messages/text"
        payload = { "typing_time": 0,
                    "to": phone,
                    "body":  message}
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": "Bearer zNqDoACC4QYwPCIBOjP4Bb7WwA8Jl8h8"
        }
        response = requests.post(url, json=payload, headers=headers)
        print(response.text)


    def send_batch(self,df)-> None:
        print(df.columns)
        df = df.reset_index(drop=True)
        for  index, row in df.iterrows():
            text = text_message(row)
            self.send_msg(row["phone_professional"], text)
            print(f"{index + 1} de {len(df)} mensagens enviadas")
        print("Sent all messages")


    # def send_whapi_request(endpoint, params=None, method='POST'):
    #     """
    #     Send a request to the Whapi.Cloud API.
    #     Handles both JSON and multipart (media) requests.
    #     """
    #     headers = {
    #         'Authorization': f"Bearer {os.getenv('TOKEN')}"
    #     }
    #     url = f"{os.getenv('API_URL')}/{endpoint}"
    #     if params:
    #         if 'media' in params:
    #             # Handle file upload for media messages
    #             details = params.pop('media').split(';')
    #             with open(details[0], 'rb') as file:
    #                 m = MultipartEncoder(fields={**params, 'media': (details[0], file, details[1])})
    #                 headers['Content-Type'] = m.content_type
    #                 response = requests.request(method, url, data=m, headers=headers)
    #         elif method == 'GET':
    #             response = requests.get(url, params=params, headers=headers)
    #         else:
    #             headers['Content-Type'] = 'application/json'
    #             response = requests.request(method, url, json=params, headers=headers)
    #     else:
    #         response = requests.request(method, url, headers=headers)
    #     print('Whapi response:', response.json())  # Debug output
    #     return response.json()


    # def set_hook():
    #     """
    #     Register webhook URL with Whapi.Cloud if BOT_URL is set.
    #     """
    #     if os.getenv('BOT_URL'):
    #         settings = {
    #             'webhooks': [
    #                 {
    #                     'url': os.getenv('BOT_URL'),
    #                     'events': [
    #                         {'type': "messages", 'method': "post"}
    #                     ],
    #                     'mode': "method"
    #                 }
    #             ]
    #         }
    #         send_whapi_request('settings', settings, 'PATCH')

    
    # def set_hook(self):
    #     set_hook()  # Register webhook on startup
    #     port = os.getenv('PORT') 
    #     app.run(port=port, debug=True)


if __name__ == '__main__':
    df = open_mock()
    sender = Whapi_sender()
    sender.send_batch(df)