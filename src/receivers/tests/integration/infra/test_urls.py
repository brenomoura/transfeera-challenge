import json
import os
import uuid
from typing import List

from django.test import TestCase
from ninja.testing import TestClient

from receivers.application.dtos import CreateReceiverIn, ReceiverOut
from receivers.domain.entities import ReceiverStatuses, PixKeyTypes
from receivers.infra.django_ninja_app.mappers import ReceiverModelMapper
from receivers.infra.django_ninja_app.models import ReceiverModel
from receivers.infra.django_ninja_app.urls import api
from receivers.tests.helpers import generate_pix, new_receiver_entity
from shared.domain.repositories import PAGE, PAGE_SIZE


class TestReceiversUrls(TestCase):

    def setUp(self):
        os.environ["NINJA_SKIP_REGISTRY"] = "yes"
        self.client = TestClient(api)

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
    def _check_receiver_existence_in_db(receiver_ids: List[uuid.UUID] | str) -> bool:
        return ReceiverModel.objects.filter(id__in=receiver_ids).exists()

    def tearDown(self):
        del os.environ['NINJA_SKIP_REGISTRY']

    def test_create_receiver(self):
        data = CreateReceiverIn.from_entity(new_receiver_entity()).dict()
        response = self.client.post("/receivers/", json=data)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self._check_receiver_existence_in_db([response_data["id"]])
        self.assertTrue(set(data.items()).issubset(set(response_data.items())))

    def test_create_receiver_invalid_fields(self):
        data = {
            "name": [1],
            "cpf_cnpj": "1231",
            "email": "random@",
            "pix_key_type": "non_existent_pix_key_type",
            "pix_key": "random_pix_value"
        }
        response = self.client.post("/receivers/", json=data)
        self.assertEqual(response.status_code, 422)
        response_data = response.json()["detail"]
        expected_errors_message = [
            'Input should be a valid string',
            'Value error, Formato de CPF ou CNPJ inválido',
            'Value error, Formato de E-mail inválido',
            "Input should be 'CPF', 'CNPJ', 'EMAIL', 'TELEFONE' or 'CHAVE_ALEATORIA'",
        ]
        for response_data_item in response_data:
            assert response_data_item["msg"] in expected_errors_message

    def test_create_receiver_already_registred_cpf(self):
        receiver_model = self._create_receiver_in_db()
        data = CreateReceiverIn.from_entity(new_receiver_entity()).dict()
        data["cpf_cnpj"] = receiver_model.cpf_cnpj
        response = self.client.post("/receivers/", json=data)
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertEqual(response_data["msg"], 'CPF/CNPJ ou E-mail já registrado')

    def test_create_receiver_already_registred_email(self):
        receiver_model = self._create_receiver_in_db()
        data = CreateReceiverIn.from_entity(new_receiver_entity()).dict()
        data["email"] = receiver_model.email
        response = self.client.post("/receivers/", json=data)
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertEqual(response_data["msg"], 'CPF/CNPJ ou E-mail já registrado')

    def test_retrieve_receivers(self):
        receivers_quantity = 20
        for _ in range(receivers_quantity):
            self._create_receiver_in_db()
        response = self.client.get("/receivers/")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["page"], PAGE)
        self.assertEqual(response_data["page_size"], PAGE_SIZE)
        self.assertEqual(response_data["items_count"], receivers_quantity)
        self.assertEqual(len(response_data["results"]), PAGE_SIZE)

    def test_retrieve_receivers_different_page(self):
        receivers_quantity = 20
        for _ in range(receivers_quantity):
            self._create_receiver_in_db()
        page = 2
        response = self.client.get(f"/receivers/?page={page}")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["page"], page)
        self.assertEqual(response_data["page_size"], PAGE_SIZE)
        self.assertEqual(response_data["items_count"], receivers_quantity)
        self.assertEqual(len(response_data["results"]), PAGE_SIZE)

    def test_retrieve_receivers_different_page_size(self):
        receivers_quantity = 20
        for _ in range(receivers_quantity):
            self._create_receiver_in_db()
        response = self.client.get(f"/receivers/?page_size={receivers_quantity}")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["page"], PAGE)
        self.assertEqual(response_data["page_size"], receivers_quantity)
        self.assertEqual(response_data["items_count"], receivers_quantity)
        self.assertEqual(len(response_data["results"]), receivers_quantity)

    def test_retrieve_receivers_filter_by_status(self):
        receivers_quantity = 5
        for _ in range(receivers_quantity):
            self._create_receiver_in_db()
        # create one as validated, to allow us to test the query params
        status_filter = ReceiverStatuses.VALIDATED
        self._create_receiver_in_db(status=status_filter)
        response = self.client.get(f"/receivers/?search={status_filter.value}")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["page"], PAGE)
        self.assertEqual(response_data["page_size"], PAGE_SIZE)
        self.assertEqual(response_data["items_count"], 1)
        self.assertEqual(len(response_data["results"]), 1)

    def test_retrieve_receivers_filter_by_name(self):
        receivers_quantity = 5
        for _ in range(receivers_quantity):
            self._create_receiver_in_db()
        # create one as validated, to allow us to test the query params
        receiver_model = self._create_receiver_in_db()
        response = self.client.get(f"/receivers/?search={receiver_model.name}")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["page"], PAGE)
        self.assertEqual(response_data["page_size"], PAGE_SIZE)
        self.assertEqual(response_data["items_count"], 1)
        self.assertEqual(len(response_data["results"]), 1)

    def test_retrieve_receivers_filter_by_pix_key_type(self):
        receivers_quantity = 5
        for _ in range(receivers_quantity):
            self._create_receiver_in_db()
        # create one as validated, to allow us to test the query params
        receiver_model = self._create_receiver_in_db(pix_key_type=PixKeyTypes.CHAVE_ALEATORIA)
        response = self.client.get(f"/receivers/?search={receiver_model.pix_key_type}")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["page"], PAGE)
        self.assertEqual(response_data["page_size"], PAGE_SIZE)
        self.assertEqual(response_data["items_count"], 1)
        self.assertEqual(len(response_data["results"]), 1)

    def test_retrieve_receivers_filter_by_pix_key_value(self):
        receivers_quantity = 5
        for _ in range(receivers_quantity):
            self._create_receiver_in_db()
        # create one as validated, to allow us to test the query params
        receiver_model = self._create_receiver_in_db(pix_key_type=PixKeyTypes.EMAIL)
        response = self.client.get(f"/receivers/?search={receiver_model.pix_key}")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["page"], PAGE)
        self.assertEqual(response_data["page_size"], PAGE_SIZE)
        self.assertEqual(response_data["items_count"], 1)
        self.assertEqual(len(response_data["results"]), 1)

    def test_retrieve_receiver_detail(self):
        receiver_model = self._create_receiver_in_db()
        response = self.client.get(f"/receivers/{receiver_model.id}/")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertDictEqual(
            response_data,
            json.loads(ReceiverOut.from_entity(ReceiverModelMapper.to_entity(receiver_model)).json())
        )

    def test_retrieve_receiver_detail_not_found(self):
        response = self.client.get(f"/receivers/{uuid.uuid4()}/")
        self.assertEqual(response.status_code, 404)

    def test_update_receiver(self):
        receiver_model = self._create_receiver_in_db()
        data = CreateReceiverIn.from_entity(new_receiver_entity()).dict()
        response = self.client.patch(f"/receivers/{receiver_model.id}/", json=data)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(set(data.items()).issubset(set(response_data.items())))

    def test_update_receiver_invalid_fields(self):
        receiver_model = self._create_receiver_in_db(status=ReceiverStatuses.DRAFT)
        data = {
            "name": [1],
            "cpf_cnpj": "1231",
            "email": "random@",
            "pix_key_type": "non_existent_pix_key_type",
            "pix_key": "random_pix_value"
        }
        response = self.client.patch(f"/receivers/{receiver_model.id}/", json=data)
        self.assertEqual(response.status_code, 422)
        response_data = response.json()["detail"]
        expected_errors_message = [
            'Input should be a valid string',
            'Value error, Formato de CPF ou CNPJ inválido',
            'Value error, Formato de E-mail inválido',
            "Input should be 'CPF', 'CNPJ', 'EMAIL', 'TELEFONE' or 'CHAVE_ALEATORIA'",
        ]
        for response_data_item in response_data:
            assert response_data_item["msg"] in expected_errors_message

    def test_delete_receivers(self):
        receiver_model_ids = []
        for _ in range(2):
            receiver_model = self._create_receiver_in_db()
            receiver_model_ids.append(str(receiver_model.id))
        data = {
            "ids": receiver_model_ids
        }
        response = self.client.post(f"/receivers/delete-multiple/", json=data)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(receiver_model_ids), response_data["deleted_count"])
        self.assertFalse(self._check_receiver_existence_in_db(receiver_model_ids))

    def test_delete_empty_ids(self):
        receiver_model_ids = []
        data = {
            "ids": receiver_model_ids
        }
        response = self.client.post(f"/receivers/delete-multiple/", json=data)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(receiver_model_ids), response_data["deleted_count"])
