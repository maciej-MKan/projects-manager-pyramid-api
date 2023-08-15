from typing import List

from pydantic import BaseModel

from backend.src.business.models.DTOProject import Project


class User(BaseModel):
    id: int = None
    name: str
    surname: str
    password: str = None
    age: int = None
    gender: str = None
    email: str
    phone_number: int = None
    # projects: list = None

    class Config:
        orm_mode = True

    def get_json(self):
        return self.json()


class UserCreate(User):
    projects: List[Project]
