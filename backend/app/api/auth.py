"""
認証APIルーター
POST /api/auth/register - 新規登録
POST /api/auth/login - ログイン
POST /api/auth/logout - ログアウト
GET /api/auth/me - 現在のユーザー情報取得
"""
import uuid
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.auth import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    get_password_hash,
    get_permissions_for_role,
    verify_password,
)
from app.core.config import settings
from app.db.session import get_db
from app.models import RefreshToken, User
from app.schemas.auth import (
    AuthResponse,
    LoginRequest,
    LogoutResponse,
    RegisterRequest,
    UserProfile,
    UserResponse,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])

# Bearer Token認証
security = HTTPBearer()


# ==================== ヘルパー関数 ====================


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """
    アクセストークンから現在のユーザーを取得

    Args:
        credentials: Bearer Token
        db: データベースセッション

    Returns:
        Userモデル

    Raises:
        HTTPException: トークンが無効、またはユーザーが見つからない場合
    """
    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="認証が必要です",
        )

    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ユーザーが見つかりません",
        )

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ユーザーが見つかりません",
        )

    return user


def create_user_response(user: User, access_token: str, refresh_token: str) -> AuthResponse:
    """
    ユーザー情報からAuthResponseを生成

    Args:
        user: Userモデル
        access_token: アクセストークン
        refresh_token: リフレッシュトークン

    Returns:
        AuthResponse
    """
    permissions = get_permissions_for_role(user.role)

    user_response = UserResponse(
        id=user.id,
        email=user.email,
        role=user.role,
        permissions=permissions,
        profile=UserProfile(
            name=user.profile_name,
            avatar=user.profile_avatar,
        ),
        createdAt=user.created_at.isoformat(),
    )

    return AuthResponse(
        accessToken=access_token,
        refreshToken=refresh_token,
        user=user_response,
    )


# ==================== エンドポイント ====================


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest, db: Session = Depends(get_db)):
    """
    新規登録

    - メールアドレスとパスワードでユーザー登録
    - 自動的にログイン状態にする
    - プロフィール名はメールアドレスのローカル部分（@の前）

    Args:
        data: RegisterRequest（email, password, migrateGuestData）
        db: データベースセッション

    Returns:
        AuthResponse（accessToken, refreshToken, user）

    Raises:
        HTTPException 409: メールアドレスが既に登録されている
        HTTPException 400: パスワードが8文字未満
    """
    # パスワードバリデーション
    if len(data.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="パスワードは8文字以上である必要があります",
        )

    # メールアドレス重複チェック
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="このメールアドレスは既に登録されています",
        )

    # プロフィール名生成（nameが指定されていればそれを使用、なければメールアドレスのローカル部分）
    profile_name = data.name if data.name else data.email.split("@")[0]

    # ユーザー作成
    user_id = str(uuid.uuid4())
    hashed_password = get_password_hash(data.password)

    new_user = User(
        id=user_id,
        email=data.email,
        hashed_password=hashed_password,
        profile_name=profile_name,
        role="user",
        is_active=True,
        is_verified=False,
        is_superuser=False,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # トークン生成
    access_token = create_access_token(data={"sub": user_id, "email": data.email, "role": "user"})
    refresh_token_str = create_refresh_token()

    # リフレッシュトークンをDBに保存
    refresh_token_expires = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token_model = RefreshToken(
        id=str(uuid.uuid4()),
        user_id=user_id,
        token=refresh_token_str,
        expires_at=refresh_token_expires,
        is_revoked=False,
    )

    db.add(refresh_token_model)
    db.commit()

    return create_user_response(new_user, access_token, refresh_token_str)


@router.post("/login", response_model=AuthResponse)
async def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    ログイン

    - メールアドレスとパスワードで認証
    - アクセストークンとリフレッシュトークンを発行

    Args:
        data: LoginRequest（email, password, rememberMe）
        db: データベースセッション

    Returns:
        AuthResponse（accessToken, refreshToken, user）

    Raises:
        HTTPException 401: メールアドレスまたはパスワードが正しくない
    """
    # ユーザー検索
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="メールアドレスまたはパスワードが正しくありません",
        )

    # パスワード検証
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="メールアドレスまたはパスワードが正しくありません",
        )

    # アクティブチェック
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="このアカウントは無効化されています",
        )

    # トークン生成
    access_token = create_access_token(data={"sub": user.id, "email": user.email, "role": user.role})
    refresh_token_str = create_refresh_token()

    # リフレッシュトークンをDBに保存
    refresh_token_expires = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token_model = RefreshToken(
        id=str(uuid.uuid4()),
        user_id=user.id,
        token=refresh_token_str,
        expires_at=refresh_token_expires,
        is_revoked=False,
    )

    db.add(refresh_token_model)
    db.commit()

    return create_user_response(user, access_token, refresh_token_str)


@router.post("/logout", response_model=LogoutResponse)
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """
    ログアウト

    - リフレッシュトークンを無効化
    - クライアント側でトークンを削除する必要がある

    Args:
        credentials: Bearer Token
        db: データベースセッション

    Returns:
        LogoutResponse（success, message）

    Raises:
        HTTPException 401: トークンが無効
    """
    # ユーザー取得
    user = get_current_user(credentials, db)

    # 全てのリフレッシュトークンを無効化
    db.query(RefreshToken).filter(RefreshToken.user_id == user.id).update(
        {"is_revoked": True}
    )
    db.commit()

    return LogoutResponse(success=True, message="ログアウトしました")


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    現在のユーザー情報取得

    - アクセストークンから現在のユーザー情報を取得

    Args:
        current_user: 現在のユーザー（Depends経由）

    Returns:
        UserResponse

    Raises:
        HTTPException 401: トークンが無効
    """
    permissions = get_permissions_for_role(current_user.role)

    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        role=current_user.role,
        permissions=permissions,
        profile=UserProfile(
            name=current_user.profile_name,
            avatar=current_user.profile_avatar,
        ),
        createdAt=current_user.created_at.isoformat(),
    )
