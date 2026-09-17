from fastapi import APIRouter

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/health")
async def health() -> dict:
    return {"domain": "profiles", "ok": True}