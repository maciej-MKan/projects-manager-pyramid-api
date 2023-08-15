from datetime import datetime

from pydantic import BaseModel


class Comment(BaseModel):
    id: int = None
    project: int = None
    author: int = None
    description: str
    date: datetime

    class Config:
        orm_mode = True

    def get_json(self):
        return self.json()
