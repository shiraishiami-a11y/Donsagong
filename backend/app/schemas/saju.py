"""
命式API用のPydanticスキーマ定義
frontend/src/types/index.ts と完全同期
"""
from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, field_validator


# ==================== リクエストスキーマ ====================


class BirthDataRequest(BaseModel):
    """命式計算リクエスト"""

    birthDatetime: str = Field(..., description="生年月日時（ISO 8601形式）")
    gender: Literal["male", "female"] = Field(..., description="性別")
    name: Optional[str] = Field(None, description="名前（オプション）")
    timezoneOffset: Optional[int] = Field(9, description="タイムゾーンオフセット（KST=9）")

    @field_validator("birthDatetime")
    @classmethod
    def validate_datetime(cls, v: str) -> str:
        """ISO 8601形式の日時をバリデーション"""
        try:
            # ISO 8601パース可能かチェック
            datetime.fromisoformat(v.replace("Z", "+00:00"))
            return v
        except ValueError:
            raise ValueError("birthDatetimeはISO 8601形式である必要があります")


# ==================== レスポンススキーマ ====================


class DaeunInfo(BaseModel):
    """大運情報"""

    id: int = Field(..., description="大運ID")
    sajuId: str = Field(..., description="命式ID")
    startAge: int = Field(..., description="開始年齢")
    endAge: int = Field(..., description="終了年齢")
    daeunStem: str = Field(..., description="大運天干")
    daeunBranch: str = Field(..., description="大運地支")
    fortuneLevel: Literal["大吉", "吉", "平", "凶", "大凶"] = Field(..., description="吉凶レベル")
    sipsin: Optional[str] = Field(None, description="十神")
    isCurrent: Optional[bool] = Field(False, description="現在の大運期間かどうか")


class SajuResponse(BaseModel):
    """命式計算結果レスポンス"""

    id: str = Field(..., description="命式ID（UUID）")
    name: Optional[str] = Field(None, description="名前")
    birthDatetime: str = Field(..., description="生年月日時（ISO 8601形式）")
    gender: str = Field(..., description="性別")

    # 四柱（年・月・日・時）
    yearStem: str = Field(..., description="年天干")
    yearBranch: str = Field(..., description="年地支")
    monthStem: str = Field(..., description="月天干")
    monthBranch: str = Field(..., description="月地支")
    dayStem: str = Field(..., description="日天干")
    dayBranch: str = Field(..., description="日地支")
    hourStem: str = Field(..., description="時天干")
    hourBranch: str = Field(..., description="時地支")

    # 大運計算情報
    daeunNumber: Optional[int] = Field(None, description="大運数")
    isForward: Optional[bool] = Field(None, description="順行（true）/逆行（false）")
    afterBirthYears: Optional[int] = Field(None, description="生後年数")
    afterBirthMonths: Optional[int] = Field(None, description="生後月数")
    afterBirthDays: Optional[int] = Field(None, description="生後日数")
    firstDaeunDate: Optional[str] = Field(None, description="第一大運開始日（YYYY-MM-DD形式）")

    # 大運リスト
    daeunList: List[DaeunInfo] = Field(..., description="大運リスト")

    # 吉凶レベル
    fortuneLevel: Literal["大吉", "吉", "平", "凶", "大凶"] = Field(..., description="吉凶レベル")

    createdAt: str = Field(..., description="作成日時（ISO 8601形式）")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "saju-1730505600000",
                "name": "山田 太郎",
                "birthDatetime": "1990-03-15T14:30:00+09:00",
                "gender": "male",
                "yearStem": "庚",
                "yearBranch": "午",
                "monthStem": "己",
                "monthBranch": "卯",
                "dayStem": "丙",
                "dayBranch": "午",
                "hourStem": "乙",
                "hourBranch": "未",
                "daeunNumber": 7,
                "isForward": True,
                "afterBirthYears": 7,
                "afterBirthMonths": 5,
                "afterBirthDays": 2,
                "firstDaeunDate": "1997-08-17",
                "daeunList": [
                    {
                        "id": 1,
                        "sajuId": "saju-1730505600000",
                        "startAge": 8,
                        "endAge": 17,
                        "daeunStem": "乙",
                        "daeunBranch": "卯",
                        "fortuneLevel": "平",
                        "sipsin": "偏印",
                        "isCurrent": False,
                    }
                ],
                "fortuneLevel": "吉",
                "createdAt": "2025-11-02T10:00:00+09:00",
            }
        }


