from dataclasses import dataclass
import datetime


@dataclass
class User:
    email: str
    password: str
    admin: bool = False
    id: int = None
    created_at: datetime.datetime = None