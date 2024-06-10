import time
import uuid
from typing import List
from unittest import TestCase

from django.db.models import QuerySet
from pycpfcnpj import gen
import pytest

from receivers.application.dtos import CreateReceiverIn, CreateReceiverOut, ReceiverOut, UpdateReceiverIn, \
    UpdateReceiverOut, DeleteReceiversIn, DeleteReceiverOut
from receivers.application.services import ReceiverService
from receivers.domain.entities import ReceiverStatuses, PixKeyTypes
from receivers.domain.repositories import ReceiverSearchParams
from receivers.infra.django_ninja_app.mappers import ReceiverModelMapper
from receivers.infra.django_ninja_app.models import ReceiverModel
from receivers.infra.django_ninja_app.repositories import ReceiverDjangoRepository, NotFoundException
from receivers.tests.helpers import new_receiver_entity, generate_pix
from shared.domain.repositories import PAGE_SIZE


@pytest.mark.django_db
class TestReceiverService(TestCase):

    def setUp(self):
        self.repo = ReceiverDjangoRepository()
        self.service = ReceiverService(self.repo)

    @staticmethod
    def _create_receiver_in_db(status: ReceiverStatuses = None, pix_key_type: PixKeyTypes = None) -> ReceiverModel:
        receiver = new_receiver_entity()
        if status:
            receiver.status = status
        if pix_key_type:
            receiver.pix = generate_pix(pix_key_type)
        receiver = ReceiverModelMapper.to_model(receiver)
        receiver.save()
        return receiver

    @staticmethod
    def _check_receiver_existence_in_db(receiver_id: uuid.UUID) -> bool:
        return ReceiverModel.objects.filter(id__in=[receiver_id]).exists()

    @staticmethod
    def _retrieve_receivers_from_db_ordered_alphabetically(receiver_ids: List[uuid.UUID]) -> QuerySet:
        return ReceiverModel.objects.filter(id__in=receiver_ids).order_by("name")

    def test_receiver_service_create(self):
        receiver = new_receiver_entity()
        create_receiver_in = CreateReceiverIn.from_entity(receiver)
        created_receiver_out = self.service.create(create_receiver_in)
        self.assertTrue(isinstance(created_receiver_out, CreateReceiverOut))
        created_receiver = ReceiverModel.objects.get(id=created_receiver_out.id)
        self.assertEqual(created_receiver.name, receiver.name)
        self.assertEqual(created_receiver.email, receiver.email)
        self.assertEqual(created_receiver.cpf_cnpj, receiver.cpf_cnpj)
        self.assertEqual(created_receiver.pix_key_type, receiver.pix.pix_key_type)
        self.assertEqual(created_receiver.pix_key, receiver.pix.pix_key)
        self.assertEqual(created_receiver.status, receiver.status)

    def test_receiver_service_get(self):
        receiver_model = self._create_receiver_in_db()
        retrieved_receiver = self.service.get(receiver_model.id)
        self.assertTrue(isinstance(retrieved_receiver, ReceiverOut))
        self.assertEqual(retrieved_receiver.name, receiver_model.name)
        self.assertEqual(retrieved_receiver.email, receiver_model.email)
        self.assertEqual(retrieved_receiver.cpf_cnpj, receiver_model.cpf_cnpj)
        self.assertEqual(retrieved_receiver.pix_key_type, receiver_model.pix_key_type)
        self.assertEqual(retrieved_receiver.pix_key, receiver_model.pix_key)
        self.assertEqual(retrieved_receiver.status, receiver_model.status)

    def test_receiver_service_get_not_found(self):
        non_existing_receiver_id = uuid.uuid4()
        with pytest.raises(NotFoundException):
            self.service.get(non_existing_receiver_id)

    def test_receiver_service_update_draft_status(self):
        receiver_model = self._create_receiver_in_db(status=ReceiverStatuses.DRAFT)

        new_name = f"New Random Name {time.time()}"
        new_cpf = gen.cpf()
        new_email = f"NEW.EMAIL.{time.time()}@TEST.COM"
        new_pix_key_type = PixKeyTypes.CNPJ
        new_pix_key = gen.cnpj()
        update_receiver_data = UpdateReceiverIn(
            name=new_name,
            cpf_cnpj=new_cpf,
            email=new_email,
            pix_key_type=new_pix_key_type,
            pix_key=new_pix_key,
        )
        updated_receiver_out = self.service.update(receiver_model.id, update_receiver_data)
        self.assertTrue(isinstance(updated_receiver_out, UpdateReceiverOut))
        updated_receiver_model = ReceiverModel.objects.get(id=receiver_model.id)
        self.assertEqual(updated_receiver_model.name, new_name)
        self.assertEqual(updated_receiver_model.email, new_email)
        self.assertEqual(updated_receiver_model.cpf_cnpj, new_cpf)
        self.assertEqual(updated_receiver_model.pix_key_type, new_pix_key_type)
        self.assertEqual(updated_receiver_model.pix_key, new_pix_key)
        self.assertEqual(updated_receiver_model.status, ReceiverStatuses.DRAFT)

    def test_receiver_service_update_validated_status(self):
        receiver_model = self._create_receiver_in_db(status=ReceiverStatuses.VALIDATED)

        new_name = f"New Random Name {time.time()}"
        new_cpf = gen.cpf()
        new_email = f"NEW.EMAIL.{time.time()}@TEST.COM"
        new_pix_key_type = PixKeyTypes.CNPJ
        new_pix_key = gen.cnpj()
        update_receiver_data = UpdateReceiverIn(
            name=new_name,
            cpf_cnpj=new_cpf,
            email=new_email,
            pix_key_type=new_pix_key_type,
            pix_key=new_pix_key,
        )
        updated_receiver_out = self.service.update(receiver_model.id, update_receiver_data)
        self.assertTrue(isinstance(updated_receiver_out, UpdateReceiverOut))
        updated_receiver_model = ReceiverModel.objects.get(id=receiver_model.id)
        self.assertNotEqual(updated_receiver_model.name, new_name)
        self.assertEqual(updated_receiver_model.email, new_email)
        self.assertNotEqual(updated_receiver_model.cpf_cnpj, new_cpf)
        self.assertNotEqual(updated_receiver_model.pix_key_type, new_pix_key_type)
        self.assertNotEqual(updated_receiver_model.pix_key, new_pix_key)
        self.assertEqual(updated_receiver_model.status, ReceiverStatuses.VALIDATED)

    def test_receiver_service_update_not_found(self):
        non_existing_receiver_id = uuid.uuid4()
        with pytest.raises(NotFoundException):
            self.service.update(non_existing_receiver_id, UpdateReceiverIn.from_entity(new_receiver_entity()))

    def test_receiver_service_delete(self):
        receiver_model_1 = self._create_receiver_in_db()
        receiver_model_2 = self._create_receiver_in_db()
        receivers = [receiver_model_1.id, receiver_model_2.id]
        delete_data = DeleteReceiversIn(ids=receivers)
        delete_out = self.service.delete(delete_data)
        self.assertTrue(isinstance(delete_out, DeleteReceiverOut))
        self.assertEqual(delete_out.deleted_count, len(receivers))
        self.assertFalse(self._check_receiver_existence_in_db(receiver_model_1.id))
        self.assertFalse(self._check_receiver_existence_in_db(receiver_model_2.id))

    def test_receiver_service_delete_empty_id_list(self):
        delete_data = DeleteReceiversIn(ids=[])
        delete_out = self.service.delete(delete_data)
        self.assertTrue(isinstance(delete_out, DeleteReceiverOut))
        self.assertEqual(delete_out.deleted_count, 0)

    def test_receiver_service_list_default_query_params(self):
        receiver_model_id_list = []
        receiver_quantity = 20
        for _ in range(receiver_quantity):
            receiver_model = self._create_receiver_in_db()
            receiver_model_id_list.append(receiver_model.id)
        search_params = ReceiverSearchParams()
        receivers, items_count = self.service.list(search_params)
        self.assertEqual(len(receivers), PAGE_SIZE)
        self.assertEqual(items_count, receiver_quantity)
        receivers_model = self._retrieve_receivers_from_db_ordered_alphabetically(receiver_model_id_list)
        first_item, last_item = receivers_model.first(), receivers_model.last()
        retrieved_receivers_id_list = [receiver.id for receiver in receivers]
        # check if the first item from first page is inside the retrieved receivers from page 2
        self.assertIn(first_item.id, retrieved_receivers_id_list)
        # check if the second item from seconds page is inside the retrieved receivers from page 2
        self.assertNotIn(last_item.id, retrieved_receivers_id_list)

    def test_receiver_service_list_different_page(self):
        receiver_model_id_list = []
        receiver_quantity = 20
        for _ in range(receiver_quantity):
            receiver_model = self._create_receiver_in_db()
            receiver_model_id_list.append(receiver_model.id)
        search_params = ReceiverSearchParams(page=2)
        receivers, items_count = self.service.list(search_params)
        self.assertEqual(len(receivers), PAGE_SIZE)
        self.assertEqual(items_count, receiver_quantity)
        receivers_model = self._retrieve_receivers_from_db_ordered_alphabetically(receiver_model_id_list)
        first_item, last_item = receivers_model.first(), receivers_model.last()
        retrieved_receivers_id_list = [receiver.id for receiver in receivers]
        # check if the first item from first page is inside the retrieved receivers from page 2
        self.assertNotIn(first_item.id, retrieved_receivers_id_list)
        # check if the second item from seconds page is inside the retrieved receivers from page 2
        self.assertIn(last_item.id, retrieved_receivers_id_list)

    def test_receiver_service_list_different_page_size(self):
        receiver_quantity = 20
        for _ in range(receiver_quantity):
            self._create_receiver_in_db()
        search_params = ReceiverSearchParams(page_size=receiver_quantity)
        receivers, items_count = self.service.list(search_params)
        self.assertEqual(len(receivers), receiver_quantity)
        self.assertEqual(items_count, receiver_quantity)

    def test_receiver_service_list_filter_by_status(self):
        receiver_quantity = 20
        for _ in range(receiver_quantity):
            self._create_receiver_in_db()
        # create one as validated, to allow us to test the filtering by status
        status_filter = ReceiverStatuses.VALIDATED
        receiver_model = self._create_receiver_in_db(status=status_filter)
        search_params = ReceiverSearchParams(search=status_filter)
        receivers, items_count = self.service.list(search_params)
        self.assertEqual(len(receivers), 1)
        self.assertEqual(items_count, 1)
        self.assertDictEqual(
            receivers[0].dict(),
            ReceiverOut.from_entity(ReceiverModelMapper.to_entity(receiver_model)).dict()
        )

    def test_receiver_service_list_filter_by_name(self):
        receiver_model_list = []
        receiver_quantity = 20
        for _ in range(receiver_quantity):
            receiver_model = self._create_receiver_in_db()
            receiver_model_list.append(self._create_receiver_in_db())
        # get one from the list to use as filter
        receiver_model_filter = receiver_model_list[11]
        name_filter = receiver_model_filter.name
        search_params = ReceiverSearchParams(search=name_filter)
        receivers, items_count = self.service.list(search_params)
        self.assertEqual(len(receivers), 1)
        self.assertEqual(items_count, 1)
        self.assertDictEqual(
            receivers[0].dict(),
            ReceiverOut.from_entity(ReceiverModelMapper.to_entity(receiver_model_filter)).dict()
        )

    def test_receiver_service_list_filter_by_pix_key_type(self):
        receiver_quantity = 20
        for _ in range(receiver_quantity):
            self._create_receiver_in_db()
        # create one with a different pix_key_type (RANDOM KEY), to allow us to test the filtering by status
        receiver_model = self._create_receiver_in_db(pix_key_type=PixKeyTypes.CHAVE_ALEATORIA)
        search_params = ReceiverSearchParams(search=receiver_model.pix_key_type)
        receivers, items_count = self.service.list(search_params)
        self.assertEqual(len(receivers), 1)
        self.assertEqual(items_count, 1)
        self.assertDictEqual(
            receivers[0].dict(),
            ReceiverOut.from_entity(ReceiverModelMapper.to_entity(receiver_model)).dict()
        )

    def test_receiver_service_list_filter_by_pix_key_value(self):
        receiver_quantity = 20
        for _ in range(receiver_quantity):
            self._create_receiver_in_db()
        # create one with a different pix_key_type (RANDOM KEY), to allow us to test the filtering by status
        receiver_model = self._create_receiver_in_db(pix_key_type=PixKeyTypes.CHAVE_ALEATORIA)
        search_params = ReceiverSearchParams(search=receiver_model.pix_key)
        receivers, items_count = self.service.list(search_params)
        self.assertEqual(len(receivers), 1)
        self.assertEqual(items_count, 1)
        self.assertDictEqual(
            receivers[0].dict(),
            ReceiverOut.from_entity(ReceiverModelMapper.to_entity(receiver_model)).dict()
        )


