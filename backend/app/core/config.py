"""
アプリケーション設定
.env.localから環境変数を読み込む
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """環境変数設定"""

    # データベース
    DATABASE_URL: str

    # JWT認証
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # アプリケーション
    BACKEND_URL: str = "http://localhost:8432"
    FRONTEND_URL: str = "http://localhost:3247"
    CORS_ORIGIN: str = "http://localhost:3247"

    # 既存資産パス
    SOLAR_TERMS_DB_PATH: str = "/app/solar_terms_1900_2109_JIEQI_ONLY.json"
    DONSAGONG_MASTER_DB_PATH: str = "/app/docs/DONSAGONG_MASTER_DATABASE.md"

    model_config = SettingsConfigDict(
        env_file="../.env.local",  # backend/から見た相対パス
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # 余分なフィールドを無視
    )


settings = Settings()
