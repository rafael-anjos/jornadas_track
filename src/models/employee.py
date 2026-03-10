from dataclasses import dataclass, field
from models.journey import Journey

@dataclass
class Employee:
    cpf:         str
    name:        str
    nightWorker: bool
    journeys:    list[Journey] = field(default_factory=list)
