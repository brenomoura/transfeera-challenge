import uuid
from typing import List, Tuple

from django.db.models import F, CharField
from django.db.models.functions import Concat
from django.db.utils import IntegrityError
from django.forms import model_to_dict

from receivers.domain.entities import Receiver
from receivers.domain.repositories import ReceiverRepository, ReceiverSearchParams
from receivers.infra.django_ninja_app.mappers import ReceiverModelMapper
from receivers.infra.django_ninja_app.models import ReceiverModel


class NotFoundException(Exception): ...


class AlreadyRegisteredReceiver(Exception): ...


class ReceiverDjangoRepository(ReceiverRepository):
    def __init__(self):
        self.model = ReceiverModel

    def _get(self, receiver_id: uuid.UUID) -> ReceiverModel:
        try:
            receiver_model = self.model.objects.get(id=receiver_id)
        except self.model.DoesNotExist:
            raise NotFoundException
        return receiver_model

    def get_by_id(self, receiver_id: uuid.UUID) -> Receiver:
        """
        Get Receiver By its ID
        """
        receiver_model = self._get(receiver_id)
        return ReceiverModelMapper.to_entity(receiver_model)

    def create(self, receiver: Receiver) -> Receiver:
        """
        Create a Receiver
        """
        try:
            receiver_model = ReceiverModelMapper.to_model(receiver)
            receiver_model.save()
            return ReceiverModelMapper.to_entity(receiver_model)
        except IntegrityError:
            raise AlreadyRegisteredReceiver

    def update_by_id(self, receiver_id: uuid.UUID, receiver: Receiver) -> Receiver:
        """
        Update the whole receiver according to the provided values in the receiver entity
        """
        receiver_model = self._get(receiver_id)
        updated_model_dict = model_to_dict(ReceiverModelMapper.to_model(receiver))
        for k, v in updated_model_dict.items():
            setattr(receiver_model, k, v)
        receiver_model.save()
        return receiver

    def update_email_by_id(self, receiver_id: uuid.UUID, new_email: str) -> Receiver:
        """
        Only update the receiver email
        """
        receiver_model = self._get(receiver_id)
        receiver_model.email = new_email
        receiver_model.save()
        return ReceiverModelMapper.to_entity(receiver_model)

    def bulk_delete_by_id(self, ids: List[uuid.UUID]) -> int:
        """
        Delete the receivers by providing their ids
        """
        deleted_count, _ = self.model.objects.filter(id__in=ids).delete()
        return deleted_count

    def list(self, search_params: ReceiverSearchParams) -> Tuple[List[Receiver], int]:
        """
        Retrieve a paginated list of receivers
        """
        start_index = (search_params.page - 1) * search_params.page_size
        final_index = start_index + search_params.page_size
        receivers_qs = self.model.objects.all().order_by("name")
        if search_params.search:
            receivers_qs = receivers_qs.filter(
                _search_field__contains=search_params.search
            )
        receivers_models = receivers_qs[start_index:final_index]
        return [
            ReceiverModelMapper.to_entity(receiver_model)
            for receiver_model in list(receivers_models)
        ], receivers_qs.count()
