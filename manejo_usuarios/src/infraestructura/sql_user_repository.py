from sqlalchemy.orm import Session
from dominio.user import User
from infraestructura.models import UserModel

class SQLUserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str):
        return self.db.query(UserModel).filter_by(email=email).first()

    def save(self, user: User):
        user_db = UserModel(
            id=user.id,
            name=user.name,
            email=user.email,
            hashed_password=user.hashed_password,
            created_at=user.created_at
        )
        self.db.add(user_db)
        self.db.commit()
        self.db.refresh(user_db)
        return user_db
