"""
命式計算・保存APIルーター
"""
import json
import uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException, status, Depends, Response
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.db.session import get_db
from app.models import Saju as SajuModel, User
from app.schemas.saju import (
    AfterBirth,
    BirthDataRequest,
    CurrentFortuneResponse,
    DaeunAnalysisResponse,
    DaeunInfo,
    DayFortuneInfo,
    DayFortuneListResponse,
    DeleteResponse,
    ErrorResponse,
    ExportData,
    ExportResponse,
    ExportSajuItem,
    FortuneDetail,
    ImportResponse,
    MigrateRequest,
    MigrateResponse,
    MonthFortuneInfo,
    MonthFortuneListResponse,
    SajuListResponse,
    SajuSummary,
    SaveResponse,
    SajuResponse,
    YearFortuneInfo,
    YearFortuneListResponse,
)
from app.services.saju_calculator import SajuCalculator, SolarTermsDB
from app.services.fortune_service import FortuneCalculator

router = APIRouter(prefix="/api/saju", tags=["saju"])

# 命式計算エンジンのシングルトンインスタンス
_calculator_instance: SajuCalculator = None
_fortune_calculator_instance: FortuneCalculator = None


def get_calculator() -> SajuCalculator:
    """命式計算エンジンのインスタンスを取得（シングルトン）"""
    global _calculator_instance
    if _calculator_instance is None:
        from app.core.config import settings
        solar_terms_db = SolarTermsDB(db_path=settings.SOLAR_TERMS_DB_PATH)
        _calculator_instance = SajuCalculator(solar_terms_db)
    return _calculator_instance


def get_fortune_calculator() -> FortuneCalculator:
    """年月日運計算エンジンのインスタンスを取得（シングルトン）"""
    global _fortune_calculator_instance
    if _fortune_calculator_instance is None:
        _fortune_calculator_instance = FortuneCalculator()
    return _fortune_calculator_instance


@router.post(
    "/calculate",
    response_model=SajuResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "バリデーションエラー"},
    },
)
async def calculate_saju(data: BirthDataRequest, db: Session = Depends(get_db)):
    """
    命式計算エンドポイント

    生年月日時と性別から四柱推命の命式を計算し、大運リスト・吉凶レベルを返す
    ゲストモードでもデータベースに保存（user_id=NULL）
    """
    try:
        # ISO 8601文字列をdatetimeに変換
        birth_datetime = datetime.fromisoformat(data.birthDatetime.replace("Z", "+00:00"))

        # 命式計算
        calculator = get_calculator()
        result = calculator.calculate(birth_datetime, data.gender, data.name)

        # UUID生成
        saju_id = f"saju-{uuid.uuid4()}"

        # DaeunInfoリストにsajuIdを設定
        daeun_list = []
        for daeun in result["daeunList"]:
            daeun["sajuId"] = saju_id
            daeun_list.append(DaeunInfo(**daeun))

        # 吉凶レベル文字列を数値に変換
        fortune_level_map = {"大凶": 1, "凶": 2, "平": 3, "吉凶": 4, "吉": 5, "小吉": 6, "大吉": 7}
        fortune_level_int = fortune_level_map.get(result["fortuneLevel"], 3)  # デフォルト=平

        # データベースに保存（ゲストモード: user_id=NULL）
        saju_db = SajuModel(
            id=saju_id,
            user_id=None,  # ゲストモード
            name=result["name"],
            birth_datetime=birth_datetime,
            gender=result["gender"],
            year_stem=result["yearStem"],
            year_branch=result["yearBranch"],
            month_stem=result["monthStem"],
            month_branch=result["monthBranch"],
            day_stem=result["dayStem"],
            day_branch=result["dayBranch"],
            hour_stem=result["hourStem"],
            hour_branch=result["hourBranch"],
            daeun_list=json.dumps([daeun.model_dump() for daeun in daeun_list], ensure_ascii=False),
            fortune_level=fortune_level_int,
        )
        db.add(saju_db)
        db.commit()
        db.refresh(saju_db)

        # レスポンス構築
        response = SajuResponse(
            id=saju_id,
            name=result["name"],
            birthDatetime=result["birthDatetime"],
            gender=result["gender"],
            yearStem=result["yearStem"],
            yearBranch=result["yearBranch"],
            monthStem=result["monthStem"],
            monthBranch=result["monthBranch"],
            dayStem=result["dayStem"],
            dayBranch=result["dayBranch"],
            hourStem=result["hourStem"],
            hourBranch=result["hourBranch"],
            daeunNumber=result["daeunNumber"],
            isForward=result["isForward"],
            afterBirthYears=result["afterBirthYears"],
            afterBirthMonths=result["afterBirthMonths"],
            afterBirthDays=result["afterBirthDays"],
            firstDaeunDate=result["firstDaeunDate"],
            daeunList=daeun_list,
            fortuneLevel=result["fortuneLevel"],
            createdAt=result["createdAt"],
        )

        return response

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"命式計算中にエラーが発生しました: {str(e)}"
        )


