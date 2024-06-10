import uuid
from typing import List, Tuple

from api.receivers.application.dtos import CreateReceiverOut, \
    CreateReceiverIn, UpdateReceiverIn, UpdateReceiverOut, ReceiverOut, \
    DeleteReceiverOut, DeleteReceiversIn
from api.receivers.domain.entities import ReceiverStatuses
from api.receivers.domain.repositories import ReceiverRepository, \
    ReceiverSearchParams


class ReceiverService:

    def __init__(self, repo: ReceiverRepository):
        self.repo = repo

    def create(self,create_receiver_data: CreateReceiverIn) -> CreateReceiverOut:
        receiver = self.repo.create(create_receiver_data.to_entity())
        return CreateReceiverOut.from_entity(receiver)

    def get(self, receiver_id: uuid.UUID) -> ReceiverOut:
        receiver = self.repo.get_by_id(receiver_id)
        return ReceiverOut.from_entity(receiver)

    def update(self, receiver_id: uuid.UUID,
               update_receiver_data: UpdateReceiverIn) -> UpdateReceiverOut:
        receiver = self.repo.get_by_id(receiver_id)
        if receiver.status == ReceiverStatuses.VALIDATED:
            receiver = self.repo.update_email_by_id(receiver_id,
                                                    update_receiver_data.email)
        else:
            receiver = self.repo.update_by_id(receiver_id,
                                              update_receiver_data.to_entity())
        return UpdateReceiverOut.from_entity(receiver)

    def delete(self, delete_data: DeleteReceiversIn) -> DeleteReceiverOut:
        deleted_count = self.repo.bulk_delete_by_id(
            delete_data.ids)
        return DeleteReceiverOut(deleted_count=deleted_count)

    def list(self, search_params: ReceiverSearchParams) -> Tuple[List[ReceiverOut], int]:
        receivers, items_count = self.repo.list(search_params)
        return [ReceiverOut.from_entity(receiver) for receiver in receivers], items_count
