"""
認証用Pydanticスキーマ
フロントエンドの型定義（frontend/src/types/index.ts）と同期
"""
import re
from typing import List, Optional

from pydantic import BaseModel, field_validator


# ==================== ユーザー関連 ====================


class UserProfile(BaseModel):
    """ユーザープロフィール"""

    name: str
    avatar: Optional[str] = None


class UserResponse(BaseModel):
    """ユーザー情報レスポンス"""

    id: str
    email: str
    role: str  # 'guest', 'user', 'admin'
    permissions: List[str]
    profile: UserProfile
    createdAt: str

    model_config = {"from_attributes": True}


# ==================== 認証関連 ====================


class LoginRequest(BaseModel):
    """ログインリクエスト"""

    email: str
    password: str
    rememberMe: Optional[bool] = False

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        """メールアドレスのバリデーション（.localドメイン許可）"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        local_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.local$'

        if not (re.match(email_pattern, v) or re.match(local_pattern, v)):
            raise ValueError('有効なメールアドレスを入力してください')
        return v.lower()


class RegisterRequest(BaseModel):
    """新規登録リクエスト"""

    email: str
    password: str
    name: Optional[str] = None  # プロフィール名（任意）
    migrateGuestData: Optional[bool] = False

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        """メールアドレスのバリデーション（.localドメイン許可）"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        local_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.local$'

        if not (re.match(email_pattern, v) or re.match(local_pattern, v)):
            raise ValueError('有効なメールアドレスを入力してください')
        return v.lower()


class AuthResponse(BaseModel):
    """認証レスポンス（ログイン・新規登録共通）"""

    accessToken: str
    refreshToken: str
    user: UserResponse


class LogoutResponse(BaseModel):
    """ログアウトレスポンス"""

    success: bool
    message: str


class RefreshTokenRequest(BaseModel):
    """リフレッシュトークンリクエスト"""

    refreshToken: str


class RefreshTokenResponse(BaseModel):
    """リフレッシュトークンレスポンス"""

    accessToken: str
    refreshToken: str