@router.post(
    "/save",
    response_model=SaveResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "バリデーションエラー"},
    },
)
async def save_saju(
    saju: SajuResponse,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    命式保存エンドポイント

    計算済みの命式をPostgreSQLに保存（UPSERT処理）
    既に存在する場合はuser_idを更新、存在しない場合は新規作成
    """
    try:
        # birth_datetimeをdatetimeオブジェクトに変換
        birth_datetime = datetime.fromisoformat(saju.birthDatetime.replace("Z", "+00:00"))

        # 吉凶レベルを数値に変換
        fortune_level_map = {"大凶": 1, "凶": 2, "平": 3, "吉凶": 4, "吉": 5, "小吉": 6, "大吉": 7}
        fortune_level_int = fortune_level_map.get(saju.fortuneLevel, 3)

        # daeunListをJSON文字列に変換
        daeun_list_json = json.dumps([d.model_dump() for d in saju.daeunList], ensure_ascii=False)

        # 既存レコードを確認
        existing_saju = db.query(SajuModel).filter(SajuModel.id == saju.id).first()

        if existing_saju:
            # 既存レコードが存在する場合はuser_idを更新（ゲスト→ログインユーザー）
            existing_saju.user_id = current_user.id
            existing_saju.name = saju.name
            existing_saju.updated_at = datetime.now()
            db.commit()
            db.refresh(existing_saju)
            return SaveResponse(success=True, id=existing_saju.id, message="命式を保存しました")
        else:
            # 新規レコードを作成
            db_saju = SajuModel(
                id=saju.id,
                user_id=current_user.id,
                name=saju.name,
                birth_datetime=birth_datetime,
                gender=saju.gender,
                year_stem=saju.yearStem,
                year_branch=saju.yearBranch,
                month_stem=saju.monthStem,
                month_branch=saju.monthBranch,
                day_stem=saju.dayStem,
                day_branch=saju.dayBranch,
                hour_stem=saju.hourStem,
                hour_branch=saju.hourBranch,
                daeun_list=daeun_list_json,
                fortune_level=fortune_level_int,
            )

            # DB保存
            db.add(db_saju)
            db.commit()
            db.refresh(db_saju)

            return SaveResponse(success=True, id=db_saju.id, message="命式を保存しました")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"命式データが不正です: {str(e)}")


@router.get(
    "/list",
    response_model=SajuListResponse,
    status_code=status.HTTP_200_OK,
)
async def get_saju_list(
    page: int = 1,
    limit: int = 20,
    sortBy: str = "createdAt",
    order: str = "desc",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    命式リスト取得エンドポイント

    ログインユーザーの命式一覧を取得
    ページネーション、ソート機能付き
    """
    try:
        # セッションのキャッシュをクリア（最新のデータを取得するため）
        db.expire_all()

        # バリデーション
        if limit > 100:
            limit = 100
        if page < 1:
            page = 1

        # ログインユーザーの命式を取得
        query = db.query(SajuModel).filter(SajuModel.user_id == current_user.id)

        # ソート処理
        if sortBy == "createdAt":
            query = query.order_by(
                SajuModel.created_at.desc() if order == "desc" else SajuModel.created_at.asc()
            )
        elif sortBy == "birthDatetime":
            query = query.order_by(
                SajuModel.birth_datetime.desc()
                if order == "desc"
                else SajuModel.birth_datetime.asc()
            )
        elif sortBy == "fortuneLevel":
            query = query.order_by(
                SajuModel.fortune_level.desc() if order == "desc" else SajuModel.fortune_level.asc()
            )

        # 総件数取得
        total = query.count()
        print(f"[LIST] user_id={current_user.id}, total={total}, page={page}, limit={limit}")

        # ページネーション
        offset = (page - 1) * limit
        items_db = query.offset(offset).limit(limit).all()

        # 吉凶レベルを文字列に変換
        fortune_level_reverse_map = {1: "大凶", 2: "凶", 3: "平", 4: "吉凶", 5: "吉", 6: "小吉", 7: "大吉"}

        items = []
        for item in items_db:
            fortune_level_str = fortune_level_reverse_map.get(item.fortune_level, "平")
            items.append(
                SajuSummary(
                    id=item.id,
                    name=item.name,
                    birthDatetime=item.birth_datetime.isoformat(),
                    gender=item.gender,
                    fortuneLevel=fortune_level_str,
                    createdAt=item.created_at.isoformat(),
                    yearStem=item.year_stem,
                    yearBranch=item.year_branch,
                    monthStem=item.month_stem,
                    monthBranch=item.month_branch,
                    dayStem=item.day_stem,
                    dayBranch=item.day_branch,
                    hourStem=item.hour_stem,
                    hourBranch=item.hour_branch,
                )
            )

        # 次のページが存在するか
        has_next = (page * limit) < total

        return SajuListResponse(items=items, total=total, page=page, limit=limit, hasNext=has_next)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"リスト取得中にエラーが発生しました: {str(e)}"
        )


