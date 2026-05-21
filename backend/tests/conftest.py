import pytest
import sys
from collections.abc import Generator
from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.config import get_settings
from app.database import Base, get_db
from app.dependencies import get_current_user
from app.main import app

TEST_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/mavunoroute"
engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture(scope="session", autouse=True)
def ensure_tables() -> None:
    Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def _patch_rate_limits() -> None:
    settings = get_settings()
    settings.rate_limit_auth_per_minute = 1000
    settings.rate_limit_public_per_minute = 5000


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    original_commit = session.commit
    session.commit = session.flush
    yield session
    session.commit = original_commit
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(id=uuid4(), role="SUPER_ADMIN")
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides = {}


@pytest.fixture
def real_db_client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()
