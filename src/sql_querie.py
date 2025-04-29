import pandas as pd
from pandasql import sqldf


df_paciente = pd.DataFrame({
    'nome_paciente': [
        'Ana', 'Bruno', 'Carlos', 'Daniela', 'Eduardo', 'Fernanda', 'Gabriel', 'Helena',
        'Isabela', 'João', 'Karen', 'Lucas', 'Mariana'
    ],
    'area': [
        'Cardiologia', 'Ortopedia', 'Cardiologia', 'Dermatologia', 'Cardiologia', 'Ortopedia',
        'Neurologia', 'Terapia', 'Psiquiatria', 'Psiquiatria', 'Neurologia', 'Psiquiatria', 'Ginecologia'
    ],
    'telefone_paciente': [
        '1111-1111', '2222-2222', '3333-3333', '4444-4444', '5555-5555', '6666-6666',
        '7777-7777', '8888-8888', '9999-9999', '1010-1010', '1212-1212', '1313-1313', '1414-1414'
    ],
    'valor_consulta': [
        200, 150, 250, 180, 210, 160, 300, 220, 190, 230, 280, 170, 240
    ],
    'Ideintificação_sexual': [
        'Hetero', 'LGBT', 'LGBT', 'Hetero', 'LGBT', 'Hetero', 'LGBT', 'Hetero', 'LGBT',
        'Hetero', 'LGBT', 'LGBT', 'Hetero'
    ],
    'data_cadastro': [
        '2024-04-01', '2024-04-03', '2024-04-05', '2024-04-07', '2024-04-08', '2024-04-09',
        '2024-04-10', '2024-04-11', '2024-04-12', '2024-04-13', '2024-04-14', '2024-04-15', '2024-04-16'
    ]
})


df_profissional = pd.DataFrame({
    'nome_profissional': [
        'Dr. João', 'Dra. Paula', 'Dr. Marcos', 'Dra. Renata', 'Dr. André', 'Dra. Camila'
    ],
    'area': [
        'Cardiologia', 'Dermatologia', 'Ortopedia', 'Ginecologia', 'Neurologia', 'Ortopedia'
    ],
    'telefone_profissional': [
        '9999-9999', '8888-8888', '7777-7777', '6666-6666', '5555-5555', '4444-4444'
    ],
    'valor_aceite': [
        180, 170, 160, 200, 270, 165
    ],
    'Ideintificação_sexual': [
        'Hetero', 'LGBT', 'Hetero', 'LGBT', 'Hetero', 'LGBT'
    ]
})


pysqldf = lambda q: sqldf(q, globals())

query = """
SELECT *
FROM (
    SELECT
        p.nome_paciente,
        p.area AS area_comum,
        p.telefone_paciente,
        p.valor_consulta,
        p.data_cadastro,
        prof.nome_profissional,
        prof.area AS area_profissional,
        prof.telefone_profissional,
        prof.valor_aceite,
        ROW_NUMBER() OVER (PARTITION BY p.nome_paciente ORDER BY prof.valor_aceite ASC) as rn
    FROM df_paciente p
    JOIN df_profissional prof
        ON p.area = prof.area
) t
WHERE rn = 1
ORDER BY data_cadastro DESC
"""


resultado = pysqldf(query)
print(resultado)

caminho_arquivo_csv = './csv/resultado_pacientes_profissionais.csv'

resultado.to_csv(caminho_arquivo_csv, index=False)

print(f"Arquivos salvos em: {caminho_arquivo_csv}")