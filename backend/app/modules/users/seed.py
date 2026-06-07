from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.users.models import User


def seed_default_admin(db: Session) -> None:
    existing = db.scalar(select(User).where(User.username == "admin"))
    if existing is not None:
        return
    db.add(User(username="admin", password_hash=hash_password("admin123"), is_admin=True))
    db.commit()
