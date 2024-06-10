from anydi import Module, provider

from api.receivers.application.services import ReceiverService
from api.receivers.domain.repositories import ReceiverRepository
from api.receivers.infra.django_ninja_app.repositories import \
    ReceiverDjangoRepository


class ReceiverModule(Module):
    @provider(scope="singleton")
    def receiver_repository(self) -> ReceiverRepository:
        return ReceiverDjangoRepository()

    @provider(scope="singleton")
    def receiver_service(self, receiver_repository: ReceiverRepository) -> ReceiverService:
        return ReceiverService(repo=receiver_repository)
