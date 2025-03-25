
import pandas as pd

nome_colunas= ['time','name','e-mail','phone','categorie','description','max_price','price','phone2','urgencie','free_service','sexual_identity','profissional','whatsapp','none1','none2','none3','none4','none5']

sheets_respostas = '1oYmgd_7PBhEOhva35GOjlnjJKak0dQ54_Gwl3qizyg8'
df_resposta = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheets_respostas}/export?format=csv")

df_resposta.columns = nome_colunas

# print(df_resposta)

sheets_professional = '1bR0JO10IrKomcis7fZQp0832bV96lzF0fuMMMwTSyhQ'
df_professional = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheets_professional}/export?format=csv")

# print(df_professional)

df_resposta = pd.merge(df_professional, df_resposta, on='categorie', how='inner')



result_professional = df_professional.loc[df_professional['categorie'] == "Psiquiatria"]
result_resposta = df_resposta.loc[df_resposta['categorie'] == "Psiquiatria"]
print(df_resposta)