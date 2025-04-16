import pandas as pd
import json
import requests


# Erros/implementações que tem pra fazer/corrigir nesse módulo:
# 1.coluna price de df_respostas tem descrição dos preços solicitados, precisa transformar para int
# 2.extrair mais informações da descrição das respostas de cada paciente(implementação complicada)
# 3.

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


def preprocess_respostas(df):
        name_columns= ['time','name_paciente','e-mail','phone_paciente','area','description','max_price','price','phone2','urgencie','free_service','sexual_identity','profissional','whatsapp']
        df.columns = name_columns
        type_columns=[str,str,str,int,str,str,int,int,int,str,str,str,str,str]
        
        # df = df.reset_index()
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
        return df


def preprocess_profissional(df) -> pd.DataFrame:
        # Adding new data
        df['freq'] = '0'
        
        # Rename columns
        name_columns = ['name_professional','area','CRN','phone_professional','price','gender','freq']
        df.columns = name_columns
        
        # Remove unwanted data
        df = df.dropna(axis=1)
        df.loc[:,'phone_professional'] = df['phone_professional'].apply(lambda x: x.replace("wa.me/",""),)
        df.loc[:,'price'] = df['price'].apply(lambda x: x.replace("+",""))
        
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
        
        print(df_resposta)
        
        # Modify value from sheets table obs: (ainda tem erro ao modificar tabela, depois não é possível obter as informações da planilha)
        # response = send_data(40,1,"Modificado")


if __name__ == "__main__":
        main()