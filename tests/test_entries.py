from fastapi.testclient import TestClient
import faker
import random
from app.config import settings
from app.main import app
from app.schemas import EntryStatus

# use with statement to trigger lifespan
with TestClient(app) as client:
    fake = faker.Faker()

    client.fake_user_email = fake.email()
    client.fake_user_password = fake.password()
    client.fake_user_name = fake.user_name()
    client.fake_user_real_name = fake.name()
    client.new_user_id = 0
    client.user_token = ""
    client.admin_token = ""

    client.fake_book_title = "Book Title One"
    client.fake_book_author = fake.name()
    client.fake_book_year = int(random.uniform(1700, 2025))

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
        client.user_token = response.json()['access_token']

    def test_admin_login():
        response = client.post(
            "/auth/login",
            params={"username": settings.admin_username,
                    "password": settings.admin_password})
        assert response.status_code == 200
        client.admin_token = response.json()['access_token']

    def test_add_book():
        response = client.post("/books",
                               params={"token": client.admin_token,
                                       "title": client.fake_book_title,
                                       "author": client.fake_book_author,
                                       "year": client.fake_book_year})
        assert response.status_code == 201
        client.fake_book_id = response.json()["book_id"]

    def test_add_entries():
        response = client.post("/entries",
                               params={"token": client.admin_token,
                                       "status": EntryStatus.READING,
                                       "score": 10,
                                       "review": None,
                                       "book_id": client.fake_book_id})
        assert response.status_code == 201
        response = client.post("/entries",
                               params={"token": client.user_token,
                                       "status": EntryStatus.READ,
                                       "score": 5,
                                       "review": "great",
                                       "book_id": client.fake_book_id})
        assert response.status_code == 201

    def test_stats():
        response = client.get(f"/books/stats/{client.fake_book_id}")
        assert response.status_code == 200
        assert response.json()["mean_score"] == (10 + 5) / 2
        assert response.json()["entries"] == 2
        assert response.json()["reading"] == 1
        assert response.json()["read"] == 1
        assert response.json()["dropped"] == 0
