from bson.errors import InvalidId
from bson.objectid import ObjectId

from src.identity.models import User
from src.profiles.exceptions import ProfileAlreadyCompleted, UserNotFound
from src.profiles.schemas import ProfileCreate, ProfileResponse


async def complete_profile(body: ProfileCreate) -> ProfileResponse:
    """Fill profile fields on the existing users document (not a second collection)."""
    try:
        object_id = ObjectId(body.user_id)
    except InvalidId as error:
        raise UserNotFound() from error

    user = await User.get(object_id)
    if user is None:
        raise UserNotFound()
    if user.profile_completed:
        raise ProfileAlreadyCompleted()

    user.name = body.name
    user.date_of_birth = body.date_of_birth
    user.gender = body.gender
    user.preferences = body.preferences
    user.location = body.location
    user.education = body.education
    user.work = body.work
    user.bio = body.bio
    user.profile_completed = True
    await user.save()

    return ProfileResponse(
        id=str(user.id),
        user_id=str(user.id),
        name=user.name,
        date_of_birth=user.date_of_birth,
        gender=user.gender,
        preferences=user.preferences,
        location=user.location,
        education=user.education,
        work=user.work,
        bio=user.bio,
    )