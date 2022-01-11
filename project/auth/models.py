from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int
    username: str
    email: str 
    password: str
    fname: str
    lname: str
    address: str
    created_on: datetime
    debt: int
