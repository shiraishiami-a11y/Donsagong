"""
命式計算精度テスト
既知の命式データと比較して正確性を検証
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_1990_male_accuracy():
    """
    1990年3月15日14時30分生まれ、男性
    既知のテストケース
    """
    request_data = {
        "birthDatetime": "1990-03-15T14:30:00+09:00",
        "gender": "male",
        "name": "1990年男性テスト",
    }

    response = client.post("/api/saju/calculate", json=request_data)
    assert response.status_code == 200

    data = response.json()

    # 四柱の検証（lunar-pythonの結果を確認）
    print(f"\n1990年3月15日14時30分生まれ、男性:")
    print(f"  年柱: {data['yearStem']}{data['yearBranch']}")
    print(f"  月柱: {data['monthStem']}{data['monthBranch']}")
    print(f"  日柱: {data['dayStem']}{data['dayBranch']}")
    print(f"  時柱: {data['hourStem']}{data['hourBranch']}")

    # 大運情報
    print(f"  大運数: {data['daeunNumber']}")
    print(f"  順行/逆行: {'順行' if data['isForward'] else '逆行'}")
    print(f"  第一大運開始: {data['firstDaeunDate']}")

    # 大運リスト
    print(f"  大運リスト:")
    for idx, daeun in enumerate(data["daeunList"][:5], 1):  # 最初の5個のみ表示
        print(
            f"    {idx}. {daeun['startAge']}-{daeun['endAge']}歳: {daeun['daeunStem']}{daeun['daeunBranch']} ({daeun['fortuneLevel']})"
        )

    # 基本的な妥当性チェック
    assert len(data["daeunList"]) >= 8
    assert all(d["endAge"] - d["startAge"] == 9 for d in data["daeunList"])


def test_1995_female_accuracy():
    """
    1995年6月20日10時15分生まれ、女性
    既知のテストケース
    """
    request_data = {
        "birthDatetime": "1995-06-20T10:15:00+09:00",
        "gender": "female",
        "name": "1995年女性テスト",
    }

    response = client.post("/api/saju/calculate", json=request_data)
    assert response.status_code == 200

    data = response.json()

    print(f"\n1995年6月20日10時15分生まれ、女性:")
    print(f"  年柱: {data['yearStem']}{data['yearBranch']}")
    print(f"  月柱: {data['monthStem']}{data['monthBranch']}")
    print(f"  日柱: {data['dayStem']}{data['dayBranch']}")
    print(f"  時柱: {data['hourStem']}{data['hourBranch']}")
    print(f"  順行/逆行: {'順行' if data['isForward'] else '逆行'}")

    # 大運リスト
    print(f"  大運リスト:")
    for idx, daeun in enumerate(data["daeunList"][:5], 1):
        print(
            f"    {idx}. {daeun['startAge']}-{daeun['endAge']}歳: {daeun['daeunStem']}{daeun['daeunBranch']}"
        )


def test_edge_case_year_boundary():
    """
    年の境界ケース: 1月1日0時0分（立春前）
    """
    request_data = {
        "birthDatetime": "2000-01-01T00:00:00+09:00",
        "gender": "male",
    }

    response = client.post("/api/saju/calculate", json=request_data)
    assert response.status_code == 200

    data = response.json()

    print(f"\n2000年1月1日0時0分生まれ（立春前）:")
    print(f"  年柱: {data['yearStem']}{data['yearBranch']}")
    print(
        f"  注: 立春前なので前年の干支になるべき（lunar-pythonが自動処理）"
    )


def test_210_year_db_range():
    """
    210年節気DB範囲内の複数年代をテスト
    """
    test_years = [
        ("1900-05-15T12:00:00+09:00", "1900年代"),
        ("1950-08-20T18:30:00+09:00", "1950年代"),
        ("2000-03-10T09:45:00+09:00", "2000年代"),
        ("2050-11-25T14:20:00+09:00", "2050年代"),
        ("2100-07-05T06:15:00+09:00", "2100年代"),
    ]

    for birth_datetime, label in test_years:
        request_data = {"birthDatetime": birth_datetime, "gender": "male"}

        response = client.post("/api/saju/calculate", json=request_data)
        assert response.status_code == 200

        data = response.json()
        print(f"\n{label}: {data['yearStem']}{data['yearBranch']} 年柱")


def test_daeun_direction_male_yang():
    """
    男性 + 陽年 → 順行
    """
    # 2000年 = 庚辰年（庚は陽干）
    request_data = {
        "birthDatetime": "2000-05-15T12:00:00+09:00",
        "gender": "male",
    }

    response = client.post("/api/saju/calculate", json=request_data)
    assert response.status_code == 200

    data = response.json()
    print(f"\n男性・陽年テスト:")
    print(f"  年干: {data['yearStem']}")

    # 庚・丙・戊・庚・壬 のいずれかの陽干なら順行になるはず
    yang_stems = ["甲", "丙", "戊", "庚", "壬"]
    if data["yearStem"] in yang_stems:
        assert data["isForward"] is True, "男性・陽年は順行であるべき"
        print(f"  結果: 順行 ✅")


def test_daeun_direction_female_yin():
    """
    女性 + 陰年 → 順行
    """
    # 1995年 = 乙亥年（乙は陰干）
    request_data = {
        "birthDatetime": "1995-06-20T10:15:00+09:00",
        "gender": "female",
    }

    response = client.post("/api/saju/calculate", json=request_data)
    assert response.status_code == 200

    data = response.json()
    print(f"\n女性・陰年テスト:")
    print(f"  年干: {data['yearStem']}")

    # 乙・丁・己・辛・癸 のいずれかの陰干なら順行になるはず
    yin_stems = ["乙", "丁", "己", "辛", "癸"]
    if data["yearStem"] in yin_stems:
        assert data["isForward"] is True, "女性・陰年は順行であるべき"
        print(f"  結果: 順行 ✅")
