from fastapi.testclient import TestClient
import faker
from app.main import app

client = TestClient(app)
fake = faker.Faker()

client.fake_user_email = fake.email()
client.fake_user_password = fake.password()
client.fake_user_name = fake.user_name()
client.fake_user_real_name = fake.name()
client.new_user_id = 0
client.auth_token = ""


def test_signup():
    response = client.post("/auth/register",
                           params={"user_name": client.fake_user_name,
                                   "real_name": client.fake_user_name,
                                   "email": client.fake_user_email,
                                   "password": client.fake_user_password,
                                   })
    assert response.status_code == 201
    client.new_user_id = response.json()["user_id"]


def test_login():
    response = client.post("/auth/login",
                           params={"username": client.fake_user_name,
                                   "password": client.fake_user_password})
    assert response.status_code == 200
    client.auth_token = response.json()['access_token']


def test_me():
    response = client.get("/auth/active_user",
                          params={"token": client.auth_token})
    assert response.status_code == 200
    assert response.json()["id"] == client.new_user_id
