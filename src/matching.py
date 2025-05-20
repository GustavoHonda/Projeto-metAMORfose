import pandas as pd
from pandasql import sqldf
from collections import defaultdict

from src.get_data import data_info, open_matches, save_matches, open_professional, open_respostas, open_mock_professional, open_mock_respostas

# Erros/implementações que tem pra fazer/corrigir nesse módulo:
# 1. (FEITO)matching muito simples
# 2. (FEITO)precisa fazer um loop para todos os profissionais (2 respostas para cada professional e não 10)
# 3. (FEITO)professional não pode receber o mesmo contato de paciente 2 vezes
# 4. (FEITO)cada professional deve receber clientes diferentes
# 5. Atualizar testes
# 6. 

def all_match(df_professional, df_resposta,df_matchings):
    query = """
    SELECT 
        paci.name_paciente,
        paci.area AS area,
        paci.phone_paciente,
        paci.price AS price,
        paci.datetime AS datetime,
        prof.name_professional,
        prof.area AS area_professional,
        prof.phone_professional,
        prof.price AS price_professional,
        ROW_NUMBER() OVER (PARTITION BY paci.name_paciente ORDER BY paci.datetime DESC, prof.price ASC) as rn_paci
    FROM df_professional prof
    JOIN df_resposta paci
        ON paci.area = prof.area
    LEFT JOIN df_matchings prev
        ON paci.name_paciente = prev.name_paciente
        AND prof.name_professional = prev.name_professional
    WHERE prev.name_paciente IS NULL
    AND prev.name_professional IS NULL
    """
    all_matches = sqldf(query, locals())
    return all_matches

def select_match(df_matchings,df_all_matches):
    # Inicializar estruturas
    paciente_counts = defaultdict(int)
    profissionais_usados = set()
    matchings_final = []

    # Criar set de tuplas para comparação rápida dos matchings existentes
    matchings_existentes = set()
    if not df_matchings.empty:
        matchings_existentes = set(
            tuple(row) for row in df_matchings[['name_paciente', 'name_professional']].values
        )

    df_all_matches = df_all_matches.sample(frac=1, random_state=42).reset_index(drop=True)
    # Algoritmo guloso
    for _, row in df_all_matches.iterrows():
        paciente = row['name_paciente']
        professional = row['name_professional']
        chave = (paciente, professional)

        if chave in matchings_existentes:
            continue
        if professional in profissionais_usados:
            continue
        if paciente_counts[paciente] >= 2:
            continue

        # Adiciona o matching
        matchings_final.append(row)
        profissionais_usados.add(professional)
        paciente_counts[paciente] += 1

    # Resultado como DataFrame
    result_df = pd.DataFrame(matchings_final)
    return result_df

def match(df_professional, df_resposta, df_matchings):
    
    df_all_matches = all_match(df_professional, df_resposta,df_matchings)
    resultado = select_match(df_matchings,df_all_matches)
    
    save_matches(resultado[["name_paciente", "name_professional", "area", "datetime", "price"]])
    df_all_matches.to_csv('./csv/all_matching.csv', index=False)
    resultado.to_csv("./csv/selected_matchings.csv",index=False)
    
    return resultado


def main():
    df_professional = open_professional()[["name_professional","area", "phone_professional", "price", "freq_professional"]]
    df_resposta = open_respostas()[["name_paciente", "area", "datetime", "phone_paciente", "price","freq_client"]]
    df_matchings = open_matches()[["name_paciente", "name_professional", "area", "datetime", "price"]]

    resultado = match(df_professional,df_resposta,df_matchings)
    

def mock():
    df_professional = open_mock_professional()
    df_paciente = open_mock_respostas()
    df_matches = open_matches()
    
    resultado = match(df_professional, df_paciente, df_matches)
    

if __name__ == "__main__":
    main()
    # mock()


# Elen Terapia Holística (Terapia holistica)
# Guilherme (Clinico Geral)
# Lorena (Clinico Geral)
# Priscila (Terapia holistica)