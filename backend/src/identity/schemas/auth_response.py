from pydantic import BaseModel


class AuthResponse(BaseModel):
    user_id: str
    profile_completed: bool
