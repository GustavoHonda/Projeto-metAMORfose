import pandas as pd
from datetime import datetime
from src.matching import find_matches, match

def test_find_matches():
    prof = {"phone_professional": "111", "area": "psicologia"}
    df_resposta = pd.DataFrame([
        {"name_paciente": "Paciente A", "area": "psicologia", "datetime": datetime(2024, 1, 1), "phone_paciente": "999", "price": 100},
        {"name_paciente": "Paciente B", "area": "psicologia", "datetime": datetime(2024, 1, 2), "phone_paciente": "888", "price": 150},
        {"name_paciente": "Paciente C", "area": "nutrição", "datetime": datetime(2024, 1, 3), "phone_paciente": "777", "price": 120},
    ])
    df_matches = pd.DataFrame([
        {"phone_professional": "111", "phone_paciente": "999"}  # Paciente A já foi pareado
    ])
    
    result = find_matches(prof, df_resposta, df_matches)
    assert len(result) == 1
    assert result.iloc[0]["phone_paciente"] == "888"  # Apenas Paciente B deve retornar

def test_match():
    df_profissional = pd.DataFrame([
        {"name_professional": "Prof A", "area": "psicologia", "phone_professional": "111", "price": 200, "freq": 0}
    ])
    df_resposta = pd.DataFrame([
        {"name_paciente": "Paciente A", "area": "psicologia", "datetime": datetime(2024, 1, 1), "phone_paciente": "999", "price": 100},
        {"name_paciente": "Paciente B", "area": "psicologia", "datetime": datetime(2024, 1, 2), "phone_paciente": "888", "price": 150},
    ])
    
    result = match(df_profissional, df_resposta)
    assert not result.empty
    assert result.shape[0] == 1
    assert result.iloc[0]["phone_paciente"] == "888"

