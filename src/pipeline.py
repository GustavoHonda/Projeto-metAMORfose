from src.get_data import open_professional, open_respostas, open_mock, open_matches
from src.get_data import open_mock_professional, open_mock_respostas, data_info
from src.send_msg import send_batch 
from src.matching import match

SAFE_TO_EXEC=True
EXECUTION_MODE="production"

def main():
    if EXECUTION_MODE == "production":
        print("Running in production mode...")
        df_professional = open_professional()
        print("professionals opened...")
        df_respostas = open_respostas()
        print("respostas opened...")
        df_matchings = open_matches()
        print("respostas matchigs...")
        matched = match(df_professional, df_respostas, df_matchings)
        print(matched)
    elif EXECUTION_MODE == "mock":
        print("Running in mock mode...")
        df_professional = open_mock_professional()
        df_respostas = open_mock_respostas()
        df_matchings = open_matches()
        matched = match(df_professional, df_respostas, df_matchings)
    else:
        return
    
    if SAFE_TO_EXEC:
        
        print("Safe to execute, sending batch...")
        response = send_batch(matched)
    print("End of pipeline")
    return 0