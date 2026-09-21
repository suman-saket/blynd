from datetime import date

from beanie import Document
from pymongo import ASCENDING, IndexModel

from src.identity.models.enums import DatingPreference, Gender, VerificationStatus
from src.identity.models.geo_point import GeoPoint


class User(Document):
    phone: str | None
    has_accepted_terms: bool
    is_age_verified: bool
    name: str | None
    date_of_birth: date | None
    gender: Gender | None
    preferences: list[DatingPreference]
    location: GeoPoint | None
    education: str | None
    occupation: str | None
    bio: str | None
    profile_completed: bool
    verification_selfie_url: str | None = None
    verification_status: VerificationStatus = VerificationStatus.NOT_SUBMITTED

    class Settings:
        name = "users"
        indexes = [
            IndexModel([("phone", ASCENDING)], unique=True, sparse=True),
            IndexModel([("location.latitude", ASCENDING)]),
            IndexModel([("location.longitude", ASCENDING)]),
        ]
