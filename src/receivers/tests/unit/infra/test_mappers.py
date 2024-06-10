import pytest

from receivers.domain.entities import Receiver
from receivers.infra.django_ninja_app.mappers import ReceiverModelMapper, LoadEntityException, LoadModelException
from receivers.infra.django_ninja_app.models import ReceiverModel
from receivers.tests.fixtures import receiver, receiver_model


def test_receiver_mapper_model_to_entity(receiver_model):
    receiver_entity = ReceiverModelMapper.to_entity(receiver_model)
    assert isinstance(receiver_entity, Receiver)
    assert receiver_entity.id == receiver_model.id
    assert receiver_entity.name == receiver_model.name
    assert receiver_entity.email == receiver_model.email
    assert receiver_entity.cpf_cnpj == receiver_model.cpf_cnpj
    assert receiver_entity.status == receiver_model.status
    assert receiver_entity.pix.pix_key_type == receiver_model.pix_key_type
    assert receiver_entity.pix.pix_key == receiver_model.pix_key


def test_receiver_mapper_model_to_entity_exception(receiver_model):
    with pytest.raises(LoadEntityException):
        ReceiverModelMapper.to_entity("TEST")


def test_receiver_mapper_entity_to_model(receiver):
    receiver_model = ReceiverModelMapper.to_model(receiver)
    assert isinstance(receiver_model, ReceiverModel)
    assert receiver_model.id == receiver.id
    assert receiver_model.name == receiver.name
    assert receiver_model.email == receiver.email
    assert receiver_model.cpf_cnpj == receiver.cpf_cnpj
    assert receiver_model.status == receiver.status
    assert receiver_model.pix_key_type == receiver.pix.pix_key_type
    assert receiver_model.pix_key == receiver.pix.pix_key


def test_receiver_mapper_entity_to_model_exception(receiver_model):
    with pytest.raises(LoadModelException):
        ReceiverModelMapper.to_model("TEST")

