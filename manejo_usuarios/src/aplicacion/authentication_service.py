from dominio.user import User
from dominio.user_repository import UserRepository
from hashlib import sha256
from uuid import uuid4
from datetime import datetime

class AuthenticationService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_user(self, name: str, email: str, password: str):
        hashed_password = sha256(password.encode()).hexdigest()
        new_user = User(
            id=str(uuid4()),
            name=name,
            email=email,
            hashed_password=hashed_password,
            created_at=datetime.utcnow()
        )
        self.user_repo.save(new_user)
        return new_user

    def authenticate_user(self, email: str, password: str):
        user = self.user_repo.get_by_email(email)
        if not user or user.hashed_password != sha256(password.encode()).hexdigest():
            return None
        return user
