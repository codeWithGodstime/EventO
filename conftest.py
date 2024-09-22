import pytest

from app.main import app
from app.models.models import User, Event
from config.database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.utils import hash_password
from datetime import date, time, datetime

from faker import Faker

faker = Faker()

# Set up an in-memory SQLite database
DATABASE_URL = "sqlite:///sqlite.sqlite3"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
TestSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)

@pytest.fixture(scope="function")
def test_db():

    # Create the database tables before each test
    Base.metadata.create_all(bind=engine)

    session = TestSession()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def client(test_db):
    app.dependency_overrides[get_db] = lambda: test_db

    client = TestClient(app)
    yield client
    # clean up overrides
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def user(test_db):
    _hash_password = hash_password("timetokill")
    user = User(
        username=faker.user_name(),
        email=faker.email(),
        password=_hash_password,
        phone_number=_hash_password
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user

@pytest.fixture(scope="function")
def organizer(test_db):
    _hash_password = hash_password("timetokill")
    user = User(
        username=faker.user_name(),
        email=faker.email(),
        password=_hash_password,
        phone_number=_hash_password,
        is_organizer=True
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user

@pytest.fixture(scope="function")
def organizer_token(client, user):
    response = client.post("/auth/token", json={"email": user.email, "password": "timetokill"})
    token = response.json().get("access_token")
    
    return token

@pytest.fixture(scope="function")
def event(test_db, user):
    event = Event(
        title="Sample Event Title",
        description="Sample event description",
        max_participants=50,
        location="uyo",
        date=date.today(),  # Use the current date
        time=datetime.now().time(),  # Use the current time
        organiser=user.id
    )
    
    test_db.add(event)
    test_db.commit()
    test_db.refresh(event)

    return event