from fastapi import APIRouter, HTTPException
from src.core.config import settings
from src.identity.config import LOCAL_ENVIRONMENT_NAME
from src.identity.exceptions import AgeNotVerified, InvalidOtp, TermsNotAccepted
from src.identity.schemas import AuthResponse, OtpRequest, OtpRequestResponse, OtpVerify
from src.identity.services import request_otp, verify_otp

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/health")
async def health() -> dict:
    return {"domain": "identity", "ok": True}


@router.post("/otp/request", response_model=OtpRequestResponse)
async def otp_request(body: OtpRequest) -> OtpRequestResponse:
    include_otp = settings.ENVIRONMENT == LOCAL_ENVIRONMENT_NAME
    return await request_otp(body.phone, include_otp)


@router.post("/otp/verify", response_model=AuthResponse)
async def otp_verify(body: OtpVerify) -> AuthResponse:
    try:
        return await verify_otp(
            body.phone,
            body.otp,
            body.has_accepted_terms,
            body.is_age_verified,
        )
    except InvalidOtp as error:
        raise HTTPException(status_code=401, detail="invalid or expired otp") from error
    except TermsNotAccepted as error:
        raise HTTPException(status_code=400, detail="terms must be accepted") from error
    except AgeNotVerified as error:
        raise HTTPException(status_code=400, detail="age must be verified") from error
