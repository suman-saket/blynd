from datetime import date, datetime, timezone

MINIMUM_PROFILE_AGE_YEARS = 18


def age_check_reference_date() -> date:
    return datetime.now(timezone.utc).date()


def age_in_years(date_of_birth: date, on_date: date) -> int:
    """Full years elapsed from date_of_birth through on_date (birthday-aware)."""
    years = on_date.year - date_of_birth.year
    birthday_not_yet = (on_date.month, on_date.day) < (
        date_of_birth.month,
        date_of_birth.day,
    )
    if birthday_not_yet:
        return years - 1
    return years


def validate_profile_date_of_birth(date_of_birth: date) -> None:
    """Raise ValueError when DOB is invalid for profile completion (18+ gate)."""
    today = age_check_reference_date()
    if date_of_birth > today:
        raise ValueError("date_of_birth cannot be in the future")
    age = age_in_years(date_of_birth, today)
    if age < MINIMUM_PROFILE_AGE_YEARS:
        raise ValueError("must be at least 18 years old")
