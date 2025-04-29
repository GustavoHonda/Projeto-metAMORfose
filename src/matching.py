import pandas as pd
import pandasql as ps
from src.get_data import data_info, open_matches, save_matches, open_profissional, open_respostas

# Erros/implementações que tem pra fazer/corrigir nesse módulo:
# 1. matching muito simples
# 2. (FEITO)precisa fazer um loop para todos os profissionais (2 respostas para cada profissional e não 10)
# 3. profissional não pode receber o mesmo contato de paciente 2 vezes
# 4. cada profissional deve receber clientes diferentes


def find_matches(prof, df_resposta, df_matches):
    # query = "SELECT * FROM df_matches"
    # df = ps.sqldf(query,locals())
    
    already_matched_professional_pacient = df_matches[df_matches["phone_professional"] == prof["phone_professional"]]
    new_matches = df_resposta[df_resposta["area"] == prof["area"]]
    
    new_matches = new_matches[new_matches["datetime"].isin(already_matched_professional_pacient["datetime"])]
    new_matches = new_matches.sort_values(by="datetime")
    
    new_matches['datetime'] =new_matches["datetime"].apply(lambda x: x.isoformat() if pd.notnull(x) else None)
    
    return new_matches.head(2)


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
    df_resposta = df_resposta.head(3)
    # print(df_resposta)
    data_info(df_profissional, "area")
    data_info(df_resposta, "area")
    
    matched = match(df_profissional, df_resposta)
    
    print(matched)
    

if __name__ == "__main__":
    main()
