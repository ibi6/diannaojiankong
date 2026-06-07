from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db_session
from app.core.security import hash_password
from app.main import app
from app.modules.users.models import User  # noqa: F401 - needed for metadata


def override_database():
    # Use StaticPool to ensure all connections share the same in-memory database
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    db.add(User(username="admin", password_hash=hash_password("admin123"), is_admin=True))
    db.commit()
    db.close()

    def _get_db():
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    return _get_db


def test_login_and_me(client):
    app.dependency_overrides[get_db_session] = override_database()
    try:
        login_response = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "admin123"},
        )
        assert login_response.status_code == 200
        body = login_response.json()
        assert body["success"] is True
        token = body["data"]["accessToken"]

        me_response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert me_response.status_code == 200
        assert me_response.json()["data"]["username"] == "admin"
        assert me_response.json()["data"]["isAdmin"] is True
    finally:
        app.dependency_overrides.clear()


def test_login_rejects_bad_password(client):
    app.dependency_overrides[get_db_session] = override_database()
    try:
        response = client.post(
            "/api/auth/login",
            json={"username": "admin", "password": "wrong"},
        )
        assert response.status_code == 401
        assert response.json()["success"] is False
    finally:
        app.dependency_overrides.clear()
