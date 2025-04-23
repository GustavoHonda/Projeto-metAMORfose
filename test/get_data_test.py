import pandas as pd
from src.get_data import extrair_precos, preprocess_respostas


def test_extrair_precos_simples():
    assert extrair_precos("R$ 200,00") == [200.0]

def test_extrair_precos_multiplos():
    assert extrair_precos("R$ 1.200,50 ou R$ 999,99") == [1200.5, 999.99]

def test_extrair_precos_sem_valor():
    assert extrair_precos("Sem valor") == []

def test_extrair_precos_valor_bruto():
    assert extrair_precos("300") == [300.0]

def test_extrair_precos_com_ponto_milhar():
    assert extrair_precos("1.000") == [1000.0]


def test_preprocess_respostas_minimal(monkeypatch):
    # Simula um dataframe de entrada
    df = pd.DataFrame([{
        'time': '22/12/2024 21:10:00',
        'name_paciente': 'João',
        'e-mail': 'joao@email.com',
        'phone_paciente': '11999999999',
        'area': 'Médico: Psicologia',
        'description': 'preciso de atendimento',
        'max_price': '500',
        'price': 'R$ 200,00',
        'phone2': 'vazio',
        'urgencie': 'média',
        'free_service': 'não',
        'sexual_identity': 'masculino',
        'profissional': 'nenhum',
        'whatsapp': 'sim'
    }])

    df = preprocess_respostas(df)
    assert df['datetime'].dtype == "datetime64[ns]"
    assert df['datetime'].iloc[0] == pd.to_datetime('2024-12-22 21:10:00')
    assert df['price'].iloc[0] == [200.0]
    assert df['area'].iloc[0] == 'Psicologia'
    assert 'datetime' in df.columns
