"""
FastAPI メインアプリケーション
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, saju, user
from app.core.config import settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """アプリケーションライフサイクル管理"""
    # スタートアップ: 重い初期化処理を事前に実行
    print("🚀 アプリケーション起動中...")

    try:
        # 命式計算エンジンの事前初期化（210年節気DB読み込み）
        print("📚 命式計算エンジンを初期化中...")
        from app.api.saju import get_calculator, get_fortune_calculator

        calculator = get_calculator()
        print("✅ 命式計算エンジンの初期化完了")

        fortune_calculator = get_fortune_calculator()
        print("✅ 年月日運計算エンジンの初期化完了")

        print("🎉 アプリケーション起動完了！")
    except Exception as e:
        print(f"❌ 初期化エラー: {e}")
        raise

    yield  # アプリケーション実行中

    # シャットダウン
    print("👋 アプリケーションをシャットダウン中...")


# FastAPIアプリケーション作成
app = FastAPI(
    title="Golden Saju Fortune API",
    description="ゴールデン四柱推命アプリケーション バックエンドAPI",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS設定（環境変数から読み込み）
# 開発環境では複数ポート対応（3247, 3248, 3249）
allowed_origins = [
    "http://localhost:3247",
    "http://localhost:3248",
    "http://localhost:3249",
    settings.CORS_ORIGIN,  # .env.localから読み込み（本番環境用）
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,  # 認証情報を含むリクエストを許可
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# ルーター登録
app.include_router(auth.router)
app.include_router(saju.router)
app.include_router(user.router)


@app.get("/")
async def root():
    """ルートエンドポイント（ヘルスチェック）"""
    return {
        "message": "Golden Saju Fortune API",
        "version": "1.0.0",
        "status": "healthy",
    }


@app.get("/health")
async def health_check():
    """ヘルスチェックエンドポイント"""
    return {"status": "ok"}
