import pandas as pd
from datetime import datetime
from src.matching import match

df_profissional = pd.DataFrame([
        {"name_professional": "Prof A", "area": "psicologia", "phone_professional": "111", "price": 200, "freq": 0}
    ])
df_resposta = pd.DataFrame([
    {"name_paciente": "Paciente A", "area": "psicologia", "datetime": "31/08/2024 21:33:09", "phone_paciente": "(11)912345678", "price": 100},
    {"name_paciente": "Paciente B", "area": "psicologia", "datetime": "31/08/2024 21:33:08", "phone_paciente": "(11)912345678", "price": 150},
])
result = match(df_profissional, df_resposta)


def test_match():  
    assert not result.empty
    
def test_match2():
    assert len(result) == 2
    
def test_match3():
    assert result.iloc[0]["phone_paciente"] == "(11)912345678"
