from abc import ABC, abstractmethod


class CacheClient(ABC):
    @abstractmethod
    def get(self, key: str) -> any:
        raise NotImplementedError

    @abstractmethod
    def set(self, key: str, value: any, expiration: int = 10 * 60) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: str):
        raise NotImplementedError
