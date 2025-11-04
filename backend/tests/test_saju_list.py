"""
命式管理APIのテスト（リスト取得・詳細取得・削除）
"""
import json
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.models import Saju as SajuModel

client = TestClient(app)


def test_get_saju_list_empty(db: Session):
    """空のリストが返されることを確認"""
    # 全データ削除
    db.query(SajuModel).delete()
    db.commit()

    response = client.get("/api/saju/list")
    assert response.status_code == 200

    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0
    assert data["page"] == 1
    assert data["limit"] == 20
    assert data["hasNext"] is False


def test_get_saju_list_with_data(db: Session):
    """保存済みデータが正しく取得できることを確認"""
    # 全データ削除
    db.query(SajuModel).delete()
    db.commit()

    # テストデータ作成
    test_saju = SajuModel(
        id="test-001",
        user_id=None,  # ゲストモード
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
        daeun_list=json.dumps([]),
        fortune_level=4,  # 吉
    )
    db.add(test_saju)
    db.commit()

    response = client.get("/api/saju/list")
    assert response.status_code == 200

    data = response.json()
    assert len(data["items"]) == 1
    assert data["total"] == 1
    assert data["items"][0]["id"] == "test-001"
    assert data["items"][0]["name"] == "テスト太郎"
    assert data["items"][0]["fortuneLevel"] == "吉"
    assert data["items"][0]["yearStem"] == "庚"
    assert data["items"][0]["yearBranch"] == "午"


def test_get_saju_list_pagination(db: Session):
    """ページネーションが正しく動作することを確認"""
    # 全データ削除
    db.query(SajuModel).delete()
    db.commit()

    # 25件のテストデータ作成
    for i in range(25):
        test_saju = SajuModel(
            id=f"test-{i:03d}",
            user_id=None,
            name=f"テスト{i}",
            birth_datetime=datetime(1990, 1, 1, 0, 0, 0),
            gender="male",
            year_stem="庚",
            year_branch="午",
            month_stem="己",
            month_branch="卯",
            day_stem="丙",
            day_branch="午",
            hour_stem="乙",
            hour_branch="未",
            daeun_list=json.dumps([]),
            fortune_level=3,
        )
        db.add(test_saju)
    db.commit()

    # 1ページ目（20件）
    response = client.get("/api/saju/list?page=1&limit=20")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 20
    assert data["total"] == 25
    assert data["hasNext"] is True

    # 2ページ目（5件）
    response = client.get("/api/saju/list?page=2&limit=20")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 5
    assert data["total"] == 25
    assert data["hasNext"] is False


def test_get_saju_list_sort_by_fortune_level(db: Session):
    """吉凶レベル順ソートが正しく動作することを確認"""
    # 全データ削除
    db.query(SajuModel).delete()
    db.commit()

    # 吉凶レベルが異なるデータ作成
    levels = [
        ("test-001", 5),  # 大吉
        ("test-002", 3),  # 平
        ("test-003", 1),  # 大凶
    ]
    for id, level in levels:
        test_saju = SajuModel(
            id=id,
            user_id=None,
            name="テスト",
            birth_datetime=datetime(1990, 1, 1, 0, 0, 0),
            gender="male",
            year_stem="庚",
            year_branch="午",
            month_stem="己",
            month_branch="卯",
            day_stem="丙",
            day_branch="午",
            hour_stem="乙",
            hour_branch="未",
            daeun_list=json.dumps([]),
            fortune_level=level,
        )
        db.add(test_saju)
    db.commit()

    # 降順
    response = client.get("/api/saju/list?sortBy=fortuneLevel&order=desc")
    assert response.status_code == 200
    data = response.json()
    assert data["items"][0]["fortuneLevel"] == "大吉"
    assert data["items"][1]["fortuneLevel"] == "平"
    assert data["items"][2]["fortuneLevel"] == "大凶"

    # 昇順
    response = client.get("/api/saju/list?sortBy=fortuneLevel&order=asc")
    assert response.status_code == 200
    data = response.json()
    assert data["items"][0]["fortuneLevel"] == "大凶"
    assert data["items"][1]["fortuneLevel"] == "平"
    assert data["items"][2]["fortuneLevel"] == "大吉"


def test_get_saju_detail(db: Session):
    """命式詳細が正しく取得できることを確認"""
    # 全データ削除
    db.query(SajuModel).delete()
    db.commit()

    # テストデータ作成
    daeun_list = [
        {
            "id": 1,
            "sajuId": "test-detail-001",
            "startAge": 8,
            "endAge": 17,
            "daeunStem": "乙",
            "daeunBranch": "卯",
            "fortuneLevel": "平",
            "sipsin": "偏印",
            "isCurrent": False,
        }
    ]
    test_saju = SajuModel(
        id="test-detail-001",
        user_id=None,
        name="詳細テスト",
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
        fortune_level=4,
    )
    db.add(test_saju)
    db.commit()

    response = client.get("/api/saju/test-detail-001")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == "test-detail-001"
    assert data["name"] == "詳細テスト"
    assert data["fortuneLevel"] == "吉"
    assert len(data["daeunList"]) == 1
    assert data["daeunList"][0]["daeunStem"] == "乙"
    assert data["daeunList"][0]["daeunBranch"] == "卯"


def test_get_saju_detail_not_found(db: Session):
    """存在しないIDで404が返されることを確認"""
    response = client.get("/api/saju/non-existent-id")
    assert response.status_code == 404
    data = response.json()
    assert "命式が見つかりません" in data["detail"]


def test_delete_saju(db: Session):
    """命式削除が正しく動作することを確認"""
    # 全データ削除
    db.query(SajuModel).delete()
    db.commit()

    # テストデータ作成
    test_saju = SajuModel(
        id="test-delete-001",
        user_id=None,
        name="削除テスト",
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
        daeun_list=json.dumps([]),
        fortune_level=3,
    )
    db.add(test_saju)
    db.commit()

    # 削除実行
    response = client.delete("/api/saju/test-delete-001")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "削除しました" in data["message"]

    # DBから削除されていることを確認
    deleted_saju = db.query(SajuModel).filter(SajuModel.id == "test-delete-001").first()
    assert deleted_saju is None


def test_delete_saju_not_found(db: Session):
    """存在しないIDで404が返されることを確認"""
    response = client.delete("/api/saju/non-existent-id")
    assert response.status_code == 404
    data = response.json()
    assert "見つかりませんでした" in data["detail"]


def test_get_saju_list_only_guest_data(db: Session):
    """ゲストモードのデータのみ取得されることを確認"""
    # 全命式データ削除
    db.query(SajuModel).delete()
    db.commit()

    # ゲストデータ（user_id is null）
    guest_saju = SajuModel(
        id="guest-001",
        user_id=None,
        name="ゲスト",
        birth_datetime=datetime(1990, 1, 1, 0, 0, 0),
        gender="male",
        year_stem="庚",
        year_branch="午",
        month_stem="己",
        month_branch="卯",
        day_stem="丙",
        day_branch="午",
        hour_stem="乙",
        hour_branch="未",
        daeun_list=json.dumps([]),
        fortune_level=3,
    )
    db.add(guest_saju)
    db.commit()

    # ゲストモードのデータのみ取得されることを確認
    response = client.get("/api/saju/list")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["id"] == "guest-001"
    assert data["items"][0]["name"] == "ゲスト"
