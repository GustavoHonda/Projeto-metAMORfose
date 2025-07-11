import pandas as pd
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from src.utils.path import get_project_root
from pathlib import Path
from typing import Any

base_path = get_project_root()

# Erros/implementações que tem pra fazer/corrigir nesse módulo:
# 1. (FEITO)coluna price de df_respostas tem descrição (str) dos preços solicitados, precisa transformar para (int).
# 2. (FEITO)extrair mais informações da descrição das respostas de cada paciente(implementação complicada).
# 3. Acrescentar type columns para cada coluna do cliente.
# 4. Trocar id das URL dos google sheets para os de produção.
# 5. Testar sem envio de mensagens pressionando enter.

def data_info(df, column)-> None:
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


def extrair_precos(texto)-> list:
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


def preprocess_respostas(df)->pd.DataFrame:
    
    # Rename columns
    name_columns= ['time','name_paciente','e-mail','phone_paciente','area','description','free_service','price']
    columns = list(df.columns)
    for i, col in enumerate(name_columns):
        columns[i] = col
    df.columns = columns
    
    # Remove empty columns
    df = df.dropna(axis=1, how='all')
    
    # Remove empty rows
    df = df.dropna(axis=0, subset=['time', 'name_paciente', 'phone_paciente', 'area', 'description'])
    
    # area column
    df.loc[:,"area"] = df["area"].str.split(",")
    df = df.explode('area')
    df.loc[:,'area'] = df['area'].str.replace(":","", regex=True)
    df.loc[:,'area'] = df['area'].str.strip()

    # Datetime column
    df.loc[:,'datetime'] = pd.to_datetime(df['time'], dayfirst=True)
    df[['date','time']] = df['time'].str.split(" ", expand= True )
    
    # Price Column
    df['price'] = df['price'].apply(extrair_precos)
    df["price_max"] = df["price"].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else 300)
    df["price_min"] = df["price"].apply(lambda x: x[1] if isinstance(x, list) and len(x) > 1 else 35)
    df.drop(columns=['price'], inplace=True)

    
    return df


def preprocess_professional(df) -> pd.DataFrame:
    
    # Rename columns
    name_columns = ['name_professional','area','CRN','phone_professional','active']
    columns = list(df.columns)
    for i, col in enumerate(name_columns):
        columns[i] = col
    df.columns = columns
    
    # Remove linhas que tem valor da coluna 'active' como zero
    df = df[df['active'] != 0] 
    
    # Area column
    df.loc[:,"area"] = df["area"].str.split(",")
    df = df.explode('area')
    df.loc[:,'area'] = df['area'].str.replace(":","", regex=True)
    df.loc[:,'area'] = df['area'].str.strip()
    
    # Remove unwanted data
    df = df.dropna(axis=1,how='all')
    df = df.dropna(axis=0,subset=['name_professional', 'area', 'phone_professional'])
    df.loc[:,'phone_professional'] = df['phone_professional'].apply(lambda x: x.replace("wa.me/","") if type(x) == str else x)

    return df


def open_respostas()-> pd.DataFrame:
    client = set_credentials()
    df = get_data(sheets_name="Respostas-2025",page="Respostas", client=client)
    df = preprocess_respostas(df)
    return df


def open_professional()-> pd.DataFrame:
    client = set_credentials()
    df = get_data(sheets_name="Profissionais",page="Página1", client=client)
    df = preprocess_professional(df)
    return df


def open_matches()-> pd.DataFrame:
    try:
        client = set_credentials()
        df = get_data(sheets_name="db-metAMORfose", page="Matches", client=client)
        if df is None or df.empty:
            return pd.DataFrame(columns=["name_paciente", "name_professional" ,"phone_paciente" , "phone_professional", "area", "price", "datetime"])
        return df
    except Exception as e:
        print(f"Error: {e}")
        print(f"Error in open_matchings function.")
        return pd.DataFrame()
    
    
def save_matches(df_matches, df_all_matches)->None:
    base_dir = get_project_root()
    df_all_matches.to_csv(Path(base_dir, f'./csv/matching_all.csv'), index=False)
    df_matches.to_csv(Path(base_dir, f"./csv/matchings_selected.csv"),index=False)
    
    df = df_matches[["name_paciente", "name_professional", "phone_paciente", "phone_professional","description", "area", "datetime", "price_min", "price_max"]]
    pd.set_option('future.no_silent_downcasting', True)
    df = df.fillna('').infer_objects(copy=False)
    client = set_credentials()
    sheet = client.open("db-metAMORfose")
    sheet = sheet.worksheet("Matches")
    # data = [df.columns.tolist()] + df.values.tolist()
    data = df.values.tolist()
    sheet.append_rows(data, value_input_option="USER_ENTERED")
    print("Data saved successfully!")


def open_mock()->pd.DataFrame:
    mock_path = Path(base_path, "csv", "mock_match.csv")
    df = pd.read_csv(mock_path, sep=",",encoding="utf-8",index_col=0)
    df.reset_index(inplace=True)
    return df


def open_mock_professional()->pd.DataFrame:
    mock_path = Path(base_path, "csv", "mock_professionais.csv")
    df = pd.read_csv(mock_path, sep=",",encoding="utf-8",index_col=0)
    df.reset_index(inplace=True)
    df = preprocess_professional(df)
    return df


def open_mock_respostas()->pd.DataFrame:
    mock_path = Path(base_path, "csv", "mock_respostas.csv")
    df = pd.read_csv(mock_path, sep=",",encoding="utf-8",index_col=0)
    df.reset_index(inplace=True)
    df = preprocess_respostas(df)
    return df


def set_credentials() -> gspread.Client:
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    
    credentials_path = Path(base_path, "key", "sheets-service-account.json")
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    client = gspread.authorize(creds)
    return client


def send_data(sheets_name="db-metAMORfose", page = None,df=None)-> None:
    client = set_credentials()
    sheet = client.open(sheets_name)
    sheet = sheet.worksheet(page)
    data = [df.columns.tolist()] + df.values.tolist()
    sheet.update("A1", data)  
    
    
def get_data(sheets_name = "db-metAMORfose", page = None,client=None)-> pd.DataFrame:
    sheet = client.open(sheets_name)
    sheet = sheet.worksheet(page)
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    return df


def main()-> None:
    df_resposta = open_respostas()
    df_professional = open_professional()
    df_resposta.to_csv("./csv/respostas.csv")
    df_professional.to_csv("./csv/professional.csv")
    data_info(df_resposta, "price")


if __name__ == "__main__":
    main()