from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass(kw_only=True)
class Post:

    id: Optional[int] = field(None)
    author_id: Optional[int] = field(None)
    created: datetime = None
    title: str
    body: str