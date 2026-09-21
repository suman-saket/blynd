from datetime import date

from pydantic import BaseModel, Field, field_validator

from src.identity.models.enums import DatingPreference, Gender
from src.identity.models.geo_point import GeoPoint
from src.profiles.validation.date_of_birth import validate_profile_date_of_birth


class ProfileCreate(BaseModel):
    user_id: str
    name: str
    date_of_birth: date
    gender: Gender
    preferences: list[DatingPreference] = Field(min_length=1)
    location: GeoPoint
    education: str
    occupation: str
    bio: str | None

    @field_validator("date_of_birth")
    @classmethod
    def date_of_birth_is_valid(cls, value: date) -> date:
        validate_profile_date_of_birth(value)
        return value

    @field_validator("name")
    @classmethod
    def name_is_non_empty(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("name cannot be empty")
        return stripped


class ProfileResponse(BaseModel):
    id: str
    user_id: str
    name: str
    date_of_birth: date
    gender: Gender
    preferences: list[DatingPreference]
    location: GeoPoint
    education: str
    occupation: str
    bio: str | None
