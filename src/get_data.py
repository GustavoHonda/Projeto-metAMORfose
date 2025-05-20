import pandas as pd
import json
import requests
import re
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from src.utils.path import get_project_root
from pathlib import Path

base_path = get_project_root()

# Erros/implementações que tem pra fazer/corrigir nesse módulo:
# 1.coluna price de df_respostas tem descrição (str) dos preços solicitados, precisa transformar para (int)
# 2.extrair mais informações da descrição das respostas de cada paciente(implementação complicada)
# 3. Acrescentar type columns para cada coluna do cliente

def data_info(df, column):
    """
    Função auxiliar que mostra os valores únicos, tipo e frequência de uma coluna do DataFrame.

    Args:
        df (pd.DataFrame): DataFrame analisado
        column (str): Nome da coluna analisada
    """
    print(f"Coluna: {column}")
    print(f"Tipo de dado: {df[column].dtype}\n")
    print("Frequência de valores únicos:")
    print(df[column].value_counts())  # inclui NaNs se houver


def extrair_precos(texto):
    # Remove separador de milhar
    texto = re.sub(r'\.(?=\d{3}(?:,|$))', '', str(texto))
    # Troca vírgula decimal por ponto
    texto = re.sub(r'(?<=\d),(?=\d)', '.', texto)
    # Substitui tudo que não é número ou ponto por espaço
    texto = re.sub(r'[^0-9.]', ' ', texto)
    # Remove espaços duplicados
    texto = re.sub(r'\s+', ' ', texto).strip()
    # Quebra em possíveis preços
    precos = texto.split(' ')
    # Converte os valores válidos para float
    return [float(p) for p in precos if p.replace('.', '', 1).isdigit()]

    

def preprocess_respostas(df):
    df['freq_client'] = '0'
    name_columns= ['id','time','name_paciente','e-mail','phone_paciente','area','description','max_price','price','phone2','urgencie','free_service','sexual_identity','professional','whatsapp','freq_client']
    df.columns = name_columns
    type_columns=[str,str,str,int,str,str,int,int,int,str,str,str,str,str,int]
    df = df.dropna(axis=1, how='all')

    # area column
    df.loc[:,"area"] = df["area"].str.split(",")
    df = df.explode('area')
    df.loc[:,'area'] = df['area'].str.replace(":","", regex=True)
    df.loc[:,'area'] = df['area'].str.strip()

    # Datetime column
    df.loc[:,'datetime'] = pd.to_datetime(df['time'], dayfirst=True)
    df[['date','time']] = df['time'].str.split(" ", expand= True )
    
    # df["datetime"] = df["datetime"].dt.strftime(f'%Y-%m-%d %H:%M:%S')
    
    # Price Column
    df['price'] = df['price'].apply(extrair_precos)
    df["price"] = df["price"].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else 0)
    
    return df


def preprocess_professional(df) -> pd.DataFrame:
    # Adding new data
    df['freq_professional'] = '0'
    
    # Rename columns
    name_columns = ['id','name_professional','area','CRN','phone_professional','price','gender','freq_professional']
    df.columns = name_columns
    
    #area column
    df.loc[:,"area"] = df["area"].str.split(",")
    df = df.explode('area')
    df.loc[:,'area'] = df['area'].str.replace(":","", regex=True)
    df.loc[:,'area'] = df['area'].str.strip()
    
    # Remove unwanted data
    df = df.dropna(axis=1,how='all')
    df = df.dropna(axis=0,how='any')
    df.loc[:,'phone_professional'] = df['phone_professional'].apply(lambda x: x.replace("wa.me/","") if type(x) == str else x)
    df.loc[:,'price'] = df['price'].apply(lambda x: x.replace("+","") if type(x) == str else x )
    
    # Setting correct types
    type_columns = [int,str,str,str,int,int,object,str,int]
    for i,coluna in enumerate(df.columns):
        df.loc[:,coluna] = df[coluna].astype(str).astype(type_columns[i])
    return df


def open_respostas():
    # sheets_respostas = data['url_respostas']
    # df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheets_respostas}/export?format=csv")
    client = set_credentials()
    df = get_data(sheets_name="Respostas",page="Respostas", client=client)
    df = preprocess_respostas(df)
    return df


def open_professional():
    # sheets_professional = data['url_profissionais']
    # df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheets_professional}/export?format=csv")
    client = set_credentials()
    df = get_data(sheets_name="Profissionais",page="Página1", client=client)
    df = preprocess_professional(df)
    return df


def open_matches():
    try:
        client = set_credentials()
        df = get_data(sheets_name="db-metAMORfose", page="Matches", client=client)
        if df is None or df.empty:
            return pd.DataFrame(columns=["name_paciente", "name_professional", "area", "price", "datetime"])
        return df
    except Exception as e:
        print(f"Error: {e}")
        print(f"Error in open_matchings function.")
        return pd.DataFrame()
    
    
def save_matches(df):
    df = df.fillna('')
    client = set_credentials()
    sheet = client.open("db-metAMORfose")
    sheet = sheet.worksheet("Matches")
    # data = [df.columns.tolist()] + df.values.tolist()
    data = df.values.tolist()
    sheet.append_rows(data, value_input_option="USER_ENTERED")
    print("Data saved successfully!")


def open_mock():
    mock_path = Path(base_path, "csv", "mock_match.csv")
    df = pd.read_csv(mock_path, sep=",",encoding="utf-8",index_col=0)
    df.reset_index(inplace=True)
    return df


def open_mock_professional():
    mock_path = Path(base_path, "csv", "mock_professionais.csv")
    df = pd.read_csv(mock_path, sep=",",encoding="utf-8",index_col=0)
    df.reset_index(inplace=True)
    df = preprocess_professional(df)
    return df


def open_mock_respostas():
    mock_path = Path(base_path, "csv", "mock_respostas.csv")
    df = pd.read_csv(mock_path, sep=",",encoding="utf-8",index_col=0)
    df.reset_index(inplace=True)
    df = preprocess_respostas(df)
    return df


def set_credentials():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    
    credentials_path = Path(base_path, "key", "sheets-service-account.json")
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    client = gspread.authorize(creds)
    return client


def send_data(sheets_name="db-metAMORfose", page = None,df=None):
    client = set_credentials()
    sheet = client.open(sheets_name)
    sheet = sheet.worksheet(page)
    data = [df.columns.tolist()] + df.values.tolist()
    sheet.update("A1", data)  
    
    
def get_data(sheets_name = "db-metAMORfose", page = None,client=None):
    sheet = client.open(sheets_name)
    sheet = sheet.worksheet(page)
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    return df


def main():
    df_resposta = open_respostas()
    df_professional = open_professional()
    # print(df_resposta)
    # print(df_professional)
    # send_data(sheets_name="db-metAMORfose",df=df_resposta,page="Respostas")
    # send_data(sheets_name="db-metAMORfose",df=df_professional,page="Profissionais")


if __name__ == "__main__":
    main()