import pandas as pd
from pandasql import sqldf
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
import logging
logging.basicConfig(level=logging.DEBUG)

from src.get_data import data_info, open_matches, save_matches, open_profissional, open_respostas

# Erros/implementações que tem pra fazer/corrigir nesse módulo:
# 1. matching muito simples
# 2. (FEITO)precisa fazer um loop para todos os profissionais (2 respostas para cada profissional e não 10)
# 3. profissional não pode receber o mesmo contato de paciente 2 vezes
# 4. cada profissional deve receber clientes diferentes


def find_matches(prof, df_resposta, df_matches):
    # query = "SELECT * FROM df_matches"
    # df = ps.sqldf(query,locals())
   # profissional  = prof[["name_professional", "phone_professional", "area", "price"]]
  #  paciente  = df_resposta[["datetime", "name_paciente", "phone_paciente", "area", "price"]]

  pass

   # already_matched_professional_pacient = df_matches[df_matches["phone_professional"] == prof["phone_professional"]]
   # new_matches = df_resposta[df_resposta["area"] == prof["area"]]
    
   # new_matches = new_matches[new_matches["datetime"].isin(already_matched_professional_pacient["datetime"])]
    # new_matches = new_matches.sort_values(by="datetime")
    
    # new_matches['datetime'] =new_matches["datetime"].apply(lambda x: x.isoformat() if pd.notnull(x) else None)
    
    # return new_matches.head(2)


def match(df_profissional, df_resposta):
    df_matches = open_matches()
    results = []
    for _, prof in df_profissional.iterrows():
        best_matches = find_matches(prof, df_resposta, df_matches)
        for _, match in best_matches.iterrows():
            results.append({
                "phone_professional": prof["phone_professional"],
                "name_paciente": match["name_paciente"],
                "phone_paciente": match["phone_paciente"],
                "area": match["area"],
                "price": match["price"][0],
                "datetime": match["datetime"]
            })
    new_matches = pd.DataFrame(results)
    if not new_matches.empty:
        combined = pd.concat([df_matches, new_matches], ignore_index=True)
        save_matches(combined)
        print("Novos pareamentos salvos em df_matches.csv:")
        print(new_matches)
    else:
        print("Nenhum novo pareamento encontrado.")
        
    return new_matches


def main():
    df_profissional = open_profissional()[["name_professional","area", "phone_professional", "price", "freq_professional"]]
    df_resposta = open_respostas()[["name_paciente", "area", "datetime", "phone_paciente", "price","freq_client"]]
   # df_resposta = df_resposta.head(3)
    # print(df_resposta)
   # data_info(df_profissional, "area")
   # data_info(df_resposta, "area")

   # matched = match(df_profissional, df_resposta)
    
   # print(matched)
    
   # pysqldf = lambda q: sqldf(q, globals())
    
    #pysqldf = lambda q: sqldf(q, locals())

    query = """
    SELECT *
    FROM (
        SELECT
            p.name_paciente,
            p.area AS area_comum,
            p.phone_paciente,
            p.price as valor_consulta,
            p.datetime as data_cadastro,
            prof.name_professional,
            prof.area AS area_professional,
            prof.phone_professional,
            prof.price as valor_aceite,
            ROW_NUMBER() OVER (PARTITION BY p.name_paciente ORDER BY prof.price ASC) as rn
        FROM  df_profissional prof
        JOIN df_resposta p
            ON p.area = prof.area
    ) t
    WHERE rn = 1
    ORDER BY data_cadastro DESC
    """
    pysqldf = sqldf(query, locals())
    # Executar a consulta
    resultado = pysqldf
    print(resultado)

    # Salvar os dados em arquivos Excel e CSV

    # Caminho para salvar os arquivos
    caminho_arquivo_excel = 'resultado_pacientes_profissionais.xlsx'
    caminho_arquivo_csv = 'resultado_pacientes_profissionais.csv'

    # Ginecologia = caminho_arquivo_csv.where(caminho_arquivo_csv['area_comum'] = 'Ginecologia')

    # Salvar em Excel
    resultado.to_excel(caminho_arquivo_excel, index=False)

    # Salvar em CSV
    resultado.to_csv(caminho_arquivo_csv, index=False)




    print(f"Arquivos salvos em: {caminho_arquivo_excel} e {caminho_arquivo_csv}")


# 1. Ler o Excel com os matches
    df_resultado = pd.read_excel(caminho_arquivo_excel)

if __name__ == "__main__":
    main()
