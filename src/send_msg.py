from src.get_data import open_mock
from src.utils.path import get_project_root
from abc import ABC, abstractmethod
import os
import boto3
import json


base_path = get_project_root()
os.environ.setdefault("DISPLAY", ":0")

class SendMsg(ABC):
    @abstractmethod
    def send_msg(self, fields)-> None:
        pass

    @abstractmethod
    def send_batch(self, df)-> None:
        pass


class AWS_Sender(SendMsg):
    def send_msg(self, fields)-> None:
        
        client = boto3.client('sesv2', region_name='us-east-2')

        template_data = {
            "professional_name": "Dr. Silva",
            "area": "Cardiologia",
            "paciente_name": "João",
            "paciente_phone": "5511999999999",
            "price_min": "100",
            "price_max": "200"
        }

        response = client.send_email(
            FromEmailAddress='no-reply@orgmetamorfosepro.com.br',
            Destination={
                'ToAddresses': ['gustavo_honda@usp.br'],
            },
            Content={
                'Template': {
                    'TemplateName': 'metamorfose_template_v1',
                    'TemplateData': json.dumps(template_data)
                }
            }
        )

        print(response)

    def send_batch(self,df)-> None:
        print(df.columns)
        df = df.reset_index(drop=True)
        for  index, row in df.iterrows():
            self.send_msg(row)
            print(f"{index + 1} de {len(df)} mensagens enviadas")
        print("Sent all messages")

def create_template():
    client = boto3.client('sesv2')
    response = client.create_email_template(
        TemplateName='metamorfose_template_v1',
        TemplateContent={
            'Subject': 'Olá, {{professional_name}}!',
            'Text': '''Olá {{professional_name}}, tudo bem? Sou a Inteligência Artificial da Rede MetAMORfose, você assinou conosco como profissional da área de {{area}}, e estou programada para promover suas conexões com pacientes. Temos um guia de como conversar com paciente em orgmetamorfose.com.br/manual-de-uso 

    Caso seja necessário suporte, acesse orgmetamorfose.com.br/suporte

    Entre em contato com este, que cadastrou buscar atendimento e consentiu ser conectado com você!

    👤Nome: {{paciete_name}}
    📞Contato: wa.me/{{paciente_phone}}
    💰Vocês definem o valor. Recomendamos que o paciente pague, direto para você, antes da teleconsulta!

    Obrigada por fazer parte da nossa Rede!.''',
            'Html': '''
            <html>
            <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
                <h2 style="color:#2c3e50;">Olá {{professional_name}}, tudo bem?</h2>
                <p>
                Sou a <strong>Inteligência Artificial da Rede MetAMORfose</strong>.  
                Você se cadastrou conosco como profissional da área de 
                <strong>{{area}}</strong>, e estou programada para promover suas conexões com pacientes.
                </p>
                <p>
                📘 Consulte nosso guia de comunicação:  
                <a href="https://orgmetamorfose.com.br/manual-de-uso" target="_blank">
                    orgmetamorfose.com.br/manual-de-uso
                </a>
                </p>
                <p>
                Caso precise de suporte:  
                <a href="https://orgmetamorfose.com.br/suporte" target="_blank">
                    orgmetamorfose.com.br/suporte
                </a>
                </p>
                <hr style="border: 1px solid #ddd; margin: 20px 0;">
                <h3>📩 Novo paciente interessado:</h3>
                <p><strong>👤 Nome:</strong> {{paciete_name}}<br>
                <strong>📞 Contato:</strong> <a href="https://wa.me/{{paciente_phone}}" target="_blank">wa.me/{{paciente_phone}}</a><br>
                <strong>💰 Observação:</strong> Vocês definem o valor. Recomendamos que o paciente pague diretamente para você antes da teleconsulta!
                </p>
                <hr style="border: 1px solid #ddd; margin: 20px 0;">
                <p style="font-size:14px; color:#555;">
                Obrigada por fazer parte da nossa Rede!  
                <br><em>Equipe MetAMORfose</em>
                </p>
            </body>
            </html>
            '''
        }
    )

    print("Template criado:", response)

if __name__ == '__main__':
    df = open_mock()
    sender = AWS_Sender()
    sender.send_msg("fdafas")
    # sender.send_batch(df)