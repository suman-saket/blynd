from fastapi import APIRouter, HTTPException

from src.profiles.exceptions import ProfileAlreadyCompleted, UserNotFound
from src.profiles.schemas.profile_create import ProfileCreate, ProfileResponse
from src.profiles.services.profile import complete_profile

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/health")
async def health() -> dict:
    return {"domain": "profiles", "ok": True}


@router.post("/create", response_model=ProfileResponse)
async def create_profile(profile: ProfileCreate) -> ProfileResponse:
    try:
        return await complete_profile(profile)
    except UserNotFound as error:
        raise HTTPException(status_code=404, detail="user not found") from error
    except ProfileAlreadyCompleted as error:
        raise HTTPException(status_code=409, detail="profile already completed") from error