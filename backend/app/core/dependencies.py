from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.core.exceptions import AuthError
from app.core.security import decode_access_token
from app.modules.auth.service import get_user_by_id
from app.modules.users.models import User

DbSession = Annotated[Session, Depends(get_db_session)]
_bearer = HTTPBearer(auto_error=False)


def get_current_user(
    db: DbSession,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
) -> User:
    if credentials is None:
        raise AuthError()
    try:
        payload = decode_access_token(credentials.credentials)
        user_id = int(payload["sub"])
    except (KeyError, ValueError, jwt.PyJWTError) as exc:
        raise AuthError("Invalid authentication token") from exc
    return get_user_by_id(db, user_id)


CurrentUser = Annotated[User, Depends(get_current_user)]
