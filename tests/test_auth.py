from fastapi.testclient import TestClient
import os
import faker
from app.config import settings
settings.db_path = "test.db"  # settings ignores .env file in test dir
from app.main import app  # noqa: E402

if os.path.exists(settings.db_path):
    os.remove(settings.db_path)

# use with statement to trigger lifespan
with TestClient(app) as client:
    fake = faker.Faker()

    client.fake_user_email = fake.email()
    client.fake_user_password = fake.password()
    client.fake_user_name = fake.user_name()
    client.fake_user_real_name = fake.name()
    client.new_user_id = 0
    client.auth_token = ""

    def test_signup():
        response = client.post(
            "/auth/register",
            params={"user_name": client.fake_user_name,
                    "real_name": client.fake_user_real_name,
                    "email": client.fake_user_email,
                    "password": client.fake_user_password,
                    })
        assert response.status_code == 201
        client.new_user_id = response.json()["user_id"]

    def test_login():
        response = client.post(
            "/auth/login",
            params={"username": client.fake_user_name,
                    "password": client.fake_user_password})
        assert response.status_code == 200
        client.auth_token = response.json()['access_token']

    def test_me():
        response = client.get("/auth/active_user",
                              params={"token": client.auth_token})
        assert response.status_code == 200
        assert response.json()["id"] == client.new_user_id

    def test_delete():
        response = client.delete("auth/active_user",
                                 params={"token": client.auth_token})
        assert response.status_code == 202

    def test_teapot():
        if " " not in client.fake_user_real_name:
            client.fake_user_real_name += " "
        response = client.post(
            "/auth/register",
            params={"user_name": client.fake_user_real_name,
                    "real_name": client.fake_user_real_name,
                    "email": client.fake_user_email,
                    "password": client.fake_user_password,
                    })
        assert response.status_code == 418

    def test_admin_signup():
        response = client.post(
            "/auth/login",
            params={"username": settings.admin_username,
                    "password": settings.admin_password})
        assert response.status_code == 200
        client.admin_token = response.json()['access_token']

    def test_admin_is_moderator():
        response = client.get("auth/active_user",
                              params={"token": client.admin_token})
        assert response.status_code == 200
        assert response.json()["is_moderator"] == True
