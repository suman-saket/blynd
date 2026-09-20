from datetime import date

from beanie import Document
from pymongo import ASCENDING, IndexModel


class User(Document):
    phone: str | None
    has_accepted_terms: bool
    is_age_verified: bool

    name: str | None
    date_of_birth: date | None
    gender: str | None
    preferences: list[str]
    location: str | None
    education: str | None
    work: str | None
    bio: str | None
    profile_completed: bool

    class Settings:
        name = "users"
        indexes = [
            IndexModel([("phone", ASCENDING)], unique=True, sparse=True),
        ]