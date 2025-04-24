import pandas as pd
from src.get_data import data_info, open_matches, save_matches, open_profissional, open_respostas

# Erros/implementações que tem pra fazer/corrigir nesse módulo:
# 1. matching muito simples
# 2. precisa fazer um loop para todos os profissionais (2 respostas para cada profissional e não 10)
# 3. profissional não pode receber o mesmo contato de paciente 2 vezes


def get_best_matches_for_professional(prof, df_resposta, df_matches):
    prof_phone = prof["phone_professional"]
    prof_area = prof["area"]
    already_matched_professional_pacient = df_matches[df_matches["phone_professional"] == prof_phone]
    already_matched_professional_pacient = already_matched_professional_pacient["phone_paciente"].unique()
    new_matches = df_resposta[df_resposta["area"] == prof_area]
    new_matches = new_matches[~new_matches["phone_paciente"].isin(already_matched_professional_pacient)]
    new_matches = new_matches.sort_values(by="datetime")
    return new_matches.head(2)

def match_all(df_profissional, df_resposta, df_matches):
    results = []
    for _, prof in df_profissional.iterrows():
        best_matches = get_best_matches_for_professional(prof, df_resposta, df_matches)
        for _, match in best_matches.iterrows():
            results.append({
                "phone_professional": prof["phone_professional"],
                "name_paciente": match["name_paciente"],
                "phone_paciente": match["phone_paciente"],
                "area": match["area"],
                "price": match["price"],
                "datetime": match["datetime"]
            })
    return pd.DataFrame(results)

def main():
    df_profissional = open_profissional()[["name_professional","area", "phone_professional", "price", "freq"]]
    df_resposta = open_respostas()[["name_paciente", "area", "datetime", "phone_paciente", "price"]]
    df_matches = open_matches()
    print(df_matches)
    
    # data_info(df_profissional, "area")
    # data_info(df_resposta, "area")
    
    new_matches = match_all(df_profissional, df_resposta, df_matches)
    if not new_matches.empty:
        combined = pd.concat([df_matches, new_matches], ignore_index=True)
        print(combined)
        save_matches(combined)
        print("Novos pareamentos salvos em df_matches.csv:")
        print(new_matches)
    else:
        print("Nenhum novo pareamento encontrado.")

if __name__ == "__main__":
    main()
