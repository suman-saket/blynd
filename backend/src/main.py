from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import close_db, init_db
from src.identity.router import router as identity_router
from src.profiles.router import router as profiles_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(title="Dating App", lifespan=lifespan)
app.include_router(identity_router)
app.include_router(profiles_router)


@app.get("/")
async def root() -> dict:
    return {"ok": True, "docs": "/docs", "auth_health": "/auth/health"}