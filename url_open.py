
import pandas as pd
import json

with open("../key/sheets_url.json") as file: 
        data = json.load(file) 

sheets_respostas = data['url_respostas']
df_resposta = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheets_respostas}/export?format=csv")
nome_colunas= ['time','name','e-mail','phone','categorie','description','max_price','price','phone2','urgencie','free_service','sexual_identity','profissional','whatsapp']
df_resposta.columns = nome_colunas

sheets_professional = data['url_profissionais']
df_professional = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheets_professional}/export?format=csv")
nome_colunas = ['name','categorie','CRN','phone','price','none','gender']
df_professional.columns = nome_colunas
print(df_professional)

df_resposta = pd.merge(df_professional, df_resposta, on=['categorie','price'], how='inner')
result_professional = df_professional.loc[df_professional['categorie'] == "Psiquiatria"]
result_resposta = df_resposta.loc[df_resposta['categorie'] == "Psiquiatria"]
# print(df_resposta)