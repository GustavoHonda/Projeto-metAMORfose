from os import error, write
from src.get_data import open_professional, open_respostas, open_mock, open_matches
from src.get_data import open_mock_professional, open_mock_respostas, data_info
from src.send_msg import AWS_Sender
from src.matching import match



def main(EXECUTION_MODE, SAFE_TO_SEND, SAVE_MATCH)-> int:

    if EXECUTION_MODE == "production":
        print("Running in production mode...")
        df_professional = open_professional()
        print("professionals opened...")
        df_respostas = open_respostas()
        print("respostas opened...")
        df_matchings = open_matches()
        print("respostas matchigs...")
        matched = match(df_professional, df_respostas, df_matchings,SAVE_MATCH)
    
        df_respostas.to_csv("./csv/respostas.csv")
        df_professional.to_csv("./csv/professional.csv")
    elif EXECUTION_MODE == "mock":
        print("Running in mock mode...")
        df_professional = open_mock_professional()
        df_respostas = open_mock_respostas()
        df_matchings = open_matches()
        matched = match(df_professional, df_respostas, df_matchings,SAVE_MATCH)
    
        df_respostas.to_csv("./csv/respostas.csv")
        df_professional.to_csv("./csv/professional.csv")
    elif EXECUTION_MODE == "manual":
        print("Running in manual mode...")
        df_professional = open_professional()
        print("professionals opened...")
        df_respostas = open_respostas()
        print("respostas opened...")
        df_matchings = open_matches()
        print("respostas matchigs...")
        return 0
    else:
        raise ValueError("valor de EXECUTION_MODE inválido")


    if SAFE_TO_SEND:
        
        print("Safe to execute, sending batch...")
        sender  = AWS_Sender()
        response = sender.send_batch(matched)
    print("End of pipeline")
    return 0

if __name__ == "__main__":
    SAVE_MATCH = True     # True, False
    SAFE_TO_SEND = True     # True, False
    EXECUTION_MODE = "mock"  # production, mock, manual

    main(EXECUTION_MODE, SAFE_TO_SEND, SAVE_MATCH)