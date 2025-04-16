from get_data import open_profissional, open_respostas, data_info
import pandas as pd


# Erros/implementações que tem pra fazer/corrigir nesse módulo:

def match(df_profissional, df_resposta):
    df_profissional = df_profissional[["area","phone_professional","price","freq"]]
    res = df_resposta['phone_paciente']
    df_resposta = df_resposta[["datetime","phone_paciente","area","name_paciente","price"]]
    df_merge = pd.merge(df_profissional, df_resposta, on='area', how='inner')
    df_merge["freq"] = df_merge['freq'].astype(str).astype(int)
    df_merge.iloc[5,df_merge.columns.get_loc("freq")] = -1
    df_merge = df_merge.sort_values('freq',ascending=True)
    top_10 = df_merge.head(10)
    
    return top_10
    

def main():
    df1 = open_profissional()
    df2 = open_respostas()
    top_10 = match(df1,df2)
    print(top_10)
    
    
if __name__ == "__main__":
    main()