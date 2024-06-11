from receivers.application.caching.interface import CacheClient


class CacheManager:
    def __init__(self, cache_client: CacheClient):
        self.cache_client = cache_client

    def get(self, key):
        return self.cache_client.get(key)

    def set(self, key, value, expiration=None):
        self.cache_client.set(key, value, expiration=expiration)