# ==================== データ管理エンドポイント ====================


@router.get(
    "/export",
    response_model=ExportResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "認証が必要です"},
    },
)
async def export_saju_data(
    response: Response,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    データエクスポートエンドポイント

    ログインユーザーの全命式データをJSON形式でエクスポート
    """
    try:
        # ログインユーザーの命式を全て取得（created_at降順）
        sajus_db = (
            db.query(SajuModel)
            .filter(SajuModel.user_id == current_user.id)
            .order_by(SajuModel.created_at.desc())
            .all()
        )

        # ExportSajuItemのリストを作成
        export_items = []
        for saju_db in sajus_db:
            saju_dict = {
                "year_stem": saju_db.year_stem,
                "year_branch": saju_db.year_branch,
                "month_stem": saju_db.month_stem,
                "month_branch": saju_db.month_branch,
                "day_stem": saju_db.day_stem,
                "day_branch": saju_db.day_branch,
                "hour_stem": saju_db.hour_stem,
                "hour_branch": saju_db.hour_branch,
            }

            export_item = ExportSajuItem(
                id=saju_db.id,
                name=saju_db.name,
                birth_datetime=saju_db.birth_datetime.isoformat(),
                gender=saju_db.gender,
                saju=saju_dict,
                created_at=saju_db.created_at.isoformat(),
            )
            export_items.append(export_item)

        # 現在日時を取得
        now = datetime.now()
        exported_at = now.isoformat()

        # ファイル名用の日付（YYYYMMDD形式）
        filename_date = now.strftime("%Y%m%d")

        # Content-Dispositionヘッダーを設定
        response.headers["Content-Disposition"] = f'attachment; filename="saju_export_{filename_date}.json"'

        # エクスポートレスポンスを構築
        export_response = ExportResponse(
            exported_at=exported_at,
            user_id=current_user.id,
            count=len(export_items),
            data=export_items,
        )

        return export_response

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"エクスポート中にエラーが発生しました: {str(e)}",
        )


@router.post(
    "/import",
    response_model=ImportResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ImportResponse, "description": "ファイル形式が正しくありません"},
        401: {"model": ErrorResponse, "description": "認証が必要です"},
    },
)
async def import_saju_data(import_data: ExportData, db: Session = Depends(get_db)):
    """
    データインポートエンドポイント

    JSON形式の命式データをインポート。重複チェック後にマージ
    トランザクション管理（全成功または全失敗）
    """
    try:
        # バージョンチェック
        if import_data.version != "1.0.0":
            return ImportResponse(
                success=False,
                importedCount=0,
                message=f"サポートされていないバージョンです: {import_data.version}",
            )

        # 既存のIDを取得（重複チェック用）
        # TODO: 認証実装後は current_user.id でフィルタリング
        existing_ids_query = db.query(SajuModel.id).filter(SajuModel.user_id.is_(None)).all()
        existing_ids = {row[0] for row in existing_ids_query}

        # 重複していないデータのみをフィルタリング
        new_data = [item for item in import_data.data if item.id not in existing_ids]

        if len(new_data) == 0:
            return ImportResponse(
                success=True,
                importedCount=0,
                message="インポートする新しいデータがありません（全て重複）",
            )

        # 吉凶レベルを数値に変換
        fortune_level_map = {"大凶": 1, "凶": 2, "平": 3, "吉": 4, "大吉": 5}

        # トランザクション開始（全成功または全失敗）
        imported_count = 0
        for saju in new_data:
            # birth_datetimeをdatetimeオブジェクトに変換
            birth_datetime = datetime.fromisoformat(saju.birthDatetime.replace("Z", "+00:00"))

            # 吉凶レベルを数値に変換
            fortune_level_int = fortune_level_map.get(saju.fortuneLevel, 3)

            # daeunListをJSON文字列に変換
            daeun_list_json = json.dumps(
                [d.model_dump() for d in saju.daeunList], ensure_ascii=False
            )

            # SQLAlchemyモデル作成
            db_saju = SajuModel(
                id=saju.id,
                user_id=current_user.id,
                name=saju.name,
                birth_datetime=birth_datetime,
                gender=saju.gender,
                year_stem=saju.yearStem,
                year_branch=saju.yearBranch,
                month_stem=saju.monthStem,
                month_branch=saju.monthBranch,
                day_stem=saju.dayStem,
                day_branch=saju.dayBranch,
                hour_stem=saju.hourStem,
                hour_branch=saju.hourBranch,
                daeun_list=daeun_list_json,
                fortune_level=fortune_level_int,
            )

            db.add(db_saju)
            imported_count += 1

        # 全てのデータをコミット
        db.commit()

        return ImportResponse(
            success=True,
            importedCount=imported_count,
            message=f"{imported_count}件のデータをインポートしました",
        )

    except json.JSONDecodeError as e:
        db.rollback()
        return ImportResponse(
            success=False,
            importedCount=0,
            message="ファイル形式が正しくありません（JSON解析エラー）",
        )
    except ValueError as e:
        db.rollback()
        return ImportResponse(
            success=False,
            importedCount=0,
            message=f"データ形式が正しくありません: {str(e)}",
        )
    except Exception as e:
        db.rollback()
        return ImportResponse(
            success=False,
            importedCount=0,
            message=f"インポート中にエラーが発生しました: {str(e)}",
        )


@router.get(
    "/current-fortune",
    response_model=CurrentFortuneResponse,
    summary="今日の運勢を取得",
)
async def get_current_fortune(
    birth_year: int,
    birth_month: int,
    birth_day: int,
    birth_hour: int,
    birth_minute: int,
    gender: str,
    calculator: SajuCalculator = Depends(get_calculator),
) -> CurrentFortuneResponse:
    """
    今日の年運・月運・日運の干支と吉凶レベルを計算して返す

    Args:
        birth_year: 生年
        birth_month: 生月
        birth_day: 生日
        birth_hour: 生時
        birth_minute: 生分
        gender: 性別 ('male' or 'female')

    Returns:
        CurrentFortuneResponse: 今日の年・月・日運情報
    """
    try:
        # 今日の日付を取得（KST = UTC+9）
        from datetime import datetime
        from zoneinfo import ZoneInfo

        now = datetime.now(ZoneInfo("Asia/Seoul"))
        today_str = now.strftime("%Y-%m-%d")

        # ユーザーの命式を計算して日干を取得
        from lunar_python import Solar as UserSolar

        user_solar = UserSolar.fromYmdHms(birth_year, birth_month, birth_day, birth_hour, birth_minute, 0)
        user_lunar = user_solar.getLunar()
        user_eight_char = user_lunar.getEightChar()
        user_day_stem = user_eight_char.getDayGan()  # ユーザーの日干

        # 今日の年・月・日の干支を取得
        from lunar_python import Solar

        solar = Solar.fromYmdHms(now.year, now.month, now.day, now.hour, 0, 0)
        lunar = solar.getLunar()
        eight_char = lunar.getEightChar()

        # 年・月・日の干支を取得
        year_stem = eight_char.getYearGan()  # 年干
        year_branch = eight_char.getYearZhi()  # 年支
        month_stem = eight_char.getMonthGan()  # 月干
        month_branch = eight_char.getMonthZhi()  # 月支
        day_stem = eight_char.getDayGan()  # 日干
        day_branch = eight_char.getDayZhi()  # 日支

        # 吉凶レベルを計算（ユーザーの日干を基準に判定）
        from app.services.fortune_analyzer import FortuneAnalyzer

        fortune_analyzer = FortuneAnalyzer()

        # 年運の吉凶レベル（ユーザーの日干 vs 今年の年干）
        year_tengan_level = fortune_analyzer.tengan_matrix.get(user_day_stem, {}).get(year_stem, "平")
        year_fortune_level = year_tengan_level

        # 月運の吉凶レベル（ユーザーの日干 vs 今月の月干）
        month_tengan_level = fortune_analyzer.tengan_matrix.get(user_day_stem, {}).get(month_stem, "平")
        month_fortune_level = month_tengan_level

        # 日運の吉凶レベル（ユーザーの日干 vs 今日の日干）
        day_tengan_level = fortune_analyzer.tengan_matrix.get(user_day_stem, {}).get(day_stem, "平")
        day_fortune_level = day_tengan_level

        # FortuneDetailを構築
        year_fortune = FortuneDetail(
            stem=year_stem,
            branch=year_branch,
            fortuneLevel=year_fortune_level,
            description="年運",
        )

        month_fortune = FortuneDetail(
            stem=month_stem,
            branch=month_branch,
            fortuneLevel=month_fortune_level,
            description="月運",
        )

        day_fortune = FortuneDetail(
            stem=day_stem,
            branch=day_branch,
            fortuneLevel=day_fortune_level,
            description="日運",
        )

        return CurrentFortuneResponse(
            date=today_str,
            yearFortune=year_fortune,
            monthFortune=month_fortune,
            dayFortune=day_fortune,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"今日の運勢の計算に失敗しました: {str(e)}"
        )


@router.get(
    "/{id}",
    response_model=SajuResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "命式が見つかりません"},
    },
)
async def get_saju_detail(id: str, db: Session = Depends(get_db)):
    """
    命式詳細取得エンドポイント

    指定された命式IDの詳細情報を取得
    """
    try:
        # DBから命式を取得
        saju_db = db.query(SajuModel).filter(SajuModel.id == id).first()

        if not saju_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="命式が見つかりません")

        # 吉凶レベルを文字列に変換
        fortune_level_reverse_map = {1: "大凶", 2: "凶", 3: "平", 4: "吉凶", 5: "吉", 6: "小吉", 7: "大吉"}
        fortune_level_str = fortune_level_reverse_map.get(saju_db.fortune_level, "平")

        # daeunListをJSONから復元
        daeun_list = []
        if saju_db.daeun_list:
            daeun_list_data = json.loads(saju_db.daeun_list)
            daeun_list = [DaeunInfo(**d) for d in daeun_list_data]

        # レスポンス構築
        response = SajuResponse(
            id=saju_db.id,
            name=saju_db.name,
            birthDatetime=saju_db.birth_datetime.isoformat(),
            gender=saju_db.gender,
            yearStem=saju_db.year_stem,
            yearBranch=saju_db.year_branch,
            monthStem=saju_db.month_stem,
            monthBranch=saju_db.month_branch,
            dayStem=saju_db.day_stem,
            dayBranch=saju_db.day_branch,
            hourStem=saju_db.hour_stem,
            hourBranch=saju_db.hour_branch,
            daeunList=daeun_list,
            fortuneLevel=fortune_level_str,
            createdAt=saju_db.created_at.isoformat(),
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"命式詳細取得中にエラーが発生しました: {str(e)}",
        )


@router.delete(
    "/{id}",
    response_model=DeleteResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "認証が必要です"},
        403: {"model": ErrorResponse, "description": "この命式にアクセスする権限がありません"},
        404: {"model": ErrorResponse, "description": "命式が見つかりません"},
    },
)
async def delete_saju(
    id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    命式削除エンドポイント

    指定された命式IDのデータを削除
    認証必須、自分の命式のみ削除可能
    """
    try:
        # DBから命式を取得
        saju_db = db.query(SajuModel).filter(SajuModel.id == id).first()

        # 存在チェック
        if not saju_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="命式が見つかりません"
            )

        # 権限チェック（自分の命式のみ削除可能）
        if saju_db.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="この命式にアクセスする権限がありません"
            )

        # 削除前のカウント
        count_before = db.query(SajuModel).filter(SajuModel.user_id == current_user.id).count()
        print(f"[DELETE] 削除前のカウント: {count_before}, 削除対象ID: {id}")

        # 削除実行
        db.delete(saju_db)
        db.commit()

        # セッションのキャッシュをクリア（削除が即座に反映されるようにする）
        db.expire_all()

        # 削除後のカウント（デバッグ用）
        count_after = db.query(SajuModel).filter(SajuModel.user_id == current_user.id).count()
        print(f"[DELETE] 削除後のカウント: {count_after}")

        # レスポンスメッセージに削除後のカウントを含める（デバッグ用）
        message = f"命式を削除しました（残り{count_after}件）"

        return DeleteResponse(success=True, message=message)

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"削除中にエラーが発生しました: {str(e)}"
        )


