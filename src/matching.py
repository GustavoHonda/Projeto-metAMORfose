import pandas as pd
from pandasql import sqldf
import logging
logging.basicConfig(level=logging.DEBUG)

from src.get_data import data_info, open_matches, save_matches, open_profissional, open_respostas

# Erros/implementações que tem pra fazer/corrigir nesse módulo:
# 1. matching muito simples
# 2. (FEITO)precisa fazer um loop para todos os profissionais (2 respostas para cada profissional e não 10)
# 3. profissional não pode receber o mesmo contato de paciente 2 vezes
# 4. cada profissional deve receber clientes diferentes


def main():
    df_profissional = open_profissional()[["name_professional","area", "phone_professional", "price", "freq_professional"]]
    df_resposta = open_respostas()[["name_paciente", "area", "datetime", "phone_paciente", "price","freq_client"]]

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

    # Salvar em CSV
    resultado.to_csv(caminho_arquivo_csv, index=False)

    print(f"Arquivos salvos em: {caminho_arquivo_csv}")
    df_resultado = pd.read_csv(caminho_arquivo_csv)
if __name__ == "__main__":
    main()
