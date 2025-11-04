#!/usr/bin/env python3
"""
テストユーザー作成スクリプト
test@goldensaju.local / TestGoldenSaju2025!
"""
import asyncio
import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from app.core.auth import get_password_hash
from app.db.session import SessionLocal
from app.models import User


async def create_test_user():
    """テストユーザーを作成"""
    db: Session = SessionLocal()

    try:
        # 既存ユーザーチェック
        existing_user = db.query(User).filter(User.email == "test@goldensaju.local").first()

        if existing_user:
            print("ℹ️  テストユーザーは既に存在します")
            print(f"   Email: {existing_user.email}")
            print(f"   ID: {existing_user.id}")
            print(f"   作成日: {existing_user.created_at}")

            # パスワード再設定
            existing_user.hashed_password = get_password_hash("TestGoldenSaju2025!")
            db.commit()
            print("✅ パスワードを TestGoldenSaju2025! にリセットしました")
            return

        # 新規作成
        user_id = str(uuid.uuid4())
        hashed_password = get_password_hash("TestGoldenSaju2025!")

        new_user = User(
            id=user_id,
            email="test@goldensaju.local",
            hashed_password=hashed_password,
            profile_name="test",
            role="user",
            is_active=True,
            is_verified=False,
            is_superuser=False,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        print("✅ テストユーザーを作成しました")
        print(f"   Email: {new_user.email}")
        print(f"   Password: TestGoldenSaju2025!")
        print(f"   ID: {new_user.id}")

    except Exception as e:
        print(f"❌ エラー: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(create_test_user())