# ==================== 大運分析エンドポイント ====================


@router.get(
    "/{id}/daeun",
    response_model=DaeunAnalysisResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "命式が見つかりません"},
    },
)
async def get_daeun_analysis(id: str, db: Session = Depends(get_db)):
    """
    大運分析取得エンドポイント

    指定された命式IDの大運分析情報を取得
    """
    try:
        # DBから命式を取得
        saju_db = db.query(SajuModel).filter(SajuModel.id == id).first()

        if not saju_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="命式が見つかりません")

        # daeunListをJSONから復元
        daeun_list_data = json.loads(saju_db.daeun_list) if saju_db.daeun_list else []
        daeun_list = [DaeunInfo(**d) for d in daeun_list_data]

        # 現在の年齢を計算
        birth_datetime = saju_db.birth_datetime
        today = datetime.now()
        current_age = today.year - birth_datetime.year
        if (today.month, today.day) < (birth_datetime.month, birth_datetime.day):
            current_age -= 1

        # 各大運にisCurrentフラグを設定
        for daeun in daeun_list:
            daeun.isCurrent = daeun.startAge <= current_age <= daeun.endAge

        # 大運計算情報を取得（calculate時に保存されているはず）
        # TODO: DBに保存されていない場合は再計算が必要
        daeun_number = 7  # デフォルト値（実際はDBから取得）
        is_forward = True  # デフォルト値（実際はDBから取得）
        after_birth_years = 7
        after_birth_months = 5
        after_birth_days = 2
        first_daeun_date = "1997-08-17"  # デフォルト値（実際はDBから取得）

        response = DaeunAnalysisResponse(
            daeunNumber=daeun_number,
            isForward=is_forward,
            afterBirth=AfterBirth(
                years=after_birth_years, months=after_birth_months, days=after_birth_days
            ),
            firstDaeunDate=first_daeun_date,
            currentAge=current_age,
            daeunList=daeun_list,
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"大運分析取得中にエラーが発生しました: {str(e)}",
        )


