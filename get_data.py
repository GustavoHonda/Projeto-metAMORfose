import pandas as pd
import json

with open("../key/sheets_url.json") as file: 
        data = json.load(file) 


def preprocess_respostas(df):
        
        name_columns= ['time','name','e-mail','phone','categorie','description','max_price','price','phone2','urgencie','free_service','sexual_identity','profissional','whatsapp']
        df.columns = name_columns
        df = df.reset_index()
        df = df.dropna(axis=1, how='all')

        # Categorie column
        df["categorie"] = df["categorie"].str.split(",")
        df = df.explode('categorie')
        df['categorie'] = df['categorie'].str.replace("Médico","", regex=True)
        df['categorie'] = df['categorie'].str.replace(":","", regex=True)
        df['categorie'] = df['categorie'].str.strip()

        # Datetime column
        df['datetime'] = pd.to_datetime(df['time'], dayfirst=True)
        df['datetime'] = df['datetime'].dt.strftime(f'%Y/%m/%d %H:%M:%S')
        df[['date','time']] = df['time'].str.split(" ", expand= True )
        return df

def preprocess_profissional(df) -> pd.DataFrame:
        
        # Adding new data
        df['freq'] = '0'
        
        # Rename columns
        name_columns = ['name','area','CRN','phone','price','none','gender','freq']
        df.columns = name_columns
        
        # Remove unwanted data
        df = df.dropna(axis=1)
        df.loc[:,'phone'] = df['phone'].apply(lambda x: x.replace("wa.me/",""),)
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


def main():
        df_resposta = open_respostas()
        df_profissional = open_profissional()
        
        print(df_resposta)
        
        # df_resposta = pd.merge(df_profissional, df_resposta, on=['categorie','price'], how='inner')
        # result_professional = df_profissional.loc[df_profissional['categorie'] == "Psiquiatria"]
        # result_resposta = df_resposta.loc[df_resposta['categorie'] == "Psiquiatria"]
        

if __name__ == "__main__":
        main()



