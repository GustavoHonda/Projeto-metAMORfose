from src.get_data import open_profissional, open_respostas
from src.send_msg import send_batch 
from src.matching import match

SAFE_TO_EXEC=False

def main():
    df_profissional = open_profissional()
    df_respostas = open_respostas()
    
    matched = match(df_profissional, df_respostas)
    if SAFE_TO_EXEC:
        response = send_batch(matched)
    else:
        exit(0)