@router.get(
    "/{id}/current",
    response_model=CurrentFortuneResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "命式が見つかりません"},
    },
)
async def get_current_fortune(id: str, date: str = None, db: Session = Depends(get_db)):
    """
    現在の運勢取得エンドポイント

    指定された命式IDの現在の年運・月運・日運を取得
    """
    try:
        # DBから命式を取得
        saju_db = db.query(SajuModel).filter(SajuModel.id == id).first()

        if not saju_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="命式が見つかりません")

        # 対象日付（省略時は今日）
        target_date = datetime.fromisoformat(date) if date else datetime.now()

        # 年月日運計算エンジン
        fortune_calc = get_fortune_calculator()

        # 生年月日を取得
        birth_datetime = saju_db.birth_datetime

        # 実際の年柱・月柱を取得（今日の運用）
        year_stem, year_branch = fortune_calc.get_actual_year_pillar(
            target_date.year,
            target_date.month,
            target_date.day,
        )
        month_stem, month_branch = fortune_calc.get_actual_month_pillar(
            target_date.year,
            target_date.month,
            target_date.day,
        )

        # 日運計算
        day_stem, day_branch, day_fortune_level, day_sipsin = fortune_calc.calculate_day_fortune(
            saju_db.day_stem,
            target_date.year,
            target_date.month,
            target_date.day,
        )

        # 年運・月運の吉凶判定と十神計算
        year_fortune_level = fortune_calc._calculate_fortune_level(
            saju_db.day_stem, year_stem, year_branch
        )
        year_sipsin = fortune_calc._calculate_sipsin(saju_db.day_stem, year_stem)

        month_fortune_level = fortune_calc._calculate_fortune_level(
            saju_db.day_stem, month_stem, month_branch
        )
        month_sipsin = fortune_calc._calculate_sipsin(saju_db.day_stem, month_stem)

        # 五行要素を取得
        year_element = fortune_calc.get_element_from_stem(year_stem)
        month_element = fortune_calc.get_element_from_stem(month_stem)
        day_element = fortune_calc.get_element_from_stem(day_stem)

        response = CurrentFortuneResponse(
            date=target_date.strftime("%Y-%m-%d"),
            yearFortune=FortuneDetail(
                stem=year_stem,
                branch=year_branch,
                fortuneLevel=year_fortune_level,
                description=f"{year_stem}{year_branch}年の運勢",
                element=year_element,
            ),
            monthFortune=FortuneDetail(
                stem=month_stem,
                branch=month_branch,
                fortuneLevel=month_fortune_level,
                description=f"{month_stem}{month_branch}月の運勢",
                element=month_element,
            ),
            dayFortune=FortuneDetail(
                stem=day_stem,
                branch=day_branch,
                fortuneLevel=day_fortune_level,
                description=f"{day_stem}{day_branch}日の運勢",
                element=day_element,
            ),
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"現在の運勢取得中にエラーが発生しました: {str(e)}",
        )


