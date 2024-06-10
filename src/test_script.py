import random
import re
import string
import time
import uuid
from pprint import pprint

import requests


def generate_cpf():
    cpf = [random.randint(0, 9) for x in range(9)]

    for _ in range(2):
        val = sum([(len(cpf) + 1 - i) * v for i, v in enumerate(cpf)]) % 11

        cpf.append(11 - val if val > 1 else 0)

    return '%s%s%s.%s%s%s.%s%s%s-%s%s' % tuple(cpf)


def generate_cnpj():
    def calculate_special_digit(l):
        digit = 0

        for i, v in enumerate(l):
            digit += v * (i % 8 + 2)

        digit = 11 - digit % 11

        return digit if digit < 10 else 0

    cnpj = [1, 0, 0, 0] + [random.randint(0, 9) for x in range(8)]

    for _ in range(2):
        cnpj = [calculate_special_digit(cnpj)] + cnpj

    return '%s%s.%s%s%s.%s%s%s/%s%s%s%s-%s%s' % tuple(cnpj[::-1])


def generate_random_phone_number() -> str:
    # Definir o regex para validação
    pattern = re.compile(r'^((?:\+?55)?)([1-9][0-9])(9[0-9]{8})$')

    while True:
        # Gerar código do país (opcional)
        country_code = random.choice(['', '+55', '55'])

        # Gerar DDD (10 a 99)
        ddd = f"{random.randint(1, 9)}{random.randint(0, 9)}"

        # Gerar número de celular (9 seguido de 8 dígitos)
        number = '9' + ''.join(str(random.randint(0, 9)) for _ in range(8))

        phone_number = f"{country_code}{ddd}{number}"

        # Verifica se o número gerado corresponde ao regex
        if pattern.match(phone_number):
            return phone_number


def generate_random_uuid() -> str:
    def random_hex(length: int) -> str:
        return ''.join(random.choices(string.hexdigits.lower(), k=length))

    # Gerar partes do UUID
    part1 = random_hex(8)
    part2 = random_hex(4)
    part3 = random_hex(4)
    part4 = random_hex(4)
    part5 = random_hex(12)

    # Combinar partes com hífens
    uuid = f"{part1}-{part2}-{part3}-{part4}-{part5}"

    return uuid


def create_receiver(
        name,
        email,
        cpf_cnpj,
        pix_key,
        pix_key_type,
):
    data = {
        "name": name,
        "email": email,
        "cpf_cnpj": cpf_cnpj,
        "pix_key": pix_key,
        "pix_key_type": pix_key_type,
    }
    response = requests.post("http://127.0.0.1:8000/api/receivers", json=data)
    if response.status_code in [201, 400, 422]:
        pprint(response.json())


if __name__ == "__main__":
    for i in range(1):
        email = f"TEST.NAME{time.time()}@HAHAHA.COM"
        pixes = [
            ("CPF", generate_cpf()),
            ("CNPJ", generate_cnpj()),
            ("EMAIL", email),
            ("TELEFONE", generate_random_phone_number()),
            ("CHAVE_ALEATORIA", generate_random_uuid()),
        ]
        selected_pix = random.choice(pixes)
        create_receiver(
            f"Test Name {uuid.uuid4()}",
            email,
            random.choice([generate_cnpj, generate_cpf])(),
            selected_pix[1],
            selected_pix[0],
        )
