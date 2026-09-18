from pydantic import BaseModel
from datetime import date

class ProfileCreate(BaseModel):
    user_id: str
    name: str
    date_of_birth: date
    gender: str
    preferences: list[str]
    location: str
    education: str
    work: str
    bio: str | None



class ProfileResponse(BaseModel):
    id: str
    user_id: str
    name: str
    date_of_birth: date
    gender: str
    preferences: list[str]
    location: str
    education: str
    work: str
    bio: str | None