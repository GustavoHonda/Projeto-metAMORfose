import pandas as pd
import json
import requests
import re


# Erros/implementações que tem pra fazer/corrigir nesse módulo:
# 1.coluna price de df_respostas tem descrição dos preços solicitados, precisa transformar para int
# 2.extrair mais informações da descrição das respostas de cada paciente(implementação complicada)


def data_info(df,column):
    """
    Função auxiliar que mostra os valores únicos e tipo de certa coluna do dataframe

    Args:
        df (pd.Dataframe): Dataframe analisado
        column (str): coluna analisada
    """
    
    print(df[column].unique())
    print(df[column].dtype)


with open("../key/sheets_url.json") as file: 
        data = json.load(file) 


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
    name_columns= ['time','name_paciente','e-mail','phone_paciente','area','description','max_price','price','phone2','urgencie','free_service','sexual_identity','profissional','whatsapp']
    df.columns = name_columns
    type_columns=[str,str,str,int,str,str,int,int,int,str,str,str,str,str]
    print(df['price'].head(286))
    df = df.dropna(axis=1, how='all')

    # area column
    df.loc[:,"area"] = df["area"].str.split(",")
    df = df.explode('area')
    df.loc[:,'area'] = df['area'].str.replace("Médico","", regex=True)
    df.loc[:,'area'] = df['area'].str.replace(":","", regex=True)
    df.loc[:,'area'] = df['area'].str.strip()

    # Datetime column
    df.loc[:,'datetime'] = pd.to_datetime(df['time'], dayfirst=True)
    df.loc[:,'datetime'] = df['datetime'].dt.strftime(f'%Y/%m/%d %H:%M:%S')
    df[['date','time']] = df['time'].str.split(" ", expand= True )
    
    # Price Column
    df['price'] = df['price'].apply(extrair_precos)
    print(df['price'].head(286))
    
    return df


def preprocess_profissional(df) -> pd.DataFrame:
    # Adding new data
    df['freq'] = '0'
    
    # Rename columns
    name_columns = ['name_professional','area','CRN','phone_professional','price','gender','freq']
    df.columns = name_columns
    
    # Remove unwanted data
    df = df.dropna(axis=1,how='all')
    df = df.dropna(axis=0,how='any')
    df.loc[:,'phone_professional'] = df['phone_professional'].apply(lambda x: x.replace("wa.me/","") if type(x) == str else x)
    df.loc[:,'price'] = df['price'].apply(lambda x: x.replace("+","") if type(x) == str else x )
    
    # Setting correct types
    type_columns = [str,str,str,int,int,object,str,int]
    for i,coluna in enumerate(df.columns):
            df.loc[:,coluna] = df[coluna].astype(str).astype(type_columns[i])
    return df


def open_respostas():
    sheets_respostas = data['url_respostas']
    df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheets_respostas}/export?format=csv")
    df = preprocess_respostas(df)
    return df


def open_profissional():
    sheets_professional = data['url_profissionais']
    df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheets_professional}/export?format=csv")
    df = preprocess_profissional(df)
    return df


def send_data(row, col, value):
    payload = {"row": row, "col": col, "value": value}
    url = data['url_google_script']
    response = requests.post(url, data=payload)
    if str(response) == "<Response [200]>":
            print("Request Accepted!")
    else:
            print(response)
    return response


def main():
    # Get dataframes of resposta & profissional
    df_resposta = open_respostas()
    df_profissional = open_profissional()
    response = send_data(40,1,"Modificado")


if __name__ == "__main__":
    main()