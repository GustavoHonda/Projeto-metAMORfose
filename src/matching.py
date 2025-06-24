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
# 6. (ANALIZAR) viabilidade de adicionar matching de profissionais e pacientes 

def all_match(df_professional, df_resposta,df_matchings):
    query = """
    SELECT 
        paci.name_paciente,
        paci.area AS area,
        paci.phone_paciente,
        paci.price_max AS price_max,
        paci.price_min AS price_min,
        paci.datetime AS datetime,
        paci.description AS description,
        prof.name_professional,
        prof.area AS area_professional,
        prof.phone_professional,
        ROW_NUMBER() OVER (PARTITION BY paci.phone_paciente ORDER BY paci.datetime DESC) as rn_paci
    FROM df_professional prof
    JOIN df_resposta paci
        ON paci.area = prof.area
    """
    # LEFT JOIN df_matchings prev
    #     ON paci.phone_paciente = prev.phone_paciente
    #     AND prof.phone_professional = prev.phone_professional
    # WHERE prev.phone_paciente IS NULL
    # AND prev.phone_professional IS NULL
    
    all_matches = sqldf(query, locals())
    return all_matches

def select_match(df_matchings,df_all_matches)-> pd.DataFrame:
    query = """
    SELECT 
        all_matches.datetime,
        all_matches.name_paciente,
        all_matches.name_professional,
        all_matches.phone_paciente,
        all_matches.phone_professional,
        all_matches.description,
        all_matches.area,
        all_matches.price_max,
        all_matches.price_min
    FROM df_all_matches all_matches
    LEFT JOIN df_matchings prev
        ON all_matches.phone_paciente = prev.phone_paciente
        AND all_matches.phone_professional = prev.phone_professional
    WHERE prev.phone_paciente IS NULL
    AND prev.phone_professional IS NULL
    """
    
    df_selected_matches = sqldf(query, locals())
    
    # Inicializar estruturas
    paciente_counts = defaultdict(int)
    profissionais_usados = set()
    matchings_final = []

    # Criar set de tuplas para comparação rápida dos matchings existentes
    matchings_existentes = set()
    if not df_matchings.empty:
        matchings_existentes = set(
            tuple(row) for row in df_matchings[['phone_paciente', 'phone_professional']].values
        )

    df_selected_matches = df_selected_matches.sample(frac=1, random_state=42).reset_index(drop=True)
    # Algoritmo guloso
    for _, row in df_selected_matches.iterrows():
        paciente = row['phone_paciente']
        
        professional = row['phone_professional']
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
    result_df = pd.DataFrame(matchings_final, columns=df_all_matches.columns)
    return result_df

def add_missing_matches(df_professional, df_selected_matches, df_all_matches):
    # Calcula os telefones dos profissionais que não foram selecionados
    prof_phones = set(df_professional['phone_professional'])
    selected_phones = set(df_selected_matches['phone_professional'])
    missing_phones = prof_phones - selected_phones

    if missing_phones:
        print(f"Warning!!! Profissionais que não foram selecionados: {len(missing_phones)}")
    else:
        print("Todos os profissionais foram selecionados.")
        return df_selected_matches
    
    # Seleciona os matches que faltam Randomicamente de todos os matchings
    new_matches = []
    for phone in missing_phones:
        possible_matches = df_all_matches[df_all_matches['phone_professional'] == phone]
    if not possible_matches.empty:
        random_match = possible_matches.sample(1)
        new_matches.append(random_match)
    else:
        print(f"Aviso!!! nenhum match disponível para profissional {phone}.")

    # Concatena os novos matches com os já selecionados
    if new_matches:
        df_extra_matches = pd.concat(new_matches, ignore_index=True)
        df_selected_matches = pd.concat([df_selected_matches, df_extra_matches], ignore_index=True)
        print(f"{len(df_extra_matches)} novos matches adicionados.")
    else:
        print("Nenhum novo match foi adicionado.")
    
    return df_selected_matches


def match(df_professional, df_resposta, df_matchings):
    df_all_matches = all_match(df_professional, df_resposta,df_matchings)
    df_selected_matches = select_match(df_matchings,df_all_matches)
    df_selected_matches = add_missing_matches(df_professional, df_selected_matches, df_all_matches)
    if not df_selected_matches.empty:
        save_matches(df_selected_matches,df_all_matches)
    return df_selected_matches


def main():
    df_professional = open_professional()
    df_resposta = open_respostas()
    df_matchings = open_matches()
    
    resultado = match(df_professional,df_resposta,df_matchings)


def mock():
    df_professional = open_mock_professional()
    df_paciente = open_mock_respostas()
    df_matches = open_matches()

    resultado = match(df_professional, df_paciente, df_matches)

if __name__ == "__main__":
    # main()
    mock()