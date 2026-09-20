import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from src.identity.config import OTP_LENGTH, OTP_TTL_SECONDS
from src.identity.exceptions import AgeNotVerified, InvalidOtp, TermsNotAccepted
from src.identity.models.otp_challenge import OtpChallenge
from src.identity.models.user import User
from src.identity.schemas.auth_response import AuthResponse
from src.identity.schemas.otp_request import OtpRequestResponse


def generate_otp(length: int) -> str:
    """Return a numeric code with leading zeros preserved."""
    upper_bound = 10**length
    value = secrets.randbelow(upper_bound)
    return str(value).zfill(length)


def hash_otp(phone: str, otp: str) -> str:
    """Bind the code to this phone so a hash cannot be reused on another number."""
    payload = f"{phone}:{otp}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


async def request_otp(phone: str, include_otp: bool) -> OtpRequestResponse:
    """Replace any prior code for this phone so only the latest OTP can be verified."""
    normalized_phone = phone.strip()
    otp = generate_otp(OTP_LENGTH)
    # Mongo stores these as naive UTC, so expiry checks must use naive UTC too.
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    expires_at = now + timedelta(seconds=OTP_TTL_SECONDS)

    await OtpChallenge.find(OtpChallenge.phone == normalized_phone).delete()
    challenge = OtpChallenge(
        phone=normalized_phone,
        code_hash=hash_otp(normalized_phone, otp),
        expires_at=expires_at,
        consumed=False,
    )
    await challenge.insert()

    response_otp = otp if include_otp else None
    return OtpRequestResponse(ok=True, otp=response_otp)


async def verify_otp(
    phone: str,
    otp: str,
    has_accepted_terms: bool,
    is_age_verified: bool,
) -> AuthResponse:
    """Signup if this phone is new; login if a user already exists."""
    normalized_phone = phone.strip()
    challenge = await load_valid_challenge(normalized_phone, otp)
    user = await User.find_one(User.phone == normalized_phone)
    if user is None:
        ensure_signup_allowed(has_accepted_terms, is_age_verified)
    await consume_challenge(challenge)
    if user is None:
        user = await insert_user_from_otp(
            normalized_phone,
            has_accepted_terms,
            is_age_verified,
        )

    return AuthResponse(
        user_id=str(user.id),
        profile_completed=user.profile_completed,
    )


async def load_valid_challenge(phone: str, otp: str) -> OtpChallenge:
    # Naive UTC matches how request_otp stores expires_at in Mongo.
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    challenge = await OtpChallenge.find_one(
        OtpChallenge.phone == phone,
        OtpChallenge.code_hash == hash_otp(phone, otp),
        OtpChallenge.consumed == False,
        OtpChallenge.expires_at > now,
    )
    if challenge is None:
        raise InvalidOtp()
    return challenge


async def consume_challenge(challenge: OtpChallenge) -> None:
    challenge.consumed = True
    await challenge.save()


def ensure_signup_allowed(has_accepted_terms: bool, is_age_verified: bool) -> None:
    if not has_accepted_terms:
        raise TermsNotAccepted()
    if not is_age_verified:
        raise AgeNotVerified()


async def insert_user_from_otp(
    phone: str,
    has_accepted_terms: bool,
    is_age_verified: bool,
) -> User:
    user = User(
        phone=phone,
        has_accepted_terms=has_accepted_terms,
        is_age_verified=is_age_verified,
        name=None,
        date_of_birth=None,
        gender=None,
        preferences=[],
        location=None,
        education=None,
        work=None,
        bio=None,
        profile_completed=False,
    )
    await user.insert()
    return user
