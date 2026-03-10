from dataclasses import dataclass
from datetime import datetime
from typing import Any

from models.stats import Stats


@dataclass
class Journey:
    date:       Any
    status:     str
    status_raw: str
    start:      datetime | None
    end:        datetime | None
    total:      float
    daily:      bool
    inter:      float
    plate:      str
    tracker:    str
    group:      str
    vehicle:    str
    manobrista: bool
    stats:      Stats