@router.get(
    "/{id}/year/{daeun_start_age}",
    response_model=YearFortuneListResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "命式が見つかりません"},
    },
)
async def get_year_fortune_list(id: str, daeun_start_age: int, db: Session = Depends(get_db)):
    """
    年運リスト取得エンドポイント

    指定された大運期間（10年分）の年運リストを取得
    """
    try:
        # DBから命式を取得
        saju_db = db.query(SajuModel).filter(SajuModel.id == id).first()

        if not saju_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="命式が見つかりません")

        # 年月日運計算エンジン
        fortune_calc = get_fortune_calculator()

        # 生年月日を取得
        birth_datetime = saju_db.birth_datetime

        # 年運リストを計算（10年分）
        year_list_data = fortune_calc.calculate_year_list(
            birth_datetime.year,
            birth_datetime.month,
            birth_datetime.day,
            saju_db.day_stem,
            daeun_start_age,
        )

        # YearFortuneInfoに変換
        year_list = [
            YearFortuneInfo(sajuId=id, daeunStartAge=daeun_start_age, **year)
            for year in year_list_data
        ]

        response = YearFortuneListResponse(
            daeunStartAge=daeun_start_age,
            daeunEndAge=daeun_start_age + 9,
            years=year_list,
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"年運リスト取得中にエラーが発生しました: {str(e)}",
        )


