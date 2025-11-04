"""
ユーザー設定APIルーター
PUT /api/user/password - パスワード変更
PUT /api/user/settings - ユーザー設定更新
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.api.auth import get_current_user, security
from app.core.auth import get_password_hash, verify_password
from app.db.session import get_db
from app.models import RefreshToken, User
from app.schemas.user import PasswordChangeRequest, UpdateResponse, UserSettingsRequest

router = APIRouter(prefix="/api/user", tags=["user"])


# ==================== エンドポイント ====================


@router.put("/password", response_model=UpdateResponse)
async def change_password(
    data: PasswordChangeRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """
    パスワード変更

    - 現在のパスワードを検証してから新しいパスワードに変更
    - パスワード変更後は全トークンを無効化（セキュリティ強化）

    Args:
        data: PasswordChangeRequest（oldPassword, newPassword）
        credentials: Bearer Token
        db: データベースセッション

    Returns:
        UpdateResponse（success, message）

    Raises:
        HTTPException 400: パスワードバリデーションエラー
        HTTPException 401: 現在のパスワードが正しくない
    """
    # 現在のユーザー取得
    current_user = get_current_user(credentials, db)

    # 現在のパスワード検証
    if not verify_password(data.oldPassword, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="現在のパスワードが正しくありません",
        )

    # 新しいパスワードのバリデーション（8文字以上）
    if len(data.newPassword) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="パスワードは8文字以上である必要があります",
        )

    # 新旧パスワードが同一の場合はエラー
    if data.oldPassword == data.newPassword:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="新しいパスワードは現在のパスワードと異なるものにしてください",
        )

    # パスワード更新
    current_user.hashed_password = get_password_hash(data.newPassword)
    db.commit()

    # セキュリティ強化: 全てのリフレッシュトークンを無効化（再ログイン必須）
    db.query(RefreshToken).filter(RefreshToken.user_id == current_user.id).update(
        {"is_revoked": True}
    )
    db.commit()

    return UpdateResponse(success=True, message="パスワードを変更しました")


@router.put("/settings", response_model=UpdateResponse)
async def update_settings(
    data: UserSettingsRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """
    ユーザー設定更新

    - 自動ログイン設定（rememberMe）
    - セッション期間設定（sessionDuration: 7d/30d/forever）

    Args:
        data: UserSettingsRequest（rememberMe, sessionDuration）
        credentials: Bearer Token
        db: データベースセッション

    Returns:
        UpdateResponse（success, message）

    Raises:
        HTTPException 400: 不正な設定値
        HTTPException 401: トークンが無効
    """
    # 現在のユーザー取得
    current_user = get_current_user(credentials, db)

    # sessionDurationのバリデーション
    if data.sessionDuration not in ["7d", "30d", "forever"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不正な設定値です",
        )

    # セッション期間を日数に変換
    duration_mapping = {
        "7d": 7,
        "30d": 30,
        "forever": 0,  # 0 = 無期限（実際は365日）
    }

    # ユーザー設定を更新
    current_user.auto_login_enabled = data.rememberMe
    current_user.auto_login_duration = duration_mapping[data.sessionDuration]

    db.commit()

    return UpdateResponse(success=True, message="設定を更新しました")
