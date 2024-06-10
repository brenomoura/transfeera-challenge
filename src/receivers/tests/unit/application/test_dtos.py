from receivers.application.dtos import BaseReceiver, BaseReceiverOut
from receivers.domain.entities import Receiver
from receivers.tests.fixtures import receiver, base_receiver


def test_create_base_receiver_object_from_entity(receiver):
    base_receiver_obj = BaseReceiver.from_entity(receiver)
    assert isinstance(base_receiver_obj, BaseReceiver)
    assert base_receiver_obj.name == receiver.name
    assert base_receiver_obj.cpf_cnpj == receiver.cpf_cnpj
    assert base_receiver_obj.email == receiver.email
    assert base_receiver_obj.pix_key_type == receiver.pix.pix_key_type
    assert base_receiver_obj.pix_key == receiver.pix.pix_key


def test_create_receiver_entity_to_entity(base_receiver):
    receiver_entity = base_receiver.to_entity()
    assert isinstance(receiver_entity, Receiver)
    assert receiver_entity.name == base_receiver.name
    assert receiver_entity.cpf_cnpj == base_receiver.cpf_cnpj
    assert receiver_entity.email == base_receiver.email
    assert receiver_entity.pix.pix_key_type == base_receiver.pix_key_type
    assert receiver_entity.pix.pix_key == base_receiver.pix_key


def test_create_base_receiver_out_from_entity(receiver):
    base_receiver_out_obj = BaseReceiverOut.from_entity(receiver)
    assert isinstance(base_receiver_out_obj, BaseReceiverOut)
    assert base_receiver_out_obj.id == receiver.id
    assert base_receiver_out_obj.name == receiver.name
    assert base_receiver_out_obj.cpf_cnpj == receiver.cpf_cnpj
    assert base_receiver_out_obj.email == receiver.email
    assert base_receiver_out_obj.status == receiver.status
    assert base_receiver_out_obj.pix_key_type == receiver.pix.pix_key_type
    assert base_receiver_out_obj.pix_key == receiver.pix.pix_key
