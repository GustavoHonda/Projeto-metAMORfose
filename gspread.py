import gspread
from google.oauth2 import service_account
import pandas as pd

scopes = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]
json_file = "../key/sheets_key.json"


def login():
    credentials = service_account.Credentials.from_service_account_file(json_file)
    scoped_credentials = credentials.with_scopes(scopes)
    gc = gspread.authorize(scoped_credentials)
    return gc

def leitor(aba):
    gc = login()
    planilha = gc.open('Espelho Gestão Centralizada')
    aba = planilha.worksheet("Professional")
    dados = aba.get_all_records()
    df = pd.DataFrame(dados)
    return df

def escritor(lista):
    gc = login()
    planilha = gc.open('Espelho Gestão Centralizada')
    planilha = planilha.worksheet('Professional')
    planilha.append_row(lista, value_input_option='USER_ENTERED')


login()
leitor("respostas")
