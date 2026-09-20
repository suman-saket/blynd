from pydantic import BaseModel


class OtpVerify(BaseModel):
    phone: str
    otp: str
    has_accepted_terms: bool
    is_age_verified: bool
