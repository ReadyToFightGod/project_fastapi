from fastapi.testclient import TestClient
import faker
import random
from app.config import settings
from app.main import app

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

    def test_add_book_authorized():
        response = client.post("/books",
                               params={"token": client.admin_token,
                                       "title": client.fake_book_title,
                                       "author": client.fake_book_author,
                                       "year": client.fake_book_year})
        assert response.status_code == 201
        client.fake_book_id = response.json()["book_id"]

    def test_add_book_unauthorized():
        response = client.post("/books",
                               params={"token": client.user_token,
                                       "title": client.fake_book_title,
                                       "author": client.fake_book_author,
                                       "year": client.fake_book_year})
        assert response.status_code == 403

    def test_get_book_test():
        response = client.get(f"/books/{client.fake_book_id}")
        assert response.status_code == 200
        assert response.json()["title"] == client.fake_book_title
        assert response.json()["id"] == client.fake_book_id

    def test_delete_book():
        response = client.delete(f"/books/{client.fake_book_id}",
                                 params={"token": client.admin_token})
        assert response.status_code == 202

    def test_book_deleted():
        response = client.get(f"/books/{client.fake_book_id}")
        assert response.status_code == 404