class SaveResponse(BaseModel):
    """保存成功レスポンス"""

    success: bool = Field(..., description="成功フラグ")
    id: str = Field(..., description="保存された命式ID")
    message: str = Field(..., description="メッセージ")


# ==================== エラーレスポンス ====================


class SajuSummary(BaseModel):
    """命式サマリー（リスト表示用）"""

    id: str = Field(..., description="命式ID")
    name: Optional[str] = Field(None, description="名前")
    birthDatetime: str = Field(..., description="生年月日時（ISO 8601形式）")
    gender: str = Field(..., description="性別")
    fortuneLevel: Literal["大吉", "吉", "平", "凶", "大凶"] = Field(..., description="吉凶レベル")
    createdAt: str = Field(..., description="作成日時（ISO 8601形式）")

    # 四柱プレビュー用
    yearStem: str = Field(..., description="年天干")
    yearBranch: str = Field(..., description="年地支")
    monthStem: str = Field(..., description="月天干")
    monthBranch: str = Field(..., description="月地支")
    dayStem: str = Field(..., description="日天干")
    dayBranch: str = Field(..., description="日地支")
    hourStem: str = Field(..., description="時天干")
    hourBranch: str = Field(..., description="時地支")


class SajuListResponse(BaseModel):
    """命式リスト取得レスポンス"""

    items: List[SajuSummary] = Field(..., description="命式サマリーリスト")
    total: int = Field(..., description="総件数")
    page: int = Field(..., description="現在のページ番号")
    limit: int = Field(..., description="1ページあたりの件数")
    hasNext: bool = Field(..., description="次のページが存在するか")


class DeleteResponse(BaseModel):
    """削除成功レスポンス"""

    success: bool = Field(..., description="成功フラグ")
    message: str = Field(..., description="メッセージ")


# ==================== エラーレスポンス ====================


class ErrorResponse(BaseModel):
    """エラーレスポンス"""

    error: str = Field(..., description="エラーメッセージ")


# ==================== 大運分析レスポンス ====================


class AfterBirth(BaseModel):
    """生後日時情報"""

    years: int = Field(..., description="生後年数")
    months: int = Field(..., description="生後月数")
    days: int = Field(..., description="生後日数")


class DaeunAnalysisResponse(BaseModel):
    """大運分析レスポンス"""

    daeunNumber: int = Field(..., description="大運数")
    isForward: bool = Field(..., description="順行（true）/逆行（false）")
    afterBirth: AfterBirth = Field(..., description="生後日時")
    firstDaeunDate: str = Field(..., description="第一大運開始日（YYYY-MM-DD形式）")
    currentAge: int = Field(..., description="現在年齢")
    daeunList: List[DaeunInfo] = Field(..., description="大運リスト")


# ==================== 年月日運レスポンス ====================


class FortuneDetail(BaseModel):
    """運勢詳細情報"""

    stem: str = Field(..., description="天干")
    branch: str = Field(..., description="地支")
    fortuneLevel: Literal["大吉", "吉", "平", "凶", "大凶"] = Field(..., description="吉凶レベル")
    description: str = Field(..., description="解説文")
    element: Optional[Literal["wood", "fire", "earth", "metal", "water"]] = Field(
        None, description="五行要素"
    )


class CurrentFortuneResponse(BaseModel):
    """現在の運勢レスポンス"""

    date: str = Field(..., description="対象日付（YYYY-MM-DD形式）")
    yearFortune: FortuneDetail = Field(..., description="年運")
    monthFortune: FortuneDetail = Field(..., description="月運")
    dayFortune: FortuneDetail = Field(..., description="日運")


