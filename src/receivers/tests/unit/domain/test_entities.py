import pytest
from pydantic import ValidationError

from receivers.domain.entities import ReceiverPIX, Receiver
from receivers.tests.sample_values import VALID_CPF_LIST


# ReceiverPIX


def test_invalid_pix_key_receiver_pix():
    with pytest.raises(ValidationError):
        ReceiverPIX(
            pix_key_type="NON_EXISTING_PIX_KEY_TYPE", pix_key="RANDOM_PIX_VALUE"
        )


# Receiver
def test_invalid_status_receiver():
    with pytest.raises(ValidationError):
        Receiver(
            name="Random Name",
            cpf_cnpj=VALID_CPF_LIST[0],
            email="TEST@TEST.CM",
            status="RANDOM_STATUS",
            pix=ReceiverPIX(pix_key_type="EMAIL", pix_key="TEST@TEST.CM"),
        )
