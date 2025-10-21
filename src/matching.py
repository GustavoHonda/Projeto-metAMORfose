import pandas as pd
from pandasql import sqldf
from collections import defaultdict
from src.get_data import data_info, open_matches, save_matches, open_professional, open_respostas, open_mock_professional, open_mock_respostas
from datetime import datetime
# from src.send_msg import df

# Erros/implementações que tem pra fazer/corrigir nesse módulo:
# 1. (FEITO)matching muito simples
# 2. (FEITO)precisa fazer um loop para todos os profissionais (2 respostas para cada professional e não 10)
# 3. (FEITO)professional não pode receber o mesmo contato de paciente 2 vezes
# 4. (FEITO)cada professional deve receber clientes diferentes
# 5. Atualizar testes
# 6. (ANALIZAR) viabilidade de adicionar matching de profissionais e pacientes 

def all_match(df_professional, df_resposta,df_matchings)-> pd.DataFrame:
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
        prof.email_professional,
        ROW_NUMBER() OVER (PARTITION BY paci.phone_paciente ORDER BY paci.datetime DESC) as rn_paci
    FROM df_professional prof
    JOIN df_resposta paci
        ON paci.area = prof.area
    """
    
    all_matches = sqldf(query, locals())
    return all_matches


def select_match(df_matchings, df_all_matches) -> pd.DataFrame:
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
        all_matches.price_min,
        all_matches.email_professional
    FROM df_all_matches all_matches
    LEFT JOIN df_matchings prev
        ON all_matches.phone_paciente = prev.phone_paciente
        AND all_matches.phone_professional = prev.phone_professional
    WHERE prev.phone_paciente IS NULL
    AND prev.phone_professional IS NULL
    """
    
    df_selected_matches = sqldf(query, locals())
    
    # Embaralhar para reduzir viés
    df_selected_matches = df_selected_matches.sample(frac=1, random_state=42).reset_index(drop=True)

    # contadores
    matchings_arquivados = set()
    if not df_matchings.empty:
        for row in df_matchings[['phone_paciente', 'phone_professional']].values:
            matchings_arquivados.add(tuple(row))
    matchings_existentes = defaultdict(int)
    professional_counts = defaultdict(int)
    matchings_final = []
    
    condition = 1
    while(condition):
        print(f"Iteração: {condition}")
        paciente_counts = defaultdict(int)

        # Loop guloso para selecionar matchings
        for _, row in df_selected_matches.iterrows():
            paciente = row['phone_paciente']
            professional = row['phone_professional']
            chave = (paciente, professional)

            if chave in matchings_arquivados:
                if condition > 2:
                    pass
                else:
                    continue
            if paciente_counts[paciente] >= 1:
                continue
            if professional_counts[professional] >= 4:
                continue
            if chave in matchings_existentes:
                continue

            # garante homogeneidade:
            min_count = min(professional_counts.values(), default=0)
            if professional_counts[professional] > min_count:
                continue  # pula se esse profissional já está acima da mínima

            # adiciona o matching
            matchings_final.append(row)
            paciente_counts[paciente] += 1
            professional_counts[professional] += 1
            matchings_existentes[chave] = matchings_existentes.get(chave,0) + 1  # marca como existente

        # Verificar se todos os profissionais têm pelo menos 4 pacientes
        if all(count >= 4 for count in professional_counts.values()):
            condition = 0  # todos os profissionais têm pelo menos 4 pacientes
        elif(condition < 3):
            condition += 1
        else:
            condition = 0  # evita loop infinito, sai após 3 tentativas
            
            print("🔹 Pacientes Atribuidos por profissional")
            for key in professional_counts.keys():
                print(f"    Profissional {key}: {professional_counts[key]} pacientes")

            print(" ⚠️ Limite de iterações atingido, saindo do loop. Nem todos os profissionais atingiram 4 pacientes.")

    result_df = pd.DataFrame(matchings_final, columns=df_all_matches.columns)
    return result_df
       

def match(df_professional, df_resposta, df_matchings, save=False)-> pd.DataFrame:
    df_all_matches = all_match(df_professional, df_resposta,df_matchings)
    df_selected_matches = select_match(df_matchings,df_all_matches)
    

    df_selected_matches["match_time"] = datetime.now()   
    if not df_selected_matches.empty:
        save_matches(df_selected_matches,df_all_matches,save)

    return df_selected_matches


def main()-> None:
    df_professional = open_professional()
    df_resposta = open_respostas()
    df_matchings = open_matches()
    
    resultado = match(df_professional,df_resposta,df_matchings,False)


def mock()-> None:
    df_professional = open_mock_professional()
    df_paciente = open_mock_respostas()
    df_matches = open_matches()

    print(df_professional.head())
    print(df_paciente.head())
    print(df_matches.head())
    resultado = match(df_professional, df_paciente, df_matches,False)

    print(resultado.head(20))
if __name__ == "__main__":
    # main()
    mock()