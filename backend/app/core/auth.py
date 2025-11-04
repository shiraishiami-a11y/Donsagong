"""
JWT認証ユーティリティ
トークン生成・検証・パスワードハッシュ化
"""
import secrets
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# パスワードハッシュ化設定（bcrypt）
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ==================== パスワード処理 ====================


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """パスワード検証"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """パスワードハッシュ化"""
    return pwd_context.hash(password)


# ==================== JWT トークン処理 ====================


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    アクセストークン生成

    Args:
        data: ペイロードデータ（user_id, email, role等）
        expires_delta: 有効期限（Noneの場合は設定値を使用）

    Returns:
        JWT文字列
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
    })

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token() -> str:
    """
    リフレッシュトークン生成（ランダム文字列）

    Returns:
        ランダムトークン文字列
    """
    return secrets.token_urlsafe(32)


def decode_access_token(token: str) -> Optional[dict]:
    """
    アクセストークン検証・デコード

    Args:
        token: JWT文字列

    Returns:
        デコードされたペイロード（失敗時はNone）
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


# ==================== 権限チェック ====================


def get_permissions_for_role(role: str) -> list[str]:
    """
    ロールに応じた権限リストを返す

    Args:
        role: 'guest', 'user', 'admin'

    Returns:
        権限リスト
    """
    if role == "admin":
        return ["read", "write", "delete", "admin"]
    elif role == "user":
        return ["read", "write"]
    elif role == "guest":
        return ["read"]
    else:
        return []
