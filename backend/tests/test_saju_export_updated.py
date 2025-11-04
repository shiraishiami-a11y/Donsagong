"""
データエクスポート機能のテスト（認証付き）

GET /api/saju/export
"""
import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.session import Base, get_db
from app.main import app
from app.models import Saju, User

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
    # テスト用命式を削除
    db = TestingSessionLocal()
    try:
        # テストユーザーの命式を削除
        db.query(Saju).filter(Saju.user_id.like("test-user-%")).delete(synchronize_session=False)
        # テストユーザーを削除
        db.query(User).filter(User.id.like("test-user-%")).delete(synchronize_session=False)
        db.commit()
    finally:
        db.close()


@pytest.fixture
def test_user_token():
    """テストユーザーを作成してトークンを返す"""
    # ユーザー登録
    register_payload = {
        "email": f"testexport{datetime.now().timestamp()}@test.com",
        "password": "TestPassword123!",
        "profileName": "テストユーザー",
    }
    register_response = client.post("/api/auth/register", json=register_payload)
    assert register_response.status_code == 201

    # ログイン
    login_payload = {
        "email": register_payload["email"],
        "password": register_payload["password"],
    }
    login_response = client.post("/api/auth/login", json=login_payload)
    assert login_response.status_code == 200
    token_data = login_response.json()

    return token_data["accessToken"]


