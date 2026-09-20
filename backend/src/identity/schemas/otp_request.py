from pydantic import BaseModel


class OtpRequest(BaseModel):
    phone: str


class OtpRequestResponse(BaseModel):
    ok: bool
    otp: str | None
