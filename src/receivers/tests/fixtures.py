import uuid

import pytest

from receivers.application.dtos import BaseReceiver
from receivers.domain.entities import Receiver, ReceiverPIX, ReceiverStatuses, PixKeyTypes
from receivers.infra.django_ninja_app.models import ReceiverModel


@pytest.fixture
def receiver():
    return Receiver(
        id=uuid.uuid4(),
        name="Random Name",
        cpf_cnpj="012.355.010-60",
        email="TEST@TEST.CM",
        status=ReceiverStatuses.DRAFT,
        pix=ReceiverPIX(
            pix_key_type=PixKeyTypes.EMAIL,
            pix_key="TEST@TEST.CM"
        ))


@pytest.fixture
def receiver_model():
    return ReceiverModel(
        name="Random Name",
        cpf_cnpj="012.355.010-60",
        email="TEST@TEST.CM",
        status=ReceiverStatuses.DRAFT,
        pix_key_type=PixKeyTypes.EMAIL,
        pix_key="TEST@TEST.CM"
    )


@pytest.fixture
def base_receiver():
    return BaseReceiver(
        name="Random Name",
        cpf_cnpj="012.355.010-60",
        email="TEST@TEST.CM",
        pix_key_type=PixKeyTypes.EMAIL,
        pix_key="TEST@TEST.CM"
    )
