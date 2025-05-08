from src.get_data import open_profissional, open_respostas, open_mock
from src.send_msg import send_batch 
from src.matching import match

SAFE_TO_EXEC=False

def main():
    df_profissional = open_profissional()
    df_respostas = open_respostas()
    
    matched = match(df_profissional, df_respostas)
    mock_matched = open_mock()
    if SAFE_TO_EXEC:
        response = send_batch(matched)
        return 0
    else:
        response = send_batch(mock_matched)
        print(response)
        return 0
    