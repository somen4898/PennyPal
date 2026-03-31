from datetime import datetime, timedelta

import bcrypt
from jose import JWTError, jwt

from src.domain.ports.auth_provider import AuthProvider


class JwtAuthProvider(AuthProvider):
    def __init__(self, secret_key: str, algorithm: str = "HS256", expire_minutes: int = 30) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._expire_minutes = expire_minutes

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

    def create_access_token(self, subject: str) -> str:
        expire = datetime.utcnow() + timedelta(minutes=self._expire_minutes)
        to_encode = {"sub": subject, "exp": expire}
        return jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)

    def verify_token(self, token: str) -> str | None:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            subject: str | None = payload.get("sub")
            return subject
        except JWTError:
            return None
