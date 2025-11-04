"""
pytestフィクスチャ定義
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.main import app


@pytest.fixture
def db() -> Session:
    """データベースセッションフィクスチャ"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client() -> TestClient:
    """FastAPI TestClientフィクスチャ"""
    return TestClient(app)
