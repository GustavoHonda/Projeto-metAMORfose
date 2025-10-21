import pandas as pd
import random
from faker import Faker

fake = Faker('pt_BR')
random.seed(42)

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

def generate_mock_respostas(num_rows = 50)->pd.DataFrame:
    # Criar mock de respostas

    areas = ["Personal trainer", "Nutrição", "Psicoterapia", "Clínico geral", "Terapia", "Terapia holística"]

    data = []
    phones = ["11912345678", "11950440023", "11977777777"]
    for i in range(1, num_rows + 1):
        nome = fake.name()
        email = fake.email()
        area = random.choice(areas)
        problema = fake.sentence(nb_words=6)
        row = [
            fake.date_time_this_year().strftime(f"%d/%m/%Y %H:%M:%S"),
            nome,
            email,
            f"55{''.join(str(random.randint(0,9)) for _ in range(8))}",
            area,
            problema,
            "R$30",
            "Sim",
        ]
        data.append(row)
    df_respostas = pd.DataFrame(data, columns=columns)
    return df_respostas

def generate_mock_professionals(n=50, seed=42)-> pd.DataFrame:
    fake = Faker()
    random.seed(seed)
    Faker.seed(seed)

    users=[{"name": "Gustavo USP", "area": "Psicoterapia", "email":"gustavo.honda10@gmail.com", "phone":"11950440023"},
             {"name": "Alaska", "area": "Psicoterapia", "email":"yalaska95@gmail.com", "phone": "11912345678"},
             {"name": "Gustavo Pessoal", "area": "Psicoterapia", "email":"gustavo_honda@usp.br", "phone": "11977777777"},
             {"name": "Empty email", "area": "Psicoterapia", "email":"", "phone": "119987654321"},
             {"name": "Empty phone", "area": "Psicoterapia", "email":"gustavo.honda10@gmail.com", "phone": ""}
             ]

    data = []
    for i in range(1, n + 1):
        user = random.choice(users)
        data.append({
            "name": user["name"],
            "area": user["area"],
            "whatsapp": user["phone"],
            "email": user["email"],
            "active": True,
            "payday": "2024-12-31",
        })

    df = pd.DataFrame(data)
    return df



def main()->None:
    df_profissionais = generate_mock_professionals(50)
    df_respostas = generate_mock_respostas(50)
    
    df_profissionais.to_csv("./csv/mock_professionais.csv", index=False)
    df_respostas.to_csv("./csv/mock_respostas.csv", index=False)

    
if __name__ == "__main__":
    main()