from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import AuthError, NotFoundError
from app.core.security import create_access_token, verify_password
from app.modules.auth.schemas import LoginResponse, UserResponse
from app.modules.users.models import User


def to_user_response(user: User) -> UserResponse:
    return UserResponse(id=user.id, username=user.username, isAdmin=user.is_admin)


def authenticate_user(db: Session, username: str, password: str) -> LoginResponse:
    user = db.scalar(select(User).where(User.username == username, User.is_active.is_(True)))
    if user is None or not verify_password(password, user.password_hash):
        raise AuthError("Invalid username or password")
    token = create_access_token(
        str(user.id),
        {"username": user.username, "is_admin": user.is_admin},
    )
    return LoginResponse(accessToken=token, user=to_user_response(user))


def get_user_by_id(db: Session, user_id: int) -> User:
    user = db.get(User, user_id)
    if user is None or not user.is_active:
        raise NotFoundError("User not found")
    return user
