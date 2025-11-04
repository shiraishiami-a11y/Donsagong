"""
命式保存APIのテスト
"""
import pytest
from datetime import datetime
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_save_saju():
    """命式保存テスト"""
    # まず命式を計算
    calc_request = {
        "birthDatetime": "1988-04-12T16:45:00+09:00",
        "gender": "male",
        "name": "保存テスト",
    }

    calc_response = client.post("/api/saju/calculate", json=calc_request)
    assert calc_response.status_code == 200
    saju_data = calc_response.json()

    # 計算結果を保存
    save_response = client.post("/api/saju/save", json=saju_data)

    assert save_response.status_code == 201
    save_data = save_response.json()

    assert save_data["success"] is True
    assert save_data["id"] == saju_data["id"]
    assert "保存しました" in save_data["message"]

    print(f"\n✅ 命式保存成功: ID={save_data['id']}")


def test_save_saju_multiple():
    """複数の命式を保存"""
    test_cases = [
        {"birthDatetime": "1990-01-01T00:00:00+09:00", "gender": "male", "name": "テスト1"},
        {"birthDatetime": "1995-06-15T12:30:00+09:00", "gender": "female", "name": "テスト2"},
        {"birthDatetime": "2000-12-31T23:59:00+09:00", "gender": "male", "name": "テスト3"},
    ]

    saved_ids = []

    for test_case in test_cases:
        # 計算
        calc_response = client.post("/api/saju/calculate", json=test_case)
        assert calc_response.status_code == 200
        saju_data = calc_response.json()

        # 保存
        save_response = client.post("/api/saju/save", json=saju_data)
        assert save_response.status_code == 201
        save_data = save_response.json()

        saved_ids.append(save_data["id"])

    assert len(saved_ids) == len(test_cases)
    assert len(set(saved_ids)) == len(saved_ids)  # 全てユニークID

    print(f"\n✅ 複数命式保存成功: {len(saved_ids)}件")


def test_save_saju_invalid_data():
    """不正なデータで保存エラーテスト"""
    invalid_data = {
        "id": "invalid-id",
        "name": "不正データ",
        # 必須フィールドが不足
    }

    response = client.post("/api/saju/save", json=invalid_data)

    # Pydanticバリデーションエラー
    assert response.status_code == 422
