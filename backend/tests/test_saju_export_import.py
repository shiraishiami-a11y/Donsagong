"""
データエクスポート/インポート機能のテスト

GET /api/saju/export
POST /api/saju/import
"""
import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.session import Base, get_db
from app.main import app
from app.models import Saju

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
    # テスト用命式を削除（user_id is null）
    db = TestingSessionLocal()
    try:
        db.query(Saju).filter(Saju.user_id.is_(None)).delete()
        db.commit()
    finally:
        db.close()


class TestExportImport:
    """データエクスポート/インポート機能のテストクラス"""

    def test_export_empty_data(self):
        """
        エクスポート: データが0件の場合
        空のリストが返ることを確認
        """
        response = client.get("/api/saju/export")

        assert response.status_code == 200
        data = response.json()

        assert data["version"] == "1.0.0"
        assert "exportDate" in data
        assert isinstance(data["data"], list)
        assert len(data["data"]) == 0

    def test_export_with_data(self):
        """
        エクスポート: データが存在する場合
        保存した命式が正しくエクスポートされることを確認
        """
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
        save_response = client.post("/api/saju/save", json=saju_data)
        assert save_response.status_code == 201

        # 3. エクスポート
        export_response = client.get("/api/saju/export")
        assert export_response.status_code == 200

        export_data = export_response.json()
        assert export_data["version"] == "1.0.0"
        assert len(export_data["data"]) == 1

        # エクスポートされたデータの検証
        exported_saju = export_data["data"][0]
        assert exported_saju["id"] == saju_data["id"]
        assert exported_saju["name"] == "山田 太郎"
        assert exported_saju["gender"] == "male"
        assert exported_saju["yearStem"] == saju_data["yearStem"]
        assert exported_saju["fortuneLevel"] in ["大吉", "吉", "平", "凶", "大凶"]

    def test_export_multiple_data(self):
        """
        エクスポート: 複数の命式がある場合
        全てのデータがエクスポートされることを確認
        """
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

            save_response = client.post("/api/saju/save", json=saju_data)
            assert save_response.status_code == 201

        # エクスポート
        export_response = client.get("/api/saju/export")
        assert export_response.status_code == 200

        export_data = export_response.json()
        assert export_data["version"] == "1.0.0"
        assert len(export_data["data"]) == 3

        # 名前のリストを確認
        exported_names = [item["name"] for item in export_data["data"]]
        assert "太郎" in exported_names
        assert "花子" in exported_names
        assert "次郎" in exported_names

    def test_import_valid_data(self):
        """
        インポート: 正しい形式のデータ
        データが正常にインポートされることを確認
        """
        # 1. まず命式を計算してエクスポート形式のデータを作成
        calculate_payload = {
            "birthDatetime": "1990-03-15T14:30:00+09:00",
            "gender": "male",
            "name": "テスト太郎",
        }
        calc_response = client.post("/api/saju/calculate", json=calculate_payload)
        assert calc_response.status_code == 200
        saju_data = calc_response.json()

        # 2. エクスポート形式のデータを作成
        import_payload = {
            "version": "1.0.0",
            "exportDate": datetime.now().isoformat(),
            "data": [saju_data],
        }

        # 3. インポート
        import_response = client.post("/api/saju/import", json=import_payload)
        assert import_response.status_code == 200

        import_result = import_response.json()
        assert import_result["success"] is True
        assert import_result["importedCount"] == 1
        assert "1件のデータをインポートしました" in import_result["message"]

        # 4. インポートされたデータを確認
        list_response = client.get("/api/saju/list")
        assert list_response.status_code == 200
        list_data = list_response.json()
        assert list_data["total"] == 1
        assert list_data["items"][0]["name"] == "テスト太郎"

    def test_import_duplicate_data(self):
        """
        インポート: 重複データのスキップ
        既存のIDと重複するデータはスキップされることを確認
        """
        # 1. 命式を保存
        calculate_payload = {
            "birthDatetime": "1990-03-15T14:30:00+09:00",
            "gender": "male",
            "name": "山田 太郎",
        }
        calc_response = client.post("/api/saju/calculate", json=calculate_payload)
        assert calc_response.status_code == 200
        saju_data = calc_response.json()

        save_response = client.post("/api/saju/save", json=saju_data)
        assert save_response.status_code == 201

        # 2. 同じデータをインポート（重複）
        import_payload = {
            "version": "1.0.0",
            "exportDate": datetime.now().isoformat(),
            "data": [saju_data],
        }

        import_response = client.post("/api/saju/import", json=import_payload)
        assert import_response.status_code == 200

        import_result = import_response.json()
        assert import_result["success"] is True
        assert import_result["importedCount"] == 0
        assert "全て重複" in import_result["message"]

    def test_import_multiple_data(self):
        """
        インポート: 複数データの一括インポート
        複数の命式が正常にインポートされることを確認
        """
        # 1. 複数の命式を計算
        test_births = [
            {"birthDatetime": "1990-01-15T10:00:00+09:00", "gender": "male", "name": "太郎"},
            {"birthDatetime": "1995-06-20T15:30:00+09:00", "gender": "female", "name": "花子"},
            {"birthDatetime": "2000-12-25T08:45:00+09:00", "gender": "male", "name": "次郎"},
        ]

        saju_list = []
        for birth in test_births:
            calc_response = client.post("/api/saju/calculate", json=birth)
            assert calc_response.status_code == 200
            saju_list.append(calc_response.json())

        # 2. 一括インポート
        import_payload = {
            "version": "1.0.0",
            "exportDate": datetime.now().isoformat(),
            "data": saju_list,
        }

        import_response = client.post("/api/saju/import", json=import_payload)
        assert import_response.status_code == 200

        import_result = import_response.json()
        assert import_result["success"] is True
        assert import_result["importedCount"] == 3
        assert "3件のデータをインポートしました" in import_result["message"]

        # 3. インポートされたデータを確認
        list_response = client.get("/api/saju/list")
        assert list_response.status_code == 200
        list_data = list_response.json()
        assert list_data["total"] == 3

    def test_import_invalid_version(self):
        """
        インポート: 不正なバージョン
        サポートされていないバージョンの場合はエラーを返すことを確認
        """
        import_payload = {
            "version": "2.0.0",  # サポートされていないバージョン
            "exportDate": datetime.now().isoformat(),
            "data": [],
        }

        import_response = client.post("/api/saju/import", json=import_payload)
        assert import_response.status_code == 200

        import_result = import_response.json()
        assert import_result["success"] is False
        assert import_result["importedCount"] == 0
        assert "サポートされていないバージョン" in import_result["message"]

    def test_export_import_roundtrip(self):
        """
        エクスポート→インポートの往復テスト
        エクスポートしたデータをインポートしても同じデータになることを確認
        """
        # 1. 元データを保存
        calculate_payload = {
            "birthDatetime": "1990-03-15T14:30:00+09:00",
            "gender": "male",
            "name": "山田 太郎",
        }
        calc_response = client.post("/api/saju/calculate", json=calculate_payload)
        assert calc_response.status_code == 200
        original_saju = calc_response.json()

        save_response = client.post("/api/saju/save", json=original_saju)
        assert save_response.status_code == 201

        # 2. エクスポート
        export_response = client.get("/api/saju/export")
        assert export_response.status_code == 200
        export_data = export_response.json()

        # 3. DB削除（クリーンアップ）
        delete_response = client.delete(f"/api/saju/{original_saju['id']}")
        assert delete_response.status_code == 200

        # 4. 再インポート
        import_response = client.post("/api/saju/import", json=export_data)
        assert import_response.status_code == 200
        import_result = import_response.json()
        assert import_result["success"] is True
        assert import_result["importedCount"] == 1

        # 5. インポートされたデータを取得
        detail_response = client.get(f"/api/saju/{original_saju['id']}")
        assert detail_response.status_code == 200
        imported_saju = detail_response.json()

        # 6. 元データと一致することを確認
        assert imported_saju["id"] == original_saju["id"]
        assert imported_saju["name"] == original_saju["name"]
        assert imported_saju["gender"] == original_saju["gender"]
        assert imported_saju["yearStem"] == original_saju["yearStem"]
        assert imported_saju["yearBranch"] == original_saju["yearBranch"]
        assert imported_saju["dayStem"] == original_saju["dayStem"]
        assert imported_saju["fortuneLevel"] == original_saju["fortuneLevel"]