@router.get(
    "/{id}/month/{year}",
    response_model=MonthFortuneListResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "命式が見つかりません"},
    },
)
async def get_month_fortune_list(id: str, year: int, db: Session = Depends(get_db)):
    """
    月運リスト取得エンドポイント

    指定された年の月運リスト（12ヶ月分）を取得
    """
    try:
        # DBから命式を取得
        saju_db = db.query(SajuModel).filter(SajuModel.id == id).first()

        if not saju_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="命式が見つかりません")

        # 年月日運計算エンジン
        fortune_calc = get_fortune_calculator()

        # 月運リストを計算（12ヶ月分）
        month_list_data = fortune_calc.calculate_month_list(
            saju_db.day_stem,
            year,
        )

        # MonthFortuneInfoに変換
        month_list = [MonthFortuneInfo(sajuId=id, **month) for month in month_list_data]

        response = MonthFortuneListResponse(
            year=year,
            months=month_list,
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"月運リスト取得中にエラーが発生しました: {str(e)}",
        )


@router.get(
    "/{id}/day/{year}/{month}",
    response_model=DayFortuneListResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "不正な年月指定です"},
        404: {"model": ErrorResponse, "description": "命式が見つかりません"},
    },
)
async def get_day_fortune_list(id: str, year: int, month: int, db: Session = Depends(get_db)):
    """
    日運リスト取得エンドポイント

    指定された年月の日運リスト（28-31日分）を取得
    """
    try:
        # 月のバリデーション
        if not (1 <= month <= 12):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="不正な年月指定です")

        # DBから命式を取得
        saju_db = db.query(SajuModel).filter(SajuModel.id == id).first()

        if not saju_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="命式が見つかりません")

        # 年月日運計算エンジン
        fortune_calc = get_fortune_calculator()

        # 日運リストを計算（28-31日分）
        day_list_data = fortune_calc.calculate_day_list(
            saju_db.day_stem,
            year,
            month,
        )

        # DayFortuneInfoに変換
        day_list = [DayFortuneInfo(sajuId=id, **day) for day in day_list_data]

        response = DayFortuneListResponse(
            year=year,
            month=month,
            days=day_list,
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"日運リスト取得中にエラーが発生しました: {str(e)}",
        )


# ==================== データ移行エンドポイント ====================


