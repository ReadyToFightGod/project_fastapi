import os
from app.config import settings
settings.db_path = "test.db"  # settings ignores .env file in test dir


def pytest_sessionstart(session):
    print("A A A A A")
    if os.path.exists(settings.db_path):
        os.remove(settings.db_path)
