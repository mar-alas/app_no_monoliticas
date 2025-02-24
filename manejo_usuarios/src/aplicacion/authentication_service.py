from dominio.user_repository import UserRepository
from dominio.user import User
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError
import uuid
from datetime import datetime

class AuthenticationService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, name: str, email: str, password: str):
        existing_user = self.user_repository.get_by_email(email)
        if existing_user:
            raise ValueError("El usuario ya está registrado.")

        hashed_password = generate_password_hash(password)
        new_user = User(
            id=str(uuid.uuid4()),
            name=name,
            email=email,
            hashed_password=hashed_password,
            created_at=datetime.utcnow()
        )

        try:
            self.user_repository.add(new_user)
            return {"message": "Usuario registrado exitosamente"}
        except IntegrityError:
            raise ValueError("Error al registrar usuario, posiblemente duplicado.")

    def authenticate_user(self, email: str, password: str):
        user = self.user_repository.get_by_email(email)
        if user and check_password_hash(user.hashed_password, password):
            return user
        return None