class YearFortuneInfo(BaseModel):
    """年運情報"""

    id: int = Field(..., description="年運ID")
    sajuId: str = Field(..., description="命式ID")
    daeunStartAge: int = Field(..., description="所属する大運の開始年齢")
    year: int = Field(..., description="西暦年")
    age: int = Field(..., description="その年の年齢")
    yearStem: str = Field(..., description="年天干")
    yearBranch: str = Field(..., description="年地支")
    sipsin: str = Field(..., description="十神")
    fortuneLevel: Literal["大吉", "吉", "平", "凶", "大凶"] = Field(..., description="吉凶レベル")
    isCurrent: bool = Field(..., description="現在の年かどうか")


class YearFortuneListResponse(BaseModel):
    """年運リストレスポンス"""

    daeunStartAge: int = Field(..., description="大運開始年齢")
    daeunEndAge: int = Field(..., description="大運終了年齢")
    years: List[YearFortuneInfo] = Field(..., description="年運リスト")


class MonthFortuneInfo(BaseModel):
    """月運情報"""

    id: int = Field(..., description="月運ID")
    sajuId: str = Field(..., description="命式ID")
    year: int = Field(..., description="所属する年")
    month: int = Field(..., description="月（1-12）")
    monthStem: str = Field(..., description="月天干")
    monthBranch: str = Field(..., description="月地支")
    sipsin: str = Field(..., description="十神")
    fortuneLevel: Literal["大吉", "吉", "平", "凶", "大凶"] = Field(..., description="吉凶レベル")
    isCurrent: bool = Field(..., description="現在の月かどうか")


class MonthFortuneListResponse(BaseModel):
    """月運リストレスポンス"""

    year: int = Field(..., description="対象年")
    months: List[MonthFortuneInfo] = Field(..., description="月運リスト")


class DayFortuneInfo(BaseModel):
    """日運情報"""

    id: int = Field(..., description="日運ID")
    sajuId: str = Field(..., description="命式ID")
    year: int = Field(..., description="所属する年")
    month: int = Field(..., description="所属する月")
    day: int = Field(..., description="日（1-31）")
    dayStem: str = Field(..., description="日天干")
    dayBranch: str = Field(..., description="日地支")
    sipsin: str = Field(..., description="十神")
    fortuneLevel: Literal["大吉", "吉", "平", "凶", "大凶"] = Field(..., description="吉凶レベル")
    isToday: bool = Field(..., description="今日かどうか")


class DayFortuneListResponse(BaseModel):
    """日運リストレスポンス"""

    year: int = Field(..., description="対象年")
    month: int = Field(..., description="対象月")
    days: List[DayFortuneInfo] = Field(..., description="日運リスト")


# ==================== データ管理レスポンス ====================


class ExportSajuItem(BaseModel):
    """エクスポート用の命式データ"""

    id: str = Field(..., description="命式ID")
    name: Optional[str] = Field(None, description="名前")
    birth_datetime: str = Field(..., description="生年月日時（ISO 8601形式）")
    gender: str = Field(..., description="性別")
    saju: dict = Field(..., description="命式データ（天干・地支）")
    created_at: str = Field(..., description="作成日時（ISO 8601形式）")


class ExportResponse(BaseModel):
    """エクスポートレスポンス"""

    exported_at: str = Field(..., description="エクスポート日時（ISO 8601形式）")
    user_id: str = Field(..., description="ユーザーID")
    count: int = Field(..., description="エクスポートされた件数")
    data: List[ExportSajuItem] = Field(..., description="命式データリスト")


class ExportData(BaseModel):
    """エクスポートデータ（旧形式・互換性維持）"""

    version: str = Field(..., description="データバージョン（v1.0.0）")
    exportDate: str = Field(..., description="エクスポート日時（ISO 8601形式）")
    data: List[SajuResponse] = Field(..., description="命式データリスト")


class ImportResponse(BaseModel):
    """インポート成功レスポンス"""

    success: bool = Field(..., description="成功フラグ")
    importedCount: int = Field(..., description="インポートされた件数")
    message: str = Field(..., description="メッセージ")


class MigrateRequest(BaseModel):
    """ゲストデータ移行リクエスト"""

    guestData: List[SajuResponse] = Field(..., description="ゲストモードの命式データリスト")


class MigrateResponse(BaseModel):
    """データ移行成功レスポンス"""

    success: bool = Field(..., description="成功フラグ")
    migratedCount: int = Field(..., description="移行された件数")
    message: str = Field(..., description="メッセージ")
