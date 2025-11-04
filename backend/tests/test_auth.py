"""
認証API統合テスト
テスト対象:
- POST /api/auth/register
- POST /api/auth/login
- POST /api/auth/logout
- GET /api/auth/me
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.session import Base, get_db
from app.main import app
from app.models import RefreshToken, User

# テスト用データベース（.env.localと同じデータベースを使用）
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """テスト用DBセッション"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup_test_users():
    """各テスト後にテストユーザーを削除"""
    yield
    # テスト用ユーザーを削除
    db = TestingSessionLocal()
    try:
        db.query(RefreshToken).filter(
            RefreshToken.user_id.in_(
                db.query(User.id).filter(User.email.like("test_%@example.com"))
            )
        ).delete(synchronize_session=False)
        db.query(User).filter(User.email.like("test_%@example.com")).delete()
        db.commit()
    finally:
        db.close()


# ==================== 新規登録テスト ====================


def test_register_success():
    """新規登録成功"""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test_register@example.com",
            "password": "SecurePass2025!",
        },
    )

    assert response.status_code == 201
    data = response.json()

    # トークンが発行されている
    assert "accessToken" in data
    assert "refreshToken" in data
    assert data["accessToken"] != ""
    assert data["refreshToken"] != ""

    # ユーザー情報が正しい
    assert data["user"]["email"] == "test_register@example.com"
    assert data["user"]["role"] == "user"
    assert data["user"]["profile"]["name"] == "test_register"
    assert data["user"]["permissions"] == ["read", "write"]


def test_register_duplicate_email():
    """メールアドレス重複エラー"""
    # 1回目の登録
    client.post(
        "/api/auth/register",
        json={
            "email": "test_duplicate@example.com",
            "password": "SecurePass2025!",
        },
    )

    # 2回目の登録（同じメールアドレス）
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test_duplicate@example.com",
            "password": "AnotherPass2025!",
        },
    )

    assert response.status_code == 409
    assert "既に登録されています" in response.json()["detail"]


def test_register_short_password():
    """パスワードが短すぎるエラー"""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test_short_password@example.com",
            "password": "short",  # 8文字未満
        },
    )

    assert response.status_code == 400
    assert "8文字以上" in response.json()["detail"]


# ==================== ログインテスト ====================


def test_login_success():
    """ログイン成功"""
    # まずユーザーを登録
    client.post(
        "/api/auth/register",
        json={
            "email": "test_login@example.com",
            "password": "SecurePass2025!",
        },
    )

    # ログイン
    response = client.post(
        "/api/auth/login",
        json={
            "email": "test_login@example.com",
            "password": "SecurePass2025!",
        },
    )

    assert response.status_code == 200
    data = response.json()

    # トークンが発行されている
    assert "accessToken" in data
    assert "refreshToken" in data
    assert data["accessToken"] != ""
    assert data["refreshToken"] != ""

    # ユーザー情報が正しい
    assert data["user"]["email"] == "test_login@example.com"
    assert data["user"]["role"] == "user"


def test_login_wrong_email():
    """メールアドレスが存在しないエラー"""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "SecurePass2025!",
        },
    )

    assert response.status_code == 401
    assert "正しくありません" in response.json()["detail"]


def test_login_wrong_password():
    """パスワードが間違っているエラー"""
    # まずユーザーを登録
    client.post(
        "/api/auth/register",
        json={
            "email": "test_wrong_password@example.com",
            "password": "CorrectPass2025!",
        },
    )

    # 間違ったパスワードでログイン
    response = client.post(
        "/api/auth/login",
        json={
            "email": "test_wrong_password@example.com",
            "password": "WrongPass2025!",
        },
    )

    assert response.status_code == 401
    assert "正しくありません" in response.json()["detail"]


# ==================== 現在のユーザー情報取得テスト ====================


def test_get_me_success():
    """現在のユーザー情報取得成功"""
    # まずユーザーを登録してトークン取得
    register_response = client.post(
        "/api/auth/register",
        json={
            "email": "test_me@example.com",
            "password": "SecurePass2025!",
        },
    )
    access_token = register_response.json()["accessToken"]

    # トークンを使ってユーザー情報取得
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["email"] == "test_me@example.com"
    assert data["role"] == "user"
    assert data["profile"]["name"] == "test_me"
    assert data["permissions"] == ["read", "write"]


def test_get_me_no_token():
    """トークンなしでエラー"""
    response = client.get("/api/auth/me")

    assert response.status_code == 403  # HTTPBearer requires Authorization header


def test_get_me_invalid_token():
    """無効なトークンでエラー"""
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer invalid_token_here"},
    )

    assert response.status_code == 401
    assert "認証が必要です" in response.json()["detail"]


# ==================== ログアウトテスト ====================


def test_logout_success():
    """ログアウト成功"""
    # まずユーザーを登録してトークン取得
    register_response = client.post(
        "/api/auth/register",
        json={
            "email": "test_logout@example.com",
            "password": "SecurePass2025!",
        },
    )
    access_token = register_response.json()["accessToken"]

    # ログアウト
    response = client.post(
        "/api/auth/logout",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["success"] is True
    assert "ログアウトしました" in data["message"]

    # ログアウト後はリフレッシュトークンが無効化されている
    db = TestingSessionLocal()
    try:
        user = db.query(User).filter(User.email == "test_logout@example.com").first()
        refresh_tokens = db.query(RefreshToken).filter(RefreshToken.user_id == user.id).all()
        assert all(token.is_revoked for token in refresh_tokens)
    finally:
        db.close()


def test_logout_no_token():
    """トークンなしでログアウトエラー"""
    response = client.post("/api/auth/logout")

    assert response.status_code == 403  # HTTPBearer requires Authorization header


# ==================== 統合テスト ====================


def test_full_auth_flow():
    """フルフロー: 登録 → ログアウト → ログイン → ユーザー情報取得"""
    email = "test_full_flow@example.com"
    password = "SecurePass2025!"

    # 1. 新規登録
    register_response = client.post(
        "/api/auth/register",
        json={"email": email, "password": password},
    )
    assert register_response.status_code == 201
    access_token_1 = register_response.json()["accessToken"]

    # 2. ログアウト
    logout_response = client.post(
        "/api/auth/logout",
        headers={"Authorization": f"Bearer {access_token_1}"},
    )
    assert logout_response.status_code == 200

    # 3. 再ログイン
    login_response = client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    assert login_response.status_code == 200
    access_token_2 = login_response.json()["accessToken"]

    # 4. ユーザー情報取得
    me_response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {access_token_2}"},
    )
    assert me_response.status_code == 200
    assert me_response.json()["email"] == email
