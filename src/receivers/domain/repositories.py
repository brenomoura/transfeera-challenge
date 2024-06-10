import uuid
from abc import ABC, abstractmethod
from typing import Optional, List, Tuple

from receivers.domain.entities import Receiver
from shared.domain.repositories import SearchParams


class ReceiverSearchParams(SearchParams):
    search: Optional[str] = None


class ReceiverRepository(ABC):

    @abstractmethod
    def get_by_id(self, receiver_id: uuid.UUID) -> Receiver:
        raise NotImplementedError

    @abstractmethod
    def create(self, receiver: Receiver) -> Receiver:
        raise NotImplementedError

    @abstractmethod
    def update_by_id(self, receiver_id: uuid.UUID,
                     receiver: Receiver) -> Receiver:
        raise NotImplementedError

    @abstractmethod
    def update_email_by_id(self, receiver_id: uuid.UUID, new_email: str) -> Receiver:
        raise NotImplementedError

    @abstractmethod
    def bulk_delete_by_id(self, doc_ids: List[uuid.UUID]) -> int:
        raise NotImplementedError

    @abstractmethod
    def list(self, search_params: ReceiverSearchParams) -> Tuple[List[Receiver], int]:
        raise NotImplementedError
