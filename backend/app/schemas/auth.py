"""
認証用Pydanticスキーマ
フロントエンドの型定義（frontend/src/types/index.ts）と同期
"""
from typing import List, Optional

from pydantic import BaseModel, EmailStr


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

    email: EmailStr
    password: str
    rememberMe: Optional[bool] = False


class RegisterRequest(BaseModel):
    """新規登録リクエスト"""

    email: EmailStr
    password: str
    name: str  # プロフィール名
    migrateGuestData: Optional[bool] = False


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
