"""
データベース接続のテスト
"""
import pytest
from sqlalchemy import text

from app.db.session import SessionLocal


def test_database_connection():
    """PostgreSQL接続テスト"""
    db = SessionLocal()
    try:
        # 簡単なクエリを実行
        result = db.execute(text("SELECT 1"))
        assert result.scalar() == 1
    finally:
        db.close()


def test_users_table_exists():
    """usersテーブルの存在確認"""
    db = SessionLocal()
    try:
        result = db.execute(
            text(
                "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users')"
            )
        )
        assert result.scalar() is True
    finally:
        db.close()


def test_saju_table_exists():
    """sajuテーブルの存在確認"""
    db = SessionLocal()
    try:
        result = db.execute(
            text(
                "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'saju')"
            )
        )
        assert result.scalar() is True
    finally:
        db.close()
