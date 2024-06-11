from django.core.cache import cache

from receivers.application.caching.interface import CacheClient


class CacheDjangoClient(CacheClient):

    def get(self, key: str) -> any:
        value = cache.get(key)
        return value

    def set(self, key: str, value: any, expiration: int = 10 * 60) -> None:
        cache.set(key, value, expiration)

    def delete(self, key: str):
        cache.delete(key)
