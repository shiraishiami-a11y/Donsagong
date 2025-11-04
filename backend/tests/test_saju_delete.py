"""
命式削除API統合テスト
テスト対象:
- DELETE /api/saju/{id}

要件:
- 認証必須（JWT）
- 自分の命式のみ削除可能
- 存在しないIDはエラー
- 他ユーザーの命式は削除不可
"""
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.session import Base, get_db
from app.main import app
from app.models import RefreshToken, Saju, User

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
def cleanup_test_data():
    """各テスト後にテストデータを削除"""
    yield
    # テストデータを削除
    db = TestingSessionLocal()
    try:
        # テスト用命式を削除
        db.query(Saju).filter(
            Saju.user_id.in_(
                db.query(User.id).filter(User.email.like("test_delete_%@example.com"))
            )
        ).delete(synchronize_session=False)

        # テスト用リフレッシュトークンを削除
        db.query(RefreshToken).filter(
            RefreshToken.user_id.in_(
                db.query(User.id).filter(User.email.like("test_delete_%@example.com"))
            )
        ).delete(synchronize_session=False)

        # テスト用ユーザーを削除
        db.query(User).filter(User.email.like("test_delete_%@example.com")).delete()
        db.commit()
    finally:
        db.close()


def create_test_user_and_login(email: str, password: str = "TestPassword2025!"):
    """テストユーザー作成＆ログイン"""
    # 新規登録
    response = client.post(
        "/api/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )
    assert response.status_code == 201
    data = response.json()
    return data["accessToken"], data["user"]["id"]


def create_test_saju(access_token: str, name: str = "テスト太郎"):
    """テスト命式作成"""
    # 命式計算
    calc_response = client.post(
        "/api/saju/calculate",
        json={
            "name": name,
            "birthDatetime": "1990-01-15T14:30:00+09:00",
            "gender": "male",
        },
    )
    assert calc_response.status_code == 200
    saju_data = calc_response.json()

    # 命式保存
    save_response = client.post(
        "/api/saju/save",
        json=saju_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert save_response.status_code == 201

    return saju_data["id"]


# ==================== 削除テスト ====================


def test_delete_success():
    """正常系：自分の命式を削除"""
    # ユーザー作成＆ログイン
    access_token, user_id = create_test_user_and_login("test_delete_success@example.com")

    # 命式作成
    saju_id = create_test_saju(access_token)

    # 削除実行
    response = client.delete(
        f"/api/saju/{saju_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "命式を削除しました"

    # 削除確認（GET /api/saju/{id}でエラー）
    get_response = client.get(f"/api/saju/{saju_id}")
    assert get_response.status_code == 404


def test_delete_not_found():
    """異常系：存在しないIDを削除"""
    # ユーザー作成＆ログイン
    access_token, user_id = create_test_user_and_login("test_delete_notfound@example.com")

    # 存在しないIDで削除試行
    fake_id = f"saju-{uuid.uuid4()}"
    response = client.delete(
        f"/api/saju/{fake_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "命式が見つかりません"


def test_delete_unauthorized():
    """異常系：未ログインで削除試行"""
    # ユーザー作成＆命式作成
    access_token, user_id = create_test_user_and_login("test_delete_unauth@example.com")
    saju_id = create_test_saju(access_token)

    # 認証なしで削除試行
    response = client.delete(f"/api/saju/{saju_id}")

    assert response.status_code == 403  # FastAPIのHTTPBearerのデフォルト動作


def test_delete_forbidden():
    """異常系：他ユーザーの命式を削除試行"""
    # ユーザー1作成＆命式作成
    access_token1, user_id1 = create_test_user_and_login("test_delete_user1@example.com")
    saju_id = create_test_saju(access_token1, "ユーザー1の命式")

    # ユーザー2作成＆ログイン
    access_token2, user_id2 = create_test_user_and_login("test_delete_user2@example.com")

    # ユーザー2がユーザー1の命式を削除試行
    response = client.delete(
        f"/api/saju/{saju_id}",
        headers={"Authorization": f"Bearer {access_token2}"},
    )

    assert response.status_code == 403
    data = response.json()
    assert data["detail"] == "この命式にアクセスする権限がありません"

    # ユーザー1の命式が削除されていないことを確認
    get_response = client.get(f"/api/saju/{saju_id}")
    assert get_response.status_code == 200


def test_delete_invalid_token():
    """異常系：無効なトークンで削除試行"""
    # ユーザー作成＆命式作成
    access_token, user_id = create_test_user_and_login("test_delete_invalid@example.com")
    saju_id = create_test_saju(access_token)

    # 無効なトークンで削除試行
    response = client.delete(
        f"/api/saju/{saju_id}",
        headers={"Authorization": "Bearer invalid_token_here"},
    )

    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "認証が必要です"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
