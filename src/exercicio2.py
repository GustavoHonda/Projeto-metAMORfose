
import pandas as pd
from pandasql import sqldf
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import time
import requests


# DataFrame de pacientes (agora com 13 pacientes)
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
        'wa.me/5511950440023', 'wa.me/5511978078949', 'wa.me/5511978078949', 'wa.me/5511978078949', 'wa.me/5511978078949', 'wa.me/5511978078949',
        'wa.me/5511978078949', 'wa.me/5511978078949', 'wa.me/5511978078949', 'wa.me/5511978078949', 'wa.me/5511978078949', 'wa.me/5511978078949', 'wa.me/5511978078949'
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

# DataFrame de profissionais (agora com 6 profissionais)
df_profissional = pd.DataFrame({
    'nome_profissional': [
        'Dr. João', 'Dra. Paula', 'Dr. Marcos', 'Dra. Renata', 'Dr. André', 'Dra. Camila'
    ],
    'area': [
        'Cardiologia', 'Dermatologia', 'Ortopedia', 'Ginecologia', 'Neurologia', 'Ortopedia'
    ],
    'telefone_profissional': [
        'wa.me/5511978078949', 'wa.me/5511950440023', 'wa.me/5511976154853', 'wa.me/5585985410805', 'wa.me/5585985410805', 'wa.me/5516996409979'
    ],
    'valor_aceite': [
        180, 170, 160, 200, 270, 165
    ],
    'Ideintificação_sexual': [
        'Hetero', 'LGBT', 'Hetero', 'LGBT', 'Hetero', 'LGBT'
    ]
})

# Consulta SQL
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

# Executar a consulta
resultado = pysqldf(query)
print(resultado)

# Salvar os dados em arquivos Excel e CSV

# Caminho para salvar os arquivos
caminho_arquivo_excel = 'resultado_pacientes_profissionais.xlsx'
caminho_arquivo_csv = 'resultado_pacientes_profissionais.csv'

# Ginecologia = caminho_arquivo_csv.where(caminho_arquivo_csv['area_comum'] = 'Ginecologia')

# Salvar em Excel
resultado.to_excel(caminho_arquivo_excel, index=False)

# Salvar em CSV
resultado.to_csv(caminho_arquivo_csv, index=False)




print(f"Arquivos salvos em: {caminho_arquivo_excel} e {caminho_arquivo_csv}")


# 1. Ler o Excel com os matches
df_resultado = pd.read_excel(caminho_arquivo_excel)

# 2. Inicializar o navegador (WhatsApp Web)

usuario = 'gustavo_honda@usp.br'
# usuario = 'nsiamfumukunzayila@yahoo.com.br'
dir_path = os.getcwd()
chrome_options2 = Options()
# chrome_options2.add_argument(r"user-data-dir=" + dir_path + "/pasta/sessao")
chrome_options2.add_argument(r"/usr/bin/")
driver = webdriver.Chrome(options=chrome_options2)
driver.get('https://web.whatsapp.com/')
time.sleep(10)
##################################################
# Espera tempo para escanear o QR Code
print("Escaneie o QR Code do WhatsApp Web...")
time.sleep(10)  # ajuste se precisar de mais tempo

# 3. Enviar mensagem para cada profissional
for _, row in df_resultado.iterrows():
    telefone = row['telefone_profissional']
    mensagem = f"""
Olá {row['nome_profissional']}, tudo bem?

Você foi conectado com um paciente da área de {row['area_comum']}:

👤 Nome: {row['nome_paciente']}
📅 Cadastro: {row['data_cadastro']}
📞 Contato: {row['telefone_paciente']}
💰 Valor proposto: R$ {row['valor_consulta']}

Seu valor de aceite é R$ {row['valor_aceite']}.
Entre em contato caso deseje continuar com o atendimento.

Obrigado!
    """

    # Formatar telefone para padrão internacional
    numero_formatado = telefone.replace("-", "").strip()
    link = f"https://web.whatsapp.com/send?phone=55{numero_formatado}&text={requests.utils.quote(mensagem)}"

    ##############################################################
    ##############################################################
    

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Abrir conversa
driver.get(link)
try:
    # Aguarda até que a caixa de texto esteja presente (espera explícita)
    caixa_texto = WebDriverWait(driver, 2500).until(
        EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
    )
    time.sleep(10)  # pequena pausa antes do clique
    # Clicar no botão de enviar (com novo seletor mais robusto)
    botao_enviar = WebDriverWait(driver, 300).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Enviar"]'))
    )
    botao_enviar.click()

    print(f"Mensagem enviada para {row['nome_profissional']}")

except Exception as e:
    print(f"Erro ao enviar mensagem para {telefone}: {e}")
