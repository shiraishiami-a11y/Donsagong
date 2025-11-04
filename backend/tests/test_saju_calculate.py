"""
命式計算APIのテスト
"""
import pytest
from datetime import datetime
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_calculate_saju_male():
    """男性の命式計算テスト"""
    request_data = {
        "birthDatetime": "1990-03-15T14:30:00+09:00",
        "gender": "male",
        "name": "テスト太郎",
        "timezoneOffset": 9,
    }

    response = client.post("/api/saju/calculate", json=request_data)

    assert response.status_code == 200
    data = response.json()

    # 基本情報チェック
    assert data["name"] == "テスト太郎"
    assert data["gender"] == "male"
    assert "id" in data
    assert data["id"].startswith("saju-")

    # 四柱データチェック
    assert "yearStem" in data
    assert "yearBranch" in data
    assert "monthStem" in data
    assert "monthBranch" in data
    assert "dayStem" in data
    assert "dayBranch" in data
    assert "hourStem" in data
    assert "hourBranch" in data

    # 大運情報チェック
    assert "daeunNumber" in data
    assert "isForward" in data
    assert isinstance(data["isForward"], bool)
    assert "daeunList" in data
    assert isinstance(data["daeunList"], list)
    assert len(data["daeunList"]) > 0

    # 吉凶レベルチェック
    assert data["fortuneLevel"] in ["大吉", "吉", "平", "凶", "大凶"]

    print(f"\n✅ 男性命式計算成功:")
    print(f"  四柱: {data['yearStem']}{data['yearBranch']} {data['monthStem']}{data['monthBranch']} {data['dayStem']}{data['dayBranch']} {data['hourStem']}{data['hourBranch']}")
    print(f"  大運: {len(data['daeunList'])}個")
    print(f"  順行/逆行: {'順行' if data['isForward'] else '逆行'}")


def test_calculate_saju_female():
    """女性の命式計算テスト"""
    request_data = {
        "birthDatetime": "1995-06-20T10:15:00+09:00",
        "gender": "female",
        "name": "テスト花子",
        "timezoneOffset": 9,
    }

    response = client.post("/api/saju/calculate", json=request_data)

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "テスト花子"
    assert data["gender"] == "female"
    assert "daeunList" in data
    assert len(data["daeunList"]) > 0

    print(f"\n✅ 女性命式計算成功:")
    print(f"  四柱: {data['yearStem']}{data['yearBranch']} {data['monthStem']}{data['monthBranch']} {data['dayStem']}{data['dayBranch']} {data['hourStem']}{data['hourBranch']}")
    print(f"  大運: {len(data['daeunList'])}個")


def test_calculate_saju_invalid_year():
    """範囲外の年でエラーテスト"""
    request_data = {
        "birthDatetime": "1899-01-01T00:00:00+09:00",  # 1900年未満
        "gender": "male",
    }

    response = client.post("/api/saju/calculate", json=request_data)

    assert response.status_code == 400
    assert "対応範囲外" in response.json()["detail"]


def test_calculate_saju_invalid_gender():
    """不正な性別でエラーテスト"""
    request_data = {
        "birthDatetime": "1990-03-15T14:30:00+09:00",
        "gender": "unknown",  # 不正な性別
    }

    response = client.post("/api/saju/calculate", json=request_data)

    # Pydanticバリデーションエラー
    assert response.status_code == 422


def test_calculate_saju_without_name():
    """名前なしで計算テスト"""
    request_data = {
        "birthDatetime": "2000-01-01T12:00:00+09:00",
        "gender": "male",
    }

    response = client.post("/api/saju/calculate", json=request_data)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] is None


def test_daeun_list_structure():
    """大運リストの構造テスト"""
    request_data = {
        "birthDatetime": "1985-08-10T08:00:00+09:00",
        "gender": "female",
    }

    response = client.post("/api/saju/calculate", json=request_data)

    assert response.status_code == 200
    data = response.json()

    # 大運リストの各要素をチェック
    for daeun in data["daeunList"]:
        assert "id" in daeun
        assert "sajuId" in daeun
        assert "startAge" in daeun
        assert "endAge" in daeun
        assert "daeunStem" in daeun
        assert "daeunBranch" in daeun
        assert "fortuneLevel" in daeun
        assert daeun["fortuneLevel"] in ["大吉", "吉", "平", "凶", "大凶"]

        # 年齢範囲チェック
        assert daeun["endAge"] > daeun["startAge"]
        assert daeun["endAge"] - daeun["startAge"] == 9  # 10年間

    print(f"\n✅ 大運リスト構造チェック成功: {len(data['daeunList'])}個")
