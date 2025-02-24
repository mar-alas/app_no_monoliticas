from abc import ABC, abstractmethod
from .user import User
from typing import Optional

class UserRepository(ABC):
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def save(self, user: User) -> None:
        pass
