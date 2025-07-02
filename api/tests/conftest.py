import pytest
from auth import get_current_player, get_password_hash
from database import Base, get_db
from fastapi.testclient import TestClient
from main import app
from models import Player
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

TEST_DATABASE_URL = "sqlite:///./test.db"  # Using SQLite for testing
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
db = TestingSessionLocal()


@pytest.fixture(scope="session")
def client():
    yield TestClient(app)


def get_tests_db():
    try:
        yield db
    finally:
        db.close()


async def get_mock_current_player():
    return db.query(Player).filter(Player.id == 1).first()


app.dependency_overrides[get_current_player] = get_mock_current_player
app.dependency_overrides[get_db] = get_tests_db


def get_or_create_player():
    # Attempt to get the player
    player = db.query(Player).filter(Player.id == 1).first()

    if not player:
        # If not found, create the player
        player = Player(id=1, name="test_user", password=get_password_hash("password"))
        db.add(player)
        db.commit()

    return player
