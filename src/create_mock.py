import pandas as pd
import random
from faker import Faker

fake = Faker('pt_BR')
random.seed(42)

# Áreas possíveis
areas = [
    "Personal trainer", "Nutrição", "Psicoterapia", "Clínico geral", "Terapia", "Terapia holística"
]

# Cabeçalhos
columns = [
    "Carimbo de data/hora",
    "Nome do paciente",
    "Endereço de e-mail",
    "Seu nome e whatsapp (escreva wa.me/55 e seu número com ddd)",
    "Qual área professional de saúde você precisa urgente?",
    "Quais principais problemas você enfrenta hoje?",
    "Qual é um valor justo por sessão para você?",
    "Nós temos um programa de Assistência pra Saúde Mental gratuita. Mas além dessa Assistência, temos Profissionais de saúde que podem te atender de maneira personalizada e humanizada. Você quer receber atividades terapêuticas gratuitas, além da indicação de Profissionais de Saúde?",
]

prices = [30, 50, 60, 70, 80, 90, 100]

def generate_mock_respostas(num_rows = 50):
    # Criar mock de respostas
    data = []
    for i in range(1, num_rows + 1):
        nome = fake.name()
        email = fake.email()
        telefone = fake.numerify(text="11950440023")
        area = random.choice(areas)
        problema = fake.sentence(nb_words=6)
        preco = random.choice(prices)
        row = [
            fake.date_time_this_year().strftime(f"%d/%m/%Y %H:%M:%S"),
            nome,
            email,
            f"55{telefone}",
            area,
            problema,
            preco,
            "Sim",
        ]
        data.append(row)
    df_respostas = pd.DataFrame(data, columns=columns)
    return df_respostas


def generate_mock_professionals(n=50, seed=42):
    fake = Faker()
    random.seed(seed)
    Faker.seed(seed)

    data = []
    for i in range(1, n + 1):
        name = fake.name()
        area = random.choice(areas)
        registration = f"REG{random.randint(10000, 99999)}"
        phone_number = f"wa.me/5511950440023"
        price = random.choice(prices)
        data.append({
            "name": name,
            "area": area,
            "registration": registration,
            "whatsapp": phone_number,
            "price": price,
        })

    df = pd.DataFrame(data)
    return df



def main():
    df_profissionais = generate_mock_professionals(50)
    df_respostas = generate_mock_respostas(50)
    
    df_profissionais.to_csv("./csv/mock_professionais.csv", index=False)
    df_respostas.to_csv("./csv/mock_respostas.csv", index=False)

    
if __name__ == "__main__":
    main()