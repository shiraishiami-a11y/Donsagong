"""
SQLAlchemy 2.0 データベースセッション設定
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

# SQLAlchemy 2.0エンジン作成
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # 開発時はSQLログ出力
    pool_pre_ping=True,  # 接続確認
    pool_size=5,
    max_overflow=10,
)

# セッションファクトリ
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# SQLAlchemy 2.0 DeclarativeBase
class Base(DeclarativeBase):
    """すべてのモデルの基底クラス"""

    pass


# 依存性注入用のセッション取得関数
def get_db():
    """FastAPI依存性注入用のDB取得"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
