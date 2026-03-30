from abc import ABC, abstractmethod


class AuthProvider(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str: ...

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool: ...

    @abstractmethod
    def create_access_token(self, subject: str) -> str: ...

    @abstractmethod
    def verify_token(self, token: str) -> str | None: ...
