"""
ユーザー設定APIテスト
PUT /api/user/password - パスワード変更
PUT /api/user/settings - ユーザー設定更新
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.auth import get_password_hash, verify_password
from app.main import app
from app.models import RefreshToken, User

client = TestClient(app)


# ==================== フィクスチャ ====================


@pytest.fixture
def test_user(db: Session):
    """テスト用ユーザー作成"""
    import uuid

    # ユニークなIDとメールアドレス生成
    unique_id = str(uuid.uuid4())
    unique_email = f"test-{unique_id[:8]}@example.com"

    user = User(
        id=unique_id,
        email=unique_email,
        hashed_password=get_password_hash("OldPassword123!"),
        profile_name="テストユーザー",
        role="user",
        is_active=True,
        is_verified=False,
        is_superuser=False,
        auto_login_enabled=False,
        auto_login_duration=None,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    yield user

    # テスト終了後のクリーンアップ
    db.query(RefreshToken).filter(RefreshToken.user_id == user.id).delete()
    db.delete(user)
    db.commit()


@pytest.fixture
def auth_headers(test_user: User):
    """認証済みヘッダー取得"""
    # ログイン
    response = client.post(
        "/api/auth/login",
        json={"email": test_user.email, "password": "OldPassword123!"},
    )
    assert response.status_code == 200
    data = response.json()
    access_token = data["accessToken"]

    return {"Authorization": f"Bearer {access_token}"}


# ==================== テストケース ====================


# ========== パスワード変更 ==========


def test_change_password_success(test_user: User, auth_headers: dict, db: Session):
    """パスワード変更成功"""
    response = client.put(
        "/api/user/password",
        headers=auth_headers,
        json={"oldPassword": "OldPassword123!", "newPassword": "NewPassword2025!"},
    )

    # レスポンス検証
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "パスワードを変更しました"

    # DBでパスワードが更新されたことを確認
    db.refresh(test_user)
    assert verify_password("NewPassword2025!", test_user.hashed_password)

    # リフレッシュトークンが無効化されたことを確認
    tokens = db.query(RefreshToken).filter(RefreshToken.user_id == test_user.id).all()
    assert all(token.is_revoked for token in tokens)


def test_change_password_wrong_old_password(auth_headers: dict):
    """パスワード変更失敗（現在のパスワードが間違っている）"""
    response = client.put(
        "/api/user/password",
        headers=auth_headers,
        json={"oldPassword": "WrongPassword!", "newPassword": "NewPassword2025!"},
    )

    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "現在のパスワードが正しくありません"


def test_change_password_too_short(auth_headers: dict):
    """パスワード変更失敗（新しいパスワードが短すぎる）"""
    response = client.put(
        "/api/user/password",
        headers=auth_headers,
        json={"oldPassword": "OldPassword123!", "newPassword": "Short1!"},
    )

    # Pydanticバリデーションが先に実行されるため422
    assert response.status_code == 422


def test_change_password_same_as_old(auth_headers: dict):
    """パスワード変更失敗（新旧パスワードが同一）"""
    response = client.put(
        "/api/user/password",
        headers=auth_headers,
        json={"oldPassword": "OldPassword123!", "newPassword": "OldPassword123!"},
    )

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "新しいパスワードは現在のパスワードと異なるものにしてください"


def test_change_password_no_auth():
    """パスワード変更失敗（認証なし）"""
    response = client.put(
        "/api/user/password",
        json={"oldPassword": "OldPassword123!", "newPassword": "NewPassword2025!"},
    )

    assert response.status_code == 403  # Forbiddenまたは401


# ========== ユーザー設定更新 ==========


def test_update_settings_success_7d(test_user: User, auth_headers: dict, db: Session):
    """ユーザー設定更新成功（7日間）"""
    response = client.put(
        "/api/user/settings",
        headers=auth_headers,
        json={"rememberMe": True, "sessionDuration": "7d"},
    )

    # レスポンス検証
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "設定を更新しました"

    # DBで設定が更新されたことを確認
    db.refresh(test_user)
    assert test_user.auto_login_enabled is True
    assert test_user.auto_login_duration == 7


def test_update_settings_success_30d(test_user: User, auth_headers: dict, db: Session):
    """ユーザー設定更新成功（30日間）"""
    response = client.put(
        "/api/user/settings",
        headers=auth_headers,
        json={"rememberMe": True, "sessionDuration": "30d"},
    )

    assert response.status_code == 200
    db.refresh(test_user)
    assert test_user.auto_login_enabled is True
    assert test_user.auto_login_duration == 30


def test_update_settings_success_forever(test_user: User, auth_headers: dict, db: Session):
    """ユーザー設定更新成功（無期限）"""
    response = client.put(
        "/api/user/settings",
        headers=auth_headers,
        json={"rememberMe": True, "sessionDuration": "forever"},
    )

    assert response.status_code == 200
    db.refresh(test_user)
    assert test_user.auto_login_enabled is True
    assert test_user.auto_login_duration == 0  # 0 = 無期限


def test_update_settings_disable_remember_me(test_user: User, auth_headers: dict, db: Session):
    """ユーザー設定更新（自動ログイン無効化）"""
    response = client.put(
        "/api/user/settings",
        headers=auth_headers,
        json={"rememberMe": False, "sessionDuration": "7d"},
    )

    assert response.status_code == 200
    db.refresh(test_user)
    assert test_user.auto_login_enabled is False
    assert test_user.auto_login_duration == 7


def test_update_settings_invalid_duration(auth_headers: dict):
    """ユーザー設定更新失敗（不正なセッション期間）"""
    response = client.put(
        "/api/user/settings",
        headers=auth_headers,
        json={"rememberMe": True, "sessionDuration": "99d"},
    )

    # Pydanticバリデーションエラー（422）
    assert response.status_code == 422


def test_update_settings_no_auth():
    """ユーザー設定更新失敗（認証なし）"""
    response = client.put(
        "/api/user/settings",
        json={"rememberMe": True, "sessionDuration": "7d"},
    )

    assert response.status_code == 403  # Forbiddenまたは401
