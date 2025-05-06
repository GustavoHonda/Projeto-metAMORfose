import pandas as pd
from pandasql import sqldf

from src.get_data import data_info, open_matches, save_matches, open_profissional, open_respostas

# Erros/implementações que tem pra fazer/corrigir nesse módulo:
# 1. matching muito simples
# 2. (FEITO)precisa fazer um loop para todos os profissionais (2 respostas para cada profissional e não 10)
# 3. profissional não pode receber o mesmo contato de paciente 2 vezes
# 4. cada profissional deve receber clientes diferentes

def match(df_profissional, df_resposta):
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
    resultado = sqldf(query, locals())
    return resultado

def main():
    df_profissional = open_profissional()[["name_professional","area", "phone_professional", "price", "freq_professional"]]
    df_resposta = open_respostas()[["name_paciente", "area", "datetime", "phone_paciente", "price","freq_client"]]
    caminho_arquivo_csv = './csv/resultado_pacientes_profissionais.csv'

    resultado = match(df_profissional, df_resposta)
    print(resultado.shape[0])
    print(resultado)

    # Salvar em CSV
    resultado.to_csv(caminho_arquivo_csv, index=False)

    print(f"Arquivos salvos em: {caminho_arquivo_csv}")
    df_resultado = pd.read_csv(caminho_arquivo_csv)
    
    
def main2():
    df_profissional = pd.DataFrame([
        {"name_professional": "Prof A", "area": "psicologia", "phone_professional": "111", "price": 200, "freq": 0}
    ])
    df_resposta = pd.DataFrame([
        {"name_paciente": "Paciente A", "area": "psicologia", "datetime": "31/08/2024 21:33:09", "phone_paciente": "999", "price": 100},
        {"name_paciente": "Paciente B", "area": "psicologia", "datetime": "31/08/2024 21:33:08", "phone_paciente": "888", "price": 150},
    ])
    result = match(df_profissional, df_resposta)    
    print(result)

if __name__ == "__main__":
    main2()
