from src.get_data import open_professional, open_respostas, open_mock, open_matches
from src.get_data import open_mock_professional, open_mock_respostas
from src.send_msg import send_batch 
from src.matching import match

SAFE_TO_EXEC=False
EXECUTION_MODE = "mock"

def main():
    
    if EXECUTION_MODE := "production":
        df_professional = open_professional()
        df_respostas = open_respostas()
        df_matchings = open_matches()
        matched = match(df_professional, df_respostas, df_matchings)
        print(matched)
    elif EXECUTION_MODE == "mock":
        df_professional = open_mock_professional()
        df_respostas = open_mock_respostas()
        df_matchings = open_matches()
        matched = match(df_professional, df_respostas, df_matchings)
    else:
        return
        
    if SAFE_TO_EXEC:
        print("Safe to execute, sending batch...")
        # response = send_batch(matched)
    return 0