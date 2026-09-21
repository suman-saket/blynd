from enum import StrEnum


class Gender(StrEnum):
    MALE = "male"
    FEMALE = "female"
    TRANSGENDER = "transgender"
    NON_BINARY = "non_binary"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class DatingPreference(StrEnum):
    MEN = "men"
    WOMEN = "women"
    TRANSGENDER = "transgender"
    NON_BINARY = "non_binary"
    EVERYONE = "everyone"


class VerificationStatus(StrEnum):
    NOT_SUBMITTED = "not_submitted"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"
