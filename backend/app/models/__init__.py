"""
SQLAlchemy 2.0 モデル定義
すべてのモデルをこのファイルに集約（単一真実源の原則）
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class User(Base):
    """ユーザーモデル（FastAPI-Users互換）"""

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # プロフィール情報
    profile_name: Mapped[str] = mapped_column(String, nullable=False)
    profile_avatar: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # ロール（'guest', 'user', 'admin'）
    role: Mapped[str] = mapped_column(String, default="user", nullable=False)

    # 自動ログイン設定
    auto_login_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    auto_login_duration: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True
    )  # 7, 30, or 0 (無期限)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # リレーション
    sajus: Mapped[list["Saju"]] = relationship("Saju", back_populates="user")
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship("RefreshToken", back_populates="user")


class Saju(Base):
    """命式モデル"""

    __tablename__ = "saju"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[Optional[str]] = mapped_column(
        String, ForeignKey("users.id"), nullable=True
    )  # ゲストの場合null

    # 基本情報
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    birth_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    gender: Mapped[str] = mapped_column(String, nullable=False)  # 'male' or 'female'

    # 四柱（天干・地支）
    year_stem: Mapped[str] = mapped_column(String, nullable=False)
    year_branch: Mapped[str] = mapped_column(String, nullable=False)
    month_stem: Mapped[str] = mapped_column(String, nullable=False)
    month_branch: Mapped[str] = mapped_column(String, nullable=False)
    day_stem: Mapped[str] = mapped_column(String, nullable=False)
    day_branch: Mapped[str] = mapped_column(String, nullable=False)
    hour_stem: Mapped[str] = mapped_column(String, nullable=False)
    hour_branch: Mapped[str] = mapped_column(String, nullable=False)

    # 大運データ（JSON形式で保存）
    daeun_list: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # 吉凶レベル（1-5: 大凶, 凶, 平, 吉, 大吉）
    fortune_level: Mapped[int] = mapped_column(Integer, nullable=False)

    # メタデータ
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # リレーション
    user: Mapped[Optional["User"]] = relationship("User", back_populates="sajus")


class RefreshToken(Base):
    """リフレッシュトークンモデル"""

    __tablename__ = "refresh_tokens"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    token: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # リレーション
    user: Mapped["User"] = relationship("User", back_populates="refresh_tokens")
