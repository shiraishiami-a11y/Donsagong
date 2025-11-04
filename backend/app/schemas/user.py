"""
ユーザー設定用Pydanticスキーマ
フロントエンドの型定義（frontend/src/types/index.ts）と同期
"""
from typing import Literal

from pydantic import BaseModel, Field


# ==================== ユーザー設定関連 ====================


class PasswordChangeRequest(BaseModel):
    """パスワード変更リクエスト"""

    oldPassword: str = Field(..., min_length=1, description="現在のパスワード")
    newPassword: str = Field(..., min_length=8, description="新しいパスワード（8文字以上）")


class UserSettingsRequest(BaseModel):
    """ユーザー設定更新リクエスト"""

    rememberMe: bool = Field(..., description="ログイン状態を保持")
    sessionDuration: Literal["7d", "30d", "forever"] = Field(
        ..., description="セッション期間（7日/30日/無期限）"
    )


class UpdateResponse(BaseModel):
    """更新成功レスポンス"""

    success: bool = Field(..., description="成功フラグ")
    message: str = Field(..., description="メッセージ")
