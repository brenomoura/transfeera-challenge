from anydi import Module, provider

from receivers.application.caching.handler import CacheManager
from receivers.application.caching.interface import CacheClient
from receivers.application.services import ReceiverService
from receivers.domain.repositories import ReceiverRepository
from receivers.infra.django_ninja_app.cache_client import CacheDjangoClient
from receivers.infra.django_ninja_app.repositories import ReceiverDjangoRepository


class ReceiverModule(Module):
    @provider(scope="singleton")
    def receiver_repository(self) -> ReceiverRepository:
        return ReceiverDjangoRepository()

    @provider(scope="singleton")
    def cache_manager(self) -> CacheManager:
        cache_client = CacheDjangoClient()
        return CacheManager(cache_client=cache_client)

    @provider(scope="singleton")
    def receiver_service(
            self,
            receiver_repository: ReceiverRepository,
            cache_manager: CacheManager
    ) -> ReceiverService:
        return ReceiverService(repo=receiver_repository, cache=cache_manager)
