from dataclasses import dataclass, field
import uuid

@dataclass
class Entidad:
    id: uuid.UUID = field(default_factory=uuid.uuid4)