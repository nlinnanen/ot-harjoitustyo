from dataclasses import dataclass
import datetime


@dataclass
class Member:
    id: int
    first_name: str
    last_name: str
    start_year: int
    member_until: datetime.date
    home_municipality: str
    user_id: int
    created_at: datetime.datetime

    def get_full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
    
