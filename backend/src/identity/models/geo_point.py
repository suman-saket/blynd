from pydantic import BaseModel, field_validator


class GeoPoint(BaseModel):
    """User location as WGS-84 latitude/longitude (stored on the user document)."""

    latitude: float
    longitude: float

    @field_validator("latitude")
    @classmethod
    def latitude_in_range(cls, value: float) -> float:
        if value < -90.0 or value > 90.0:
            raise ValueError("latitude must be between -90 and 90")
        return value

    @field_validator("longitude")
    @classmethod
    def longitude_in_range(cls, value: float) -> float:
        if value < -180.0 or value > 180.0:
            raise ValueError("longitude must be between -180 and 180")
        return value
