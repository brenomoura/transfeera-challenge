import base64
import uuid
from typing import List, Tuple

from receivers.application.caching.handler import CacheManager
from receivers.application.dtos import (
    CreateReceiverOut,
    CreateReceiverIn,
    UpdateReceiverIn,
    UpdateReceiverOut,
    ReceiverOut,
    DeleteReceiverOut,
    DeleteReceiversIn,
)
from receivers.domain.entities import ReceiverStatuses
from receivers.domain.repositories import ReceiverRepository, ReceiverSearchParams


class ReceiverService:
    def __init__(self, repo: ReceiverRepository, cache: CacheManager):
        self.repo = repo
        self.cache = cache

    def create(self, create_receiver_data: CreateReceiverIn) -> CreateReceiverOut:
        receiver = self.repo.create(create_receiver_data.to_entity())
        return CreateReceiverOut.from_entity(receiver)

    def get(self, receiver_id: uuid.UUID) -> ReceiverOut:
        receiver = self.cache.get(receiver_id)
        if receiver is None:
            receiver = self.repo.get_by_id(receiver_id)
            self.cache.set(receiver_id, receiver)
        return ReceiverOut.from_entity(receiver)

    def update(
        self, receiver_id: uuid.UUID, update_receiver_data: UpdateReceiverIn
    ) -> UpdateReceiverOut:
        receiver = self.repo.get_by_id(receiver_id)
        if receiver.status == ReceiverStatuses.VALIDATED:
            receiver = self.repo.update_email_by_id(
                receiver_id, update_receiver_data.email
            )
        else:
            receiver = self.repo.update_by_id(
                receiver_id, update_receiver_data.to_entity()
            )
        return UpdateReceiverOut.from_entity(receiver)

    def delete(self, delete_data: DeleteReceiversIn) -> DeleteReceiverOut:
        deleted_count = self.repo.bulk_delete_by_id(delete_data.ids)
        return DeleteReceiverOut(deleted_count=deleted_count)

    def list(
        self, search_params: ReceiverSearchParams
    ) -> Tuple[List[ReceiverOut], int]:
        cache_id = search_params.base64_encode()
        cached_receivers = self.cache.get(cache_id)
        if not cached_receivers:
            receivers, items_count = self.repo.list(search_params)
            self.cache.set(cache_id, (receivers, items_count))
        else:
            receivers, items_count = cached_receivers
        return [
            ReceiverOut.from_entity(receiver) for receiver in receivers
        ], items_count
