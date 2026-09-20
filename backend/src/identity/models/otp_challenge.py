from datetime import datetime

from beanie import Document
from pymongo import ASCENDING, IndexModel


class OtpChallenge(Document):
    phone: str
    code_hash: str
    expires_at: datetime
    consumed: bool

    class Settings:
        name = "otp_challenges"
        indexes = [
            IndexModel([("phone", ASCENDING)]),
        ]
