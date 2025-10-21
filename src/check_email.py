import re
import dns.resolver

def validate_email(email: str) -> dict:
    """
    Valida um endereço de e-mail verificando:
    1. Formato sintático (regex)
    2. Existência do domínio
    3. Presença de registros MX (servidores de e-mail)
    Retorna um dicionário com o status e a causa.
    """

    # 1. Verificação de formato
    email_regex = re.compile(
        r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    )
    if not email_regex.match(email):
        return {
            "email": email,
            "valid": False,
            "reason": "Formato inválido"
        }

    # 2. Verificação de domínio
    domain = email.split('@')[1]
    try:
        dns.resolver.resolve(domain, 'A')
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
        return {
            "email": email,
            "valid": False,
            "reason": f"Domínio inexistente ({domain})"
        }

    # 3. Verificação de registros MX
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        if not mx_records:
            return {
                "email": email,
                "valid": False,
                "reason": "Sem registro MX"
            }
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
        return {
            "email": email,
            "valid": False,
            "reason": "Erro ao buscar MX"
        }

    # Se passou em todas as etapas
    return {
        "email": email,
        "valid": True,
        "reason": "E-mail válido"
    }

# Exemplo de uso
if __name__ == "__main__":
    emails = [
        "riello@yahoo.com.br",
        "pkriello@yahoo.com.br",
    ]

    for e in emails:
        print(validate_email(e))
