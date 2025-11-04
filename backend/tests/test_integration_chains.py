"""
全19エンドポイント統合テスト
CHAIN-001〜CHAIN-005のE2E連鎖テストをバックエンドで検証
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime


class TestCHAIN001_SajuCalculationFlow:
    """CHAIN-001: 命式計算全体フロー（1.1→1.2）"""

    def test_chain_001_full_flow(self, client: TestClient):
        """命式計算から保存までの完全フロー"""
        # 1.1 命式計算
        birth_data = {
            "name": "統合テスト太郎",
            "birthDatetime": "1990-01-15T14:30:00+09:00",
            "gender": "male"
        }

        calc_response = client.post("/api/saju/calculate", json=birth_data)
        assert calc_response.status_code == 200
        saju_data = calc_response.json()

        assert "pillars" in saju_data
        assert "daeunList" in saju_data
        assert len(saju_data["pillars"]) == 4
        assert len(saju_data["daeunList"]) > 0

        # 1.2 命式保存
        save_response = client.post("/api/saju/save", json=saju_data)
        assert save_response.status_code == 200
        save_data = save_response.json()

        assert "id" in save_data
        print(f"\n✅ CHAIN-001: 命式計算・保存フロー成功 (ID: {save_data['id']})")


class TestCHAIN002_FortuneHorizontalScroll:
    """CHAIN-002: 水平スクロール運勢表示（1.1→3.1→3.2→3.3→3.4→3.5）"""

    def test_chain_002_full_fortune_flow(self, client: TestClient):
        """命式計算から全運勢データ取得までの完全フロー"""
        # 1.1 命式計算
        birth_data = {
            "name": "運勢テスト花子",
            "birthDatetime": "1995-06-20T10:15:00+09:00",
            "gender": "female"
        }

        calc_response = client.post("/api/saju/calculate", json=birth_data)
        assert calc_response.status_code == 200
        saju_data = calc_response.json()
        saju_id = f"saju-{int(datetime.fromisoformat('1995-06-20T10:15:00+09:00').timestamp() * 1000)}"

        # 3.1 現在の運勢取得
        current_response = client.get(f"/api/saju/{saju_id}/current")
        assert current_response.status_code == 200
        current_data = current_response.json()
        assert "currentDaeun" in current_data
        assert "currentYear" in current_data
        assert "currentMonth" in current_data
        assert "currentDay" in current_data

        # 3.2 大運リスト取得
        daeun_response = client.get(f"/api/saju/{saju_id}/daeun")
        assert daeun_response.status_code == 200
        daeun_data = daeun_response.json()
        assert "daeunList" in daeun_data
        assert len(daeun_data["daeunList"]) > 0

        # 大運の開始年齢を取得
        first_daeun = daeun_data["daeunList"][0]
        daeun_start_age = first_daeun["startAge"]

        # 3.3 年運リスト取得
        year_response = client.get(f"/api/saju/{saju_id}/year/{daeun_start_age}")
        assert year_response.status_code == 200
        year_data = year_response.json()
        assert "years" in year_data
        assert len(year_data["years"]) == 10  # 10年分

        # 最初の年を取得
        first_year = year_data["years"][0]["year"]

        # 3.4 月運リスト取得
        month_response = client.get(f"/api/saju/{saju_id}/month/{first_year}")
        assert month_response.status_code == 200
        month_data = month_response.json()
        assert "months" in month_data
        assert len(month_data["months"]) == 12  # 12ヶ月分

        # 3.5 日運リスト取得
        day_response = client.get(f"/api/saju/{saju_id}/day/{first_year}/1")
        assert day_response.status_code == 200
        day_data = day_response.json()
        assert "days" in day_data
        assert 28 <= len(day_data["days"]) <= 31  # 月によって日数が異なる

        print(f"\n✅ CHAIN-002: 水平スクロール運勢表示フロー成功")


class TestCHAIN003_InteractiveFortune:
    """CHAIN-003: インタラクティブ運勢選択（3.2→3.3→3.4→3.5）"""

    def test_chain_003_daeun_to_day(self, client: TestClient):
        """大運→年運→月運→日運の階層移動"""
        # 前提: 命式作成
        birth_data = {
            "name": "階層テスト三郎",
            "birthDatetime": "2000-03-15T08:00:00+09:00",
            "gender": "male"
        }

        calc_response = client.post("/api/saju/calculate", json=birth_data)
        assert calc_response.status_code == 200
        saju_id = f"saju-{int(datetime.fromisoformat('2000-03-15T08:00:00+09:00').timestamp() * 1000)}"

        # 3.2 大運リスト
        daeun_response = client.get(f"/api/saju/{saju_id}/daeun")
        assert daeun_response.status_code == 200
        daeun_list = daeun_response.json()["daeunList"]
        assert len(daeun_list) > 0

        # 2番目の大運を選択
        daeun_age = daeun_list[1]["startAge"] if len(daeun_list) > 1 else daeun_list[0]["startAge"]

        # 3.3 年運リスト（大運クリック時）
        year_response = client.get(f"/api/saju/{saju_id}/year/{daeun_age}")
        assert year_response.status_code == 200
        year_data = year_response.json()
        assert len(year_data["years"]) == 10

        # 年運の中から1つ選択
        selected_year = year_data["years"][2]["year"]

        # 3.4 月運リスト（年運クリック時）
        month_response = client.get(f"/api/saju/{saju_id}/month/{selected_year}")
        assert month_response.status_code == 200
        month_data = month_response.json()
        assert len(month_data["months"]) == 12

        # 月運の中から1つ選択
        selected_month = 11

        # 3.5 日運リスト（月運クリック時）
        day_response = client.get(f"/api/saju/{saju_id}/day/{selected_year}/{selected_month}")
        assert day_response.status_code == 200
        day_data = day_response.json()
        assert day_data["year"] == selected_year
        assert day_data["month"] == selected_month
        assert len(day_data["days"]) == 30  # 11月は30日

        print(f"\n✅ CHAIN-003: インタラクティブ運勢選択フロー成功")


class TestCHAIN004_GuestToLogin:
    """CHAIN-004: ゲスト→ログイン移行（5.2→5.3→2.1）"""

    def test_chain_004_guest_migration(self, client: TestClient):
        """ゲストデータ移行フロー"""
        # 5.2 新規登録
        register_data = {
            "email": f"guest_migrate_{datetime.now().timestamp()}@test.local",
            "password": "TestPassword123!"
        }

        register_response = client.post("/api/auth/register", json=register_data)
        assert register_response.status_code == 200

        # 5.3 ログイン
        login_response = client.post("/api/auth/login", json=register_data)
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # 2.1 ゲストデータ移行
        guest_data = [
            {
                "name": "ゲストテスト1",
                "birthDatetime": "1990-01-15T14:30:00+09:00",
                "gender": "male",
                "pillars": {
                    "year": {"stem": "庚", "branch": "午"},
                    "month": {"stem": "戊", "branch": "寅"},
                    "day": {"stem": "甲", "branch": "子"},
                    "hour": {"stem": "庚", "branch": "午"}
                },
                "daeunList": []
            },
            {
                "name": "ゲストテスト2",
                "birthDatetime": "1995-06-20T10:15:00+09:00",
                "gender": "female",
                "pillars": {
                    "year": {"stem": "乙", "branch": "亥"},
                    "month": {"stem": "壬", "branch": "午"},
                    "day": {"stem": "癸", "branch": "丑"},
                    "hour": {"stem": "丁", "branch": "巳"}
                },
                "daeunList": []
            }
        ]

        migrate_response = client.post(
            "/api/saju/migrate",
            json={"guestData": guest_data},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert migrate_response.status_code == 200
        migrate_result = migrate_response.json()

        assert migrate_result["imported"] == 2
        assert migrate_result["skipped"] == 0
        assert len(migrate_result["newIds"]) == 2

        print(f"\n✅ CHAIN-004: ゲスト→ログイン移行フロー成功 (移行数: {migrate_result['imported']})")


class TestCHAIN005_DataManagement:
    """CHAIN-005: データ管理統合（2.1→2.2→4.2）"""

    def test_chain_005_data_lifecycle(self, client: TestClient):
        """データ管理のライフサイクル全体"""
        # 前提: ログイン
        register_data = {
            "email": f"data_lifecycle_{datetime.now().timestamp()}@test.local",
            "password": "TestPassword123!"
        }

        client.post("/api/auth/register", json=register_data)
        login_response = client.post("/api/auth/login", json=register_data)
        token = login_response.json()["access_token"]

        # 2.1 命式保存
        birth_data = {
            "name": "データ管理テスト",
            "birthDatetime": "1985-12-25T18:00:00+09:00",
            "gender": "female"
        }

        calc_response = client.post("/api/saju/calculate", json=birth_data)
        saju_data = calc_response.json()

        save_response = client.post(
            "/api/saju/save",
            json=saju_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert save_response.status_code == 200
        saved_id = save_response.json()["id"]

        # 2.2 命式リスト取得
        list_response = client.get(
            "/api/saju/list",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert list_response.status_code == 200
        saju_list = list_response.json()
        assert len(saju_list) > 0

        # 4.2 エクスポート
        export_response = client.get(
            "/api/saju/export",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert export_response.status_code == 200
        export_data = export_response.json()

        assert export_data["version"] == "1.0"
        assert "exportDate" in export_data
        assert "data" in export_data
        assert len(export_data["data"]) > 0

        # 削除
        delete_response = client.delete(
            f"/api/saju/{saved_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert delete_response.status_code == 200

        print(f"\n✅ CHAIN-005: データ管理統合フロー成功")


class TestAllEndpoints:
    """全19エンドポイントの動作確認"""

    def test_all_19_endpoints(self, client: TestClient):
        """全エンドポイントが正常に動作することを確認"""
        endpoints_tested = []

        # 1. ヘルスチェック
        health_response = client.get("/health")
        assert health_response.status_code == 200
        endpoints_tested.append("GET /health")

        # 2. 新規登録
        register_data = {
            "email": f"all_endpoints_{datetime.now().timestamp()}@test.local",
            "password": "TestPassword123!"
        }
        register_response = client.post("/api/auth/register", json=register_data)
        assert register_response.status_code == 200
        endpoints_tested.append("POST /api/auth/register")

        # 3. ログイン
        login_response = client.post("/api/auth/login", json=register_data)
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        endpoints_tested.append("POST /api/auth/login")

        # 4. ユーザー情報取得
        me_response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert me_response.status_code == 200
        endpoints_tested.append("GET /api/auth/me")

        # 5. 命式計算
        birth_data = {
            "name": "全エンドポイントテスト",
            "birthDatetime": "1990-05-10T12:00:00+09:00",
            "gender": "male"
        }
        calc_response = client.post("/api/saju/calculate", json=birth_data)
        assert calc_response.status_code == 200
        saju_data = calc_response.json()
        endpoints_tested.append("POST /api/saju/calculate")

        # 6. 命式保存
        save_response = client.post(
            "/api/saju/save",
            json=saju_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert save_response.status_code == 200
        saju_id = save_response.json()["id"]
        endpoints_tested.append("POST /api/saju/save")

        # 7. 命式リスト取得
        list_response = client.get(
            "/api/saju/list",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert list_response.status_code == 200
        endpoints_tested.append("GET /api/saju/list")

        # 8. 命式詳細取得
        detail_response = client.get(f"/api/saju/{saju_id}")
        assert detail_response.status_code == 200
        endpoints_tested.append("GET /api/saju/{id}")

        # 9. 大運分析取得
        daeun_response = client.get(f"/api/saju/{saju_id}/daeun")
        assert daeun_response.status_code == 200
        daeun_data = daeun_response.json()
        daeun_age = daeun_data["daeunList"][0]["startAge"]
        endpoints_tested.append("GET /api/saju/{id}/daeun")

        # 10. 現在の運勢取得
        current_response = client.get(f"/api/saju/{saju_id}/current")
        assert current_response.status_code == 200
        endpoints_tested.append("GET /api/saju/{id}/current")

        # 11. 年運リスト取得
        year_response = client.get(f"/api/saju/{saju_id}/year/{daeun_age}")
        assert year_response.status_code == 200
        year_data = year_response.json()
        selected_year = year_data["years"][0]["year"]
        endpoints_tested.append("GET /api/saju/{id}/year/{daeun_start_age}")

        # 12. 月運リスト取得
        month_response = client.get(f"/api/saju/{saju_id}/month/{selected_year}")
        assert month_response.status_code == 200
        endpoints_tested.append("GET /api/saju/{id}/month/{year}")

        # 13. 日運リスト取得
        day_response = client.get(f"/api/saju/{saju_id}/day/{selected_year}/5")
        assert day_response.status_code == 200
        endpoints_tested.append("GET /api/saju/{id}/day/{year}/{month}")

        # 14. エクスポート
        export_response = client.get(
            "/api/saju/export",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert export_response.status_code == 200
        endpoints_tested.append("GET /api/saju/export")

        # 15. インポート
        import_data = {
            "version": "1.0",
            "exportDate": datetime.now().isoformat(),
            "data": [{
                "name": "インポートテスト",
                "birthDatetime": "2000-01-01T00:00:00+09:00",
                "gender": "female",
                "pillars": {
                    "year": {"stem": "己", "branch": "卯"},
                    "month": {"stem": "丙", "branch": "子"},
                    "day": {"stem": "辛", "branch": "亥"},
                    "hour": {"stem": "戊", "branch": "子"}
                },
                "daeunList": []
            }]
        }
        import_response = client.post(
            "/api/saju/import",
            json=import_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert import_response.status_code == 200
        endpoints_tested.append("POST /api/saju/import")

        # 16. ゲストデータ移行
        migrate_response = client.post(
            "/api/saju/migrate",
            json={"guestData": []},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert migrate_response.status_code == 200
        endpoints_tested.append("POST /api/saju/migrate")

        # 17. パスワード変更
        password_response = client.post(
            "/api/user/change-password",
            json={"oldPassword": "TestPassword123!", "newPassword": "NewPassword123!"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert password_response.status_code == 200
        endpoints_tested.append("POST /api/user/change-password")

        # 18. 設定更新
        settings_response = client.post(
            "/api/user/settings",
            json={"rememberMe": True, "rememberMeDuration": "7d"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert settings_response.status_code == 200
        endpoints_tested.append("POST /api/user/settings")

        # 19. 命式削除
        delete_response = client.delete(
            f"/api/saju/{saju_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert delete_response.status_code == 200
        endpoints_tested.append("DELETE /api/saju/{id}")

        # 全エンドポイントテスト完了
        assert len(endpoints_tested) == 19

        print("\n" + "="*80)
        print("✅ 全19エンドポイントテスト成功:")
        print("="*80)
        for i, endpoint in enumerate(endpoints_tested, 1):
            print(f"  {i:2d}. {endpoint}")
        print("="*80)