class TestExportWithAuth:
    """データエクスポート機能のテストクラス（認証付き）"""

    def test_export_without_auth(self):
        """
        エクスポート: 認証なし
        403 Forbiddenが返ることを確認（HTTPBearerの仕様）
        """
        response = client.get("/api/saju/export")

        assert response.status_code == 403
        data = response.json()
        assert "detail" in data

    def test_export_empty_data(self, test_user_token):
        """
        エクスポート: データが0件の場合
        空のリストが返ることを確認
        """
        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = client.get("/api/saju/export", headers=headers)

        assert response.status_code == 200
        data = response.json()

        # 新しいレスポンス形式を確認
        assert "exported_at" in data
        assert "user_id" in data
        assert "count" in data
        assert isinstance(data["data"], list)
        assert data["count"] == 0
        assert len(data["data"]) == 0

        # Content-Dispositionヘッダーを確認
        assert "Content-Disposition" in response.headers
        content_disposition = response.headers["Content-Disposition"]
        assert "attachment" in content_disposition
        assert "saju_export_" in content_disposition
        assert ".json" in content_disposition

    def test_export_with_data(self, test_user_token):
        """
        エクスポート: データが存在する場合
        保存した命式が正しくエクスポートされることを確認
        """
        headers = {"Authorization": f"Bearer {test_user_token}"}

        # 1. 命式を計算
        calculate_payload = {
            "birthDatetime": "1990-03-15T14:30:00+09:00",
            "gender": "male",
            "name": "山田 太郎",
        }
        calc_response = client.post("/api/saju/calculate", json=calculate_payload)
        assert calc_response.status_code == 200
        saju_data = calc_response.json()

        # 2. 命式を保存
        save_response = client.post("/api/saju/save", json=saju_data, headers=headers)
        assert save_response.status_code == 201

        # 3. エクスポート
        export_response = client.get("/api/saju/export", headers=headers)
        assert export_response.status_code == 200

        export_data = export_response.json()
        assert "exported_at" in export_data
        assert "user_id" in export_data
        assert "count" in export_data
        assert export_data["count"] == 1
        assert len(export_data["data"]) == 1

        # エクスポートされたデータの検証
        exported_saju = export_data["data"][0]
        assert exported_saju["id"] == saju_data["id"]
        assert exported_saju["name"] == "山田 太郎"
        assert exported_saju["gender"] == "male"
        assert exported_saju["birth_datetime"] is not None
        assert "saju" in exported_saju
        assert "year_stem" in exported_saju["saju"]
        assert "created_at" in exported_saju

    def test_export_multiple_data(self, test_user_token):
        """
        エクスポート: 複数の命式がある場合
        全てのデータがエクスポートされることを確認
        """
        headers = {"Authorization": f"Bearer {test_user_token}"}

        # 3つの命式を保存
        test_births = [
            {"birthDatetime": "1990-01-15T10:00:00+09:00", "gender": "male", "name": "太郎"},
            {"birthDatetime": "1995-06-20T15:30:00+09:00", "gender": "female", "name": "花子"},
            {"birthDatetime": "2000-12-25T08:45:00+09:00", "gender": "male", "name": "次郎"},
        ]

        for birth in test_births:
            calc_response = client.post("/api/saju/calculate", json=birth)
            assert calc_response.status_code == 200
            saju_data = calc_response.json()

            save_response = client.post("/api/saju/save", json=saju_data, headers=headers)
            assert save_response.status_code == 201

        # エクスポート
        export_response = client.get("/api/saju/export", headers=headers)
        assert export_response.status_code == 200

        export_data = export_response.json()
        assert export_data["count"] == 3
        assert len(export_data["data"]) == 3

        # 名前のリストを確認
        exported_names = [item["name"] for item in export_data["data"]]
        assert "太郎" in exported_names
        assert "花子" in exported_names
        assert "次郎" in exported_names

    def test_export_order(self, test_user_token):
        """
        エクスポート: ソート順序の確認
        created_at降順（新しい順）で返ることを確認
        """
        headers = {"Authorization": f"Bearer {test_user_token}"}

        # 2つの命式を保存（時間差をつける）
        test_births = [
            {"birthDatetime": "1990-01-15T10:00:00+09:00", "gender": "male", "name": "最初"},
            {"birthDatetime": "1995-06-20T15:30:00+09:00", "gender": "female", "name": "2番目"},
        ]

        for birth in test_births:
            calc_response = client.post("/api/saju/calculate", json=birth)
            saju_data = calc_response.json()
            save_response = client.post("/api/saju/save", json=saju_data, headers=headers)
            assert save_response.status_code == 201

        # エクスポート
        export_response = client.get("/api/saju/export", headers=headers)
        assert export_response.status_code == 200

        export_data = export_response.json()
        assert export_data["count"] == 2

        # 新しい順（2番目→最初）
        assert export_data["data"][0]["name"] == "2番目"
        assert export_data["data"][1]["name"] == "最初"

    def test_export_filename_format(self, test_user_token):
        """
        エクスポート: ファイル名の形式確認
        saju_export_YYYYMMDD.json の形式であることを確認
        """
        headers = {"Authorization": f"Bearer {test_user_token}"}
        response = client.get("/api/saju/export", headers=headers)

        assert response.status_code == 200

        # Content-Dispositionヘッダーを確認
        content_disposition = response.headers.get("Content-Disposition")
        assert content_disposition is not None

        # ファイル名を抽出
        assert 'filename="saju_export_' in content_disposition
        assert '.json"' in content_disposition

        # 日付形式を確認（YYYYMMDD）
        import re

        match = re.search(r'filename="saju_export_(\d{8})\.json"', content_disposition)
        assert match is not None
        date_str = match.group(1)
        assert len(date_str) == 8  # YYYYMMDD = 8桁

        # 日付が現在日付に近いことを確認
        from datetime import datetime

        file_date = datetime.strptime(date_str, "%Y%m%d")
        today = datetime.now()
        assert file_date.date() == today.date()

    def test_export_user_isolation(self):
        """
        エクスポート: ユーザー分離の確認
        他のユーザーのデータはエクスポートされないことを確認
        """
        # ユーザー1を作成
        user1_payload = {
            "email": f"user1_{datetime.now().timestamp()}@test.com",
            "password": "TestPassword123!",
            "profileName": "ユーザー1",
        }
        register1 = client.post("/api/auth/register", json=user1_payload)
        assert register1.status_code == 201
        login1 = client.post("/api/auth/login", json=user1_payload)
        token1 = login1.json()["accessToken"]

        # ユーザー2を作成
        user2_payload = {
            "email": f"user2_{datetime.now().timestamp()}@test.com",
            "password": "TestPassword123!",
            "profileName": "ユーザー2",
        }
        register2 = client.post("/api/auth/register", json=user2_payload)
        assert register2.status_code == 201
        login2 = client.post("/api/auth/login", json=user2_payload)
        token2 = login2.json()["accessToken"]

        # ユーザー1が命式を保存
        calc_payload = {
            "birthDatetime": "1990-03-15T14:30:00+09:00",
            "gender": "male",
            "name": "ユーザー1のデータ",
        }
        calc_response = client.post("/api/saju/calculate", json=calc_payload)
        saju_data = calc_response.json()
        save_response = client.post(
            "/api/saju/save", json=saju_data, headers={"Authorization": f"Bearer {token1}"}
        )
        assert save_response.status_code == 201

        # ユーザー2がエクスポート
        export_response = client.get("/api/saju/export", headers={"Authorization": f"Bearer {token2}"})
        assert export_response.status_code == 200

        export_data = export_response.json()
        # ユーザー2はデータを持っていない
        assert export_data["count"] == 0
        assert len(export_data["data"]) == 0

        # ユーザー1がエクスポート
        export_response1 = client.get("/api/saju/export", headers={"Authorization": f"Bearer {token1}"})
        assert export_response1.status_code == 200

        export_data1 = export_response1.json()
        # ユーザー1はデータを持っている
        assert export_data1["count"] == 1
        assert export_data1["data"][0]["name"] == "ユーザー1のデータ"
