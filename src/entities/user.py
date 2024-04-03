from dataclasses import dataclass
import datetime
from typing import Optional


@dataclass
class User:
    id: int
    email: str
    password: str
    admin: bool
    created_at: datetime.datetime