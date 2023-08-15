from datetime import datetime

from pydantic import BaseModel


class Project(BaseModel):
    id: int = None
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    status: str
    author: int
    users: list

    class Config:
        orm_mode = True

    def get_json(self):
        return self.json()
