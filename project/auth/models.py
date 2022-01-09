from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class User:

    id: Optional[int] = field(None)
    username: str
    email: str 
    password: str
    created: datetime
    last_login: Optional[datetime] = None