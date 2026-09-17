from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/health")
async def health() -> dict:
    return {"domain": "identity", "ok": True}