@router.post(
    "/migrate",
    response_model=MigrateResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": MigrateResponse, "description": "移行データが不正です"},
        401: {"model": ErrorResponse, "description": "認証が必要です"},
    },
)
async def migrate_guest_data(
    migrate_data: MigrateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    ゲストデータ移行エンドポイント

    LocalStorageに保存されたゲストデータをログインユーザーに紐付け
    トランザクション管理（全成功または全失敗）
    """
    try:
        # データバリデーション
        if not migrate_data.guestData:
            return MigrateResponse(
                success=False,
                migratedCount=0,
                message="移行データが空です",
            )

        if len(migrate_data.guestData) > 100:
            return MigrateResponse(
                success=False,
                migratedCount=0,
                message="一度に移行できるデータは100件までです",
            )

        # 吉凶レベルを数値に変換
        fortune_level_map = {"大凶": 1, "凶": 2, "平": 3, "吉": 4, "大吉": 5}

        # 重複チェック（birth_datetime + gender の組み合わせ）
        existing_data_query = (
            db.query(SajuModel.birth_datetime, SajuModel.gender)
            .filter(SajuModel.user_id == current_user.id)
            .all()
        )
        # タイムスタンプを文字列化して比較（タイムゾーン情報を正規化）
        existing_keys = set()
        for row in existing_data_query:
            # タイムゾーン情報がない場合はそのまま、ある場合はUTCに変換
            dt = row[0]
            if dt.tzinfo is None:
                normalized_dt = dt.isoformat()
            else:
                normalized_dt = dt.replace(tzinfo=None).isoformat()
            existing_keys.add((normalized_dt, row[1]))

        # 重複していないデータのみフィルタリング
        unique_data = []
        for saju in migrate_data.guestData:
            birth_datetime = datetime.fromisoformat(saju.birthDatetime.replace("Z", "+00:00"))
            key = (birth_datetime.replace(tzinfo=None).isoformat(), saju.gender)
            if key not in existing_keys:
                unique_data.append(saju)

        if len(unique_data) == 0:
            return MigrateResponse(
                success=True,
                migratedCount=0,
                message="移行する新しいデータがありません（全て重複）",
            )

        # トランザクション開始（全成功または全失敗）
        migrated_count = 0
        for saju in unique_data:
            # 新しいIDを生成（ゲストIDは使用しない）
            new_id = f"saju-{uuid.uuid4()}"

            # birth_datetimeをdatetimeオブジェクトに変換
            birth_datetime = datetime.fromisoformat(saju.birthDatetime.replace("Z", "+00:00"))

            # 吉凶レベルを数値に変換
            fortune_level_int = fortune_level_map.get(saju.fortuneLevel, 3)

            # daeunListのsajuIdを新しいIDに更新
            daeun_list_updated = []
            for daeun in saju.daeunList:
                daeun_dict = daeun.model_dump()
                daeun_dict["sajuId"] = new_id
                daeun_list_updated.append(daeun_dict)

            # daeunListをJSON文字列に変換
            daeun_list_json = json.dumps(daeun_list_updated, ensure_ascii=False)

            # SQLAlchemyモデル作成
            db_saju = SajuModel(
                id=new_id,
                user_id=current_user.id,  # ログインユーザーに紐付け
                name=saju.name,
                birth_datetime=birth_datetime,
                gender=saju.gender,
                year_stem=saju.yearStem,
                year_branch=saju.yearBranch,
                month_stem=saju.monthStem,
                month_branch=saju.monthBranch,
                day_stem=saju.dayStem,
                day_branch=saju.dayBranch,
                hour_stem=saju.hourStem,
                hour_branch=saju.hourBranch,
                daeun_list=daeun_list_json,
                fortune_level=fortune_level_int,
            )

            db.add(db_saju)
            migrated_count += 1

        # 全てのデータをコミット
        db.commit()

        return MigrateResponse(
            success=True,
            migratedCount=migrated_count,
            message=f"{migrated_count}件のデータを移行しました",
        )

    except json.JSONDecodeError as e:
        db.rollback()
        return MigrateResponse(
            success=False,
            migratedCount=0,
            message="移行データの形式が正しくありません（JSON解析エラー）",
        )
    except ValueError as e:
        db.rollback()
        return MigrateResponse(
            success=False,
            migratedCount=0,
            message=f"移行データの形式が正しくありません: {str(e)}",
        )
    except Exception as e:
        db.rollback()
        return MigrateResponse(
            success=False,
            migratedCount=0,
            message=f"移行中にエラーが発生しました: {str(e)}",
        )
