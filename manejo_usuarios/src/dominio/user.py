from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    id: str
    name: str
    email: str
    hashed_password: str
    created_at: datetime
    updated_at: Optional[datetime] = None
