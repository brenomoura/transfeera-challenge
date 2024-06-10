import string
import time
import uuid
import random

from pycpfcnpj import gen

from receivers.application.dtos import BaseReceiver
from receivers.domain.entities import Receiver, ReceiverPIX, ReceiverStatuses, PixKeyTypes
from receivers.infra.django_ninja_app.models import ReceiverModel


def generate_random_email():
    return f"TEST.{time.time()}@TEST.CM"


def generate_random_name():
    return f"Random Name {time.time()}"


def generate_random_phone_number():
    country_code = random.choice(['', '+55', '55'])
    ddd = f"{random.randint(1, 9)}{random.randint(0, 9)}"
    number = '9' + ''.join(str(random.randint(0, 9)) for _ in range(8))
    return f"{country_code}{ddd}{number}"


def generate_random_pix_random_key() -> str:
    def random_hex(length: int) -> str:
        return ''.join(random.choices(string.hexdigits.lower(), k=length))
    part1 = random_hex(8)
    part2 = random_hex(4)
    part3 = random_hex(4)
    part4 = random_hex(4)
    part5 = random_hex(12)
    return f"{part1}-{part2}-{part3}-{part4}-{part5}"


def new_receiver_entity():
    return Receiver(
        id=uuid.uuid4(),
        name=generate_random_name(),
        cpf_cnpj=gen.cpf(),
        email=generate_random_email(),
        status=ReceiverStatuses.DRAFT,
        pix=ReceiverPIX(
            pix_key_type=PixKeyTypes.EMAIL,
            pix_key=generate_random_email(),
        ))


def new_receiver_model():
    return ReceiverModel(
        name=generate_random_name(),
        cpf_cnpj=gen.cnpj(),
        email=generate_random_email(),
        status=ReceiverStatuses.DRAFT,
        pix_key_type=PixKeyTypes.EMAIL,
        pix_key=generate_random_email(),
    )


def new_base_model():
    return BaseReceiver(
        name=generate_random_name(),
        cpf_cnpj=gen.cpf(),
        email=generate_random_email(),
        pix_key_type=PixKeyTypes.EMAIL,
        pix_key=generate_random_email(),
    )


def generate_pix(pix_key_type: PixKeyTypes):
    pix_value_generator = {
        "CPF": gen.cpf(),
        "CNPJ": gen.cnpj(),
        "EMAIL": generate_random_email(),
        "TELEFONE": generate_random_phone_number(),
        "CHAVE_ALEATORIA": generate_random_pix_random_key(),
    }
    if pix_key_type not in pix_value_generator:
        raise ValueError("error during pix generation")
    return ReceiverPIX(
        pix_key_type=pix_key_type,
        pix_key=pix_value_generator[pix_key_type]
    )
