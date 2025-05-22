from src.get_data import open_professional, open_respostas, open_mock, open_matches
from src.get_data import open_mock_professional, open_mock_respostas
from src.send_msg import send_batch 
from src.matching import match




SAFE_TO_EXEC=False

def main():

    df_professional = open_mock_professional()
    df_respostas = open_mock_respostas()
    df_matchings = open_matches()
    
    matched = match(df_professional, df_respostas, df_matchings)
    # mock_matched = open_mock()
    if SAFE_TO_EXEC:
        response = send_batch(matched)
        return 0
    else:
        response = send_batch(matched)
        print(response)
        return 0
    