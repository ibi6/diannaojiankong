from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db_session
from app.core.security import hash_password
from app.main import app
from app.modules.users.models import User  # noqa: F401 - needed for metadata
from app.modules.resumes.models import Resume, ResumeVersion  # noqa: F401 - needed for metadata


def override_database():
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


def login(client):
    response = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    return response.json()["data"]["accessToken"]


def test_resume_crud_flow(client):
    app.dependency_overrides[get_db_session] = override_database()
    try:
        token = login(client)
        headers = {"Authorization": f"Bearer {token}"}

        create_response = client.post(
            "/api/resumes",
            headers=headers,
            json={"title": "My Resume", "templateKey": "classic"},
        )
        assert create_response.status_code == 200
        resume = create_response.json()["data"]
        assert resume["title"] == "My Resume"
        assert resume["templateKey"] == "classic"
        resume_id = resume["id"]

        list_response = client.get("/api/resumes", headers=headers)
        assert list_response.status_code == 200
        assert len(list_response.json()["data"]["items"]) == 1

        update_response = client.put(
            f"/api/resumes/{resume_id}",
            headers=headers,
            json={
                "title": "Updated Resume",
                "templateKey": "minimal",
                "content": {"basics": {"name": "Ada"}},
                "layout": {"sections": ["basics"]},
            },
        )
        assert update_response.status_code == 200
        assert update_response.json()["data"]["title"] == "Updated Resume"

        version_response = client.post(f"/api/resumes/{resume_id}/versions", headers=headers)
        assert version_response.status_code == 200
        assert version_response.json()["data"]["versionNumber"] == 1

        delete_response = client.delete(f"/api/resumes/{resume_id}", headers=headers)
        assert delete_response.status_code == 200

        empty_list_response = client.get("/api/resumes", headers=headers)
        assert empty_list_response.json()["data"]["items"] == []
    finally:
        app.dependency_overrides.clear()
