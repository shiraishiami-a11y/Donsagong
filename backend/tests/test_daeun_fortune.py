"""
大運分析APIの統合テスト
"""
import json
from datetime import datetime

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.models import Saju as SajuModel

client = TestClient(app)


@pytest.fixture
def test_saju_data(db):
    """テスト用の命式データをDBに作成"""
    # 命式データ作成
    daeun_list = [
        {
            "id": 1,
            "sajuId": "test-saju-001",
            "startAge": 8,
            "endAge": 17,
            "daeunStem": "乙",
            "daeunBranch": "卯",
            "fortuneLevel": "平",
            "sipsin": "偏印",
            "isCurrent": False,
        },
        {
            "id": 2,
            "sajuId": "test-saju-001",
            "startAge": 18,
            "endAge": 27,
            "daeunStem": "甲",
            "daeunBranch": "寅",
            "fortuneLevel": "吉",
            "sipsin": "比肩",
            "isCurrent": False,
        },
        {
            "id": 3,
            "sajuId": "test-saju-001",
            "startAge": 28,
            "endAge": 37,
            "daeunStem": "丙",
            "daeunBranch": "午",
            "fortuneLevel": "大吉",
            "sipsin": "正官",
            "isCurrent": True,
        },
    ]

    db_saju = SajuModel(
        id="test-saju-001",
        user_id=None,
        name="テスト太郎",
        birth_datetime=datetime(1990, 3, 15, 14, 30, 0),
        gender="male",
        year_stem="庚",
        year_branch="午",
        month_stem="己",
        month_branch="卯",
        day_stem="丙",
        day_branch="午",
        hour_stem="乙",
        hour_branch="未",
        daeun_list=json.dumps(daeun_list, ensure_ascii=False),
        fortune_level=4,  # 吉
    )

    db.add(db_saju)
    db.commit()
    db.refresh(db_saju)

    yield db_saju

    # テスト後のクリーンアップ
    db.delete(db_saju)
    db.commit()


def test_get_daeun_analysis_success(test_saju_data):
    """大運分析取得 - 成功"""
    response = client.get("/api/saju/test-saju-001/daeun")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "daeunNumber" in data
    assert "isForward" in data
    assert "afterBirth" in data
    assert "firstDaeunDate" in data
    assert "currentAge" in data
    assert "daeunList" in data
    assert len(data["daeunList"]) == 3


def test_get_daeun_analysis_not_found():
    """大運分析取得 - 命式が存在しない"""
    response = client.get("/api/saju/nonexistent-id/daeun")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "命式が見つかりません" in response.json()["detail"]


def test_get_current_fortune_success(test_saju_data):
    """現在の運勢取得 - 成功"""
    response = client.get("/api/saju/test-saju-001/current")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "date" in data
    assert "yearFortune" in data
    assert "monthFortune" in data
    assert "dayFortune" in data

    # 各運勢の詳細を確認
    year_fortune = data["yearFortune"]
    assert "stem" in year_fortune
    assert "branch" in year_fortune
    assert "fortuneLevel" in year_fortune
    assert "description" in year_fortune
    assert "element" in year_fortune


def test_get_current_fortune_with_date(test_saju_data):
    """現在の運勢取得 - 特定日指定"""
    response = client.get("/api/saju/test-saju-001/current?date=2025-11-02")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["date"] == "2025-11-02"


def test_get_year_fortune_list_success(test_saju_data):
    """年運リスト取得 - 成功"""
    response = client.get("/api/saju/test-saju-001/year/28")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "daeunStartAge" in data
    assert "daeunEndAge" in data
    assert "years" in data
    assert data["daeunStartAge"] == 28
    assert data["daeunEndAge"] == 37
    assert len(data["years"]) == 10  # 10年分

    # 最初の年運を確認
    first_year = data["years"][0]
    assert "id" in first_year
    assert "sajuId" in first_year
    assert "daeunStartAge" in first_year
    assert "year" in first_year
    assert "age" in first_year
    assert "yearStem" in first_year
    assert "yearBranch" in first_year
    assert "fortuneLevel" in first_year
    assert "sipsin" in first_year
    assert "isCurrent" in first_year


def test_get_month_fortune_list_success(test_saju_data):
    """月運リスト取得 - 成功"""
    response = client.get("/api/saju/test-saju-001/month/2025")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "year" in data
    assert "months" in data
    assert data["year"] == 2025
    assert len(data["months"]) == 12  # 12ヶ月分

    # 最初の月運を確認
    first_month = data["months"][0]
    assert "id" in first_month
    assert "sajuId" in first_month
    assert "year" in first_month
    assert "month" in first_month
    assert "monthStem" in first_month
    assert "monthBranch" in first_month
    assert "fortuneLevel" in first_month
    assert "sipsin" in first_month
    assert "isCurrent" in first_month


def test_get_day_fortune_list_success(test_saju_data):
    """日運リスト取得 - 成功"""
    response = client.get("/api/saju/test-saju-001/day/2025/11")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "year" in data
    assert "month" in data
    assert "days" in data
    assert data["year"] == 2025
    assert data["month"] == 11
    assert len(data["days"]) == 30  # 2025年11月は30日

    # 最初の日運を確認
    first_day = data["days"][0]
    assert "id" in first_day
    assert "sajuId" in first_day
    assert "year" in first_day
    assert "month" in first_day
    assert "day" in first_day
    assert "dayStem" in first_day
    assert "dayBranch" in first_day
    assert "fortuneLevel" in first_day
    assert "sipsin" in first_day
    assert "isToday" in first_day


def test_get_day_fortune_list_invalid_month(test_saju_data):
    """日運リスト取得 - 不正な月"""
    response = client.get("/api/saju/test-saju-001/day/2025/13")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "不正な年月指定です" in response.json()["detail"]


def test_all_endpoints_not_found():
    """全エンドポイント - 命式が存在しない場合"""
    endpoints = [
        "/api/saju/nonexistent/daeun",
        "/api/saju/nonexistent/current",
        "/api/saju/nonexistent/year/28",
        "/api/saju/nonexistent/month/2025",
        "/api/saju/nonexistent/day/2025/11",
    ]

    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "命式が見つかりません" in response.json()["detail"]
