from dataclasses import dataclass
import datetime
from typing import Optional


@dataclass
class Member:
    first_name: str
    last_name: str
    start_year: int
    member_until: datetime.date
    home_municipality: str
    user_id: Optional[int] = None
    id: Optional[int] = None
    created_at: Optional[datetime.datetime] = None

    def get_full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'
