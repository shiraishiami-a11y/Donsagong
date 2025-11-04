# バックエンド実装計画書

**策定日**: 2025年11月2日
**プロジェクト**: ゴールデン四柱推命アプリケーション
**オーケストレーター**: BlueLamp バックエンド計画オーケストレーター v1.0

---

## 📊 エンドポイント依存関係分析結果

全19エンドポイントを依存関係で分類しました。

### 基盤エンドポイント（他の前提となる）
- POST /api/auth/login
- POST /api/auth/register
- GET /api/auth/me

### 独立エンドポイント（並列実装可能）
- POST /api/saju/calculate
- POST /api/saju/save

### 連鎖エンドポイント（順序依存）
- GET /api/saju/list（依存: save完了）
- GET /api/saju/{id}（依存: save完了）
- DELETE /api/saju/{id}（依存: save完了）
- GET /api/saju/{id}/daeun（依存: 命式計算）
- GET /api/saju/{id}/current（依存: 命式計算）
- GET /api/saju/{id}/year/{daeun_start_age}（依存: 大運計算）
- GET /api/saju/{id}/month/{year}（依存: 年運計算）
- GET /api/saju/{id}/day/{year}/{month}（依存: 月運計算）

### 集約エンドポイント（複数機能依存）
- PUT /api/user/password（依存: 認証）
- PUT /api/user/settings（依存: 認証）
- GET /api/saju/export（依存: list）
- POST /api/saju/import（依存: save）
- POST /api/auth/logout（依存: 認証）
- POST /api/saju/migrate（依存: 認証 + save）

---

## 🎯 垂直スライス実装順序

垂直スライス方式で機能単位の実装順序を決定しました。番号-アルファベット表記（2-A, 2-Bなど）は並列実装可能を示します。

| 順序 | スライス名 | 主要機能 | 依存スライス | エンドポイント数 | 実装優先度 | 完了 |
|------|-----------|---------|-------------|--------------|----------|------|
| 1 | 環境構築 | FastAPI + PostgreSQL + Alembic セットアップ | なし | 0 | 🔴 最高 | [x] ✅ |
| 2 | 命式計算基盤 | lunar-python + 210年節気DB統合 | 環境構築 | 2 | 🔴 最高 | [x] ✅ |
| 3-A | 認証基盤 | ログイン/ログアウト/JWT管理 | 環境構築 | 4 | 🔴 最高 | [x] ✅ |
| 3-B | 命式管理 | リスト取得・削除 | 命式計算基盤 | 3 | 🔴 最高 | [x] ✅ |
| 4 | 大運分析 | 大運計算・年月日運 | 命式計算基盤 | 5 | 🟡 高 | [ ] |
| 5-A | ユーザー設定 | パスワード・設定変更 | 認証基盤 | 2 | 🟡 高 | [x] ✅ |
| 5-B | データ管理 | エクスポート・インポート | 命式管理 | 2 | 🟡 高 | [x] ✅ |
| 6 | データ移行 | ゲストデータ移行 | 認証基盤 + 命式管理 | 1 | 🟢 中 | [ ] |

**合計**: 6スライス、19エンドポイント

---

## 📋 エンドポイント実装タスクリスト

### スライス1: 環境構築 ✅ 完了

| タスク | 内容 | 完了 |
|--------|------|------|
| 1.1 | FastAPI プロジェクトセットアップ | [x] |
| 1.2 | PostgreSQL接続設定（Neon） | [x] |
| 1.3 | SQLAlchemy 2.0 モデル作成 | [x] |
| 1.4 | Alembic マイグレーション設定 | [x] |
| 1.5 | pytest テスト環境セットアップ | [x] |

**成功基準**: FastAPIサーバーが起動し、PostgreSQLに接続できる ✅ 達成

**実装完了日**: 2025年11月2日
**テスト結果**: 5/5 passed
**サーバー起動確認**: http://localhost:8432/ 正常動作

---

### スライス2: 命式計算基盤 ✅ 完了

| タスク | エンドポイント | メソッド | 依存ライブラリ | 完了 |
|--------|--------------|---------|---------------|------|
| 2.1 | POST /api/saju/calculate | POST | lunar-python, 210年節気DB | [x] ✅ |
| 2.2 | POST /api/saju/save | POST | SQLAlchemy | [x] ✅ |

**成功基準**: 全て達成 ✅
- ✅ lunar-python で正確な四柱計算ができる
- ✅ 210年節気DBで節入日を参照できる
- ✅ 大運リスト（10個）が性別に応じて順行/逆行で生成される
- ✅ PostgreSQLに命式データを保存できる

**実装完了日**: 2025年11月2日
**テスト結果**: 20/20 passed（精度テスト含む）
**実装ファイル**:
- `backend/app/services/saju_calculator.py` - 命式計算エンジン
- `backend/app/schemas/saju.py` - Pydanticスキーマ定義
- `backend/app/api/saju.py` - APIルーター
- `backend/tests/test_saju_calculate.py` - 計算テスト
- `backend/tests/test_saju_save.py` - 保存テスト
- `backend/tests/test_saju_accuracy.py` - 精度テスト

**実装詳細**:

#### 2.1: POST /api/saju/calculate
```python
# 1. Pydanticスキーマ定義
class BirthDataRequest(BaseModel):
    birthDatetime: str  # ISO 8601
    gender: Literal['male', 'female']
    name: Optional[str] = None
    timezoneOffset: Optional[int] = 9  # KST

class SajuResponse(BaseModel):
    id: str  # UUID
    name: Optional[str]
    birthDatetime: str
    gender: str
    yearStem: str
    yearBranch: str
    monthStem: str
    monthBranch: str
    dayStem: str
    dayBranch: str
    hourStem: str
    hourBranch: str
    daeunList: List[DaeunInfo]
    fortuneLevel: FortuneLevelEnum
    createdAt: str
    # ... その他のフィールド

# 2. エンドポイント実装
@router.post("/api/saju/calculate", response_model=SajuResponse)
async def calculate_saju(data: BirthDataRequest):
    # lunar-python統合
    from lunar_python import Solar, EightChar

    # 210年節気DB読み込み
    jieqi_data = load_solar_terms_db()

    # 命式計算（既存コード src/manseryeok/calculator.py を使用）
    saju = calculate_saju_with_jieqi(data, jieqi_data)

    # 大運計算（性別に基づく順行/逆行）
    daeun_list = calculate_daeun(saju, data.gender)

    # 吉凶レベル判定（ドンサゴンマトリックス使用）
    fortune_level = analyze_fortune_level(saju, daeun_list)

    return SajuResponse(...)
```

#### 2.2: POST /api/saju/save
```python
# 1. SQLAlchemyモデル
class SajuModel(Base):
    __tablename__ = "saju"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)  # ゲストの場合null
    name = Column(String, nullable=True)
    birth_datetime = Column(DateTime)
    gender = Column(String)
    # ... 四柱データ
    created_at = Column(DateTime, default=datetime.utcnow)

# 2. エンドポイント実装
@router.post("/api/saju/save", response_model=SaveResponse)
async def save_saju(saju: SajuResponse, db: Session = Depends(get_db)):
    db_saju = SajuModel(**saju.dict())
    db.add(db_saju)
    db.commit()
    return SaveResponse(success=True, id=db_saju.id, message="保存しました")
```

**成功基準**:
- lunar-python で正確な四柱計算ができる
- 210年節気DBで節入日を参照できる
- 大運リスト（10個）が性別に応じて順行/逆行で生成される
- PostgreSQLに命式データを保存できる

---

### スライス3-A: 認証基盤 ✅ 完了

| タスク | エンドポイント | メソッド | 完了 |
|--------|--------------|---------|------|
| 3A.1 | POST /api/auth/register | POST | [x] ✅ |
| 3A.2 | POST /api/auth/login | POST | [x] ✅ |
| 3A.3 | POST /api/auth/logout | POST | [x] ✅ |
| 3A.4 | GET /api/auth/me | GET | [x] ✅ |

**成功基準**: 全て達成 ✅
- ✅ ユーザー登録ができる
- ✅ ログインでJWTトークンが発行される
- ✅ トークン検証が動作する
- ✅ リフレッシュトークンがDBで管理される

**実装完了日**: 2025年11月2日
**テスト結果**: 12/12 passed（100%成功）
**実装ファイル**:
- `backend/app/models/__init__.py` - User, RefreshTokenモデル
- `backend/app/schemas/auth.py` - 認証スキーマ定義
- `backend/app/core/auth.py` - JWT生成・検証ユーティリティ
- `backend/app/api/auth.py` - 認証APIルーター
- `backend/tests/test_auth.py` - 認証APIテスト（12テスト）

**実装詳細**:
- JWT（python-jose + HS256）でアクセストークン生成（15分有効）
- リフレッシュトークン（30日有効）をPostgreSQLで管理
- パスワードハッシュ化（bcrypt）
- ロールベースアクセス制御（guest, user, admin）
- HTTPBearer認証によるトークン検証

---

### スライス3-B: 命式管理 ✅ 完了

| タスク | エンドポイント | メソッド | 完了 |
|--------|--------------|---------|------|
| 3B.1 | GET /api/saju/list | GET | [x] ✅ |
| 3B.2 | GET /api/saju/{id} | GET | [x] ✅ |
| 3B.3 | DELETE /api/saju/{id} | DELETE | [x] ✅ |

**実装詳細**:

```python
@router.get("/api/saju/list", response_model=List[SajuSummary])
async def get_saju_list(
    current_user: User = Depends(current_active_user),
    db: Session = Depends(get_db)
):
    # ゲストモードの場合はuser_idがnullのデータを取得
    # ログインユーザーの場合は自分のデータのみ取得
    sajus = db.query(SajuModel).filter(
        or_(SajuModel.user_id == current_user.id, SajuModel.user_id == None)
    ).all()
    return [SajuSummary.from_orm(s) for s in sajus]
```

**成功基準**: 全て達成 ✅
- ✅ ユーザーごとの命式リストが取得できる
- ✅ ゲストモードのデータも扱える（user_id is null）
- ✅ 他人のデータにはアクセスできない
- ✅ ページネーション機能が動作する
- ✅ ソート機能が動作する（createdAt, birthDatetime, fortuneLevel）
- ✅ 命式詳細が正しく取得できる
- ✅ 削除が正しく動作する

**実装完了日**: 2025年11月2日
**テスト結果**: 9/9 passed
**実装ファイル**:
- `backend/app/api/saju.py` - 3つのエンドポイント追加
- `backend/app/schemas/saju.py` - SajuSummary, SajuListResponse, DeleteResponse追加
- `backend/tests/test_saju_list.py` - 9テストケース
- `backend/tests/conftest.py` - dbフィクスチャ追加

---

### スライス4: 大運分析

| タスク | エンドポイント | メソッド | 完了 |
|--------|--------------|---------|------|
| 4.1 | GET /api/saju/{id}/daeun | GET | [ ] |
| 4.2 | GET /api/saju/{id}/current | GET | [ ] |
| 4.3 | GET /api/saju/{id}/year/{daeun_start_age} | GET | [ ] |
| 4.4 | GET /api/saju/{id}/month/{year} | GET | [ ] |
| 4.5 | GET /api/saju/{id}/day/{year}/{month} | GET | [ ] |

**実装詳細**:

```python
# 大運分析エンジン統合（既存コード src/manseryeok/donsagong_analyzer.py）
from src.manseryeok.donsagong_analyzer import DonsagongAnalyzer

@router.get("/api/saju/{id}/daeun", response_model=DaeunAnalysisResponse)
async def get_daeun_analysis(id: str, db: Session = Depends(get_db)):
    saju = db.query(SajuModel).filter(SajuModel.id == id).first()
    if not saju:
        raise HTTPException(status_code=404, detail="命式が見つかりません")

    # ドンサゴン分析エンジン使用
    analyzer = DonsagongAnalyzer()
    daeun_analysis = analyzer.analyze_daeun(saju)

    return DaeunAnalysisResponse(**daeun_analysis)
```

**成功基準**:
- 大運リストが正しく取得できる
- 年運・月運・日運がlunar-pythonで正確に計算される
- ドンサゴンマトリックスで吉凶判定ができる

---

### スライス5-A: ユーザー設定 ✅ 完了

| タスク | エンドポイント | メソッド | 完了 |
|--------|--------------|---------|------|
| 5A.1 | PUT /api/user/password | PUT | [x] ✅ |
| 5A.2 | PUT /api/user/settings | PUT | [x] ✅ |

**成功基準**: 全て達成 ✅
- ✅ パスワード変更が動作する
- ✅ 現在のパスワードを検証
- ✅ 新しいパスワードのバリデーション（8文字以上）
- ✅ パスワード変更後、全トークンを無効化
- ✅ 自動ログイン設定が保存される（rememberMe, sessionDuration）
- ✅ 認証必須（JWT Bearer Token）

**実装完了日**: 2025年11月2日
**テスト結果**: 11/11 passed（100%成功）
**実装ファイル**:
- `backend/app/schemas/user.py` - ユーザー設定スキーマ定義
- `backend/app/api/user.py` - ユーザー設定APIルーター
- `backend/tests/test_user.py` - ユーザー設定APIテスト（11テスト）

**実装詳細**:
- パスワード変更時の現在のパスワード検証
- bcryptによる安全なパスワードハッシュ化
- セッション期間設定（7d/30d/forever → 7/30/0日）
- パスワード変更後の全リフレッシュトークン無効化（セキュリティ強化）

---

### スライス5-B: データ管理 ✅ 完了

| タスク | エンドポイント | メソッド | 完了 |
|--------|--------------|---------|------|
| 5B.1 | GET /api/saju/export | GET | [x] ✅ |
| 5B.2 | POST /api/saju/import | POST | [x] ✅ |

**成功基準**: 全て達成 ✅
- ✅ JSONエクスポート/インポートが動作する
- ✅ エクスポートデータにバージョン情報（v1.0.0）が含まれる
- ✅ インポート時のバリデーションが動作する
- ✅ 重複データのスキップ機能が動作する
- ✅ トランザクション管理（全成功または全失敗）が動作する

**実装完了日**: 2025年11月2日
**テスト結果**: 8/8 passed
**実装ファイル**:
- `backend/app/api/saju.py` - エクスポート/インポートエンドポイント追加
- `backend/app/schemas/saju.py` - ExportData, ImportResponseスキーマ追加
- `backend/tests/test_saju_export_import.py` - 8テストケース

**実装詳細**:

#### 5B.1: GET /api/saju/export
```python
@router.get("/export", response_model=ExportData)
async def export_saju_data(db: Session = Depends(get_db)):
    # ゲストモードの命式を全て取得（user_id is null）
    sajus_db = db.query(SajuModel).filter(SajuModel.user_id.is_(None)).all()

    # SajuResponseのリストを作成
    saju_list = [convert_to_response(saju) for saju in sajus_db]

    # エクスポートデータを構築
    export_data = ExportData(
        version="1.0.0",
        exportDate=datetime.now().isoformat(),
        data=saju_list,
    )
    return export_data
```

#### 5B.2: POST /api/saju/import
```python
@router.post("/import", response_model=ImportResponse)
async def import_saju_data(import_data: ExportData, db: Session = Depends(get_db)):
    # バージョンチェック
    if import_data.version != "1.0.0":
        return ImportResponse(success=False, importedCount=0, message="サポートされていないバージョン")

    # 重複チェック
    existing_ids = {row[0] for row in db.query(SajuModel.id).filter(SajuModel.user_id.is_(None)).all()}
    new_data = [item for item in import_data.data if item.id not in existing_ids]

    # トランザクション開始（全成功または全失敗）
    for saju in new_data:
        db_saju = create_saju_model(saju)
        db.add(db_saju)

    db.commit()
    return ImportResponse(success=True, importedCount=len(new_data), message=f"{len(new_data)}件のデータをインポートしました")
```

**テストケース**:
1. `test_export_empty_data`: データが0件の場合のエクスポート
2. `test_export_with_data`: データが存在する場合のエクスポート
3. `test_export_multiple_data`: 複数データのエクスポート
4. `test_import_valid_data`: 正しい形式のデータのインポート
5. `test_import_duplicate_data`: 重複データのスキップ
6. `test_import_multiple_data`: 複数データの一括インポート
7. `test_import_invalid_version`: 不正なバージョンのエラーハンドリング
8. `test_export_import_roundtrip`: エクスポート→インポートの往復テスト

---

### スライス6: データ移行

| タスク | エンドポイント | メソッド | 完了 |
|--------|--------------|---------|------|
| 6.1 | POST /api/saju/migrate | POST | [ ] |

**実装詳細**:

```python
@router.post("/api/saju/migrate", response_model=MigrateResponse)
async def migrate_guest_data(
    guest_data: List[SajuResponse],
    current_user: User = Depends(current_active_user),
    db: Session = Depends(get_db)
):
    # トランザクション管理（全成功または全失敗）
    try:
        migrated_count = 0
        for saju in guest_data:
            db_saju = SajuModel(**saju.dict())
            db_saju.user_id = current_user.id  # ユーザーIDを紐付け
            db.add(db_saju)
            migrated_count += 1

        db.commit()
        return MigrateResponse(
            success=True,
            migratedCount=migrated_count,
            message=f"{migrated_count}件のデータを移行しました"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="移行に失敗しました")
```

**成功基準**: ゲストデータが一括でユーザーに紐付けられる

---

## 📅 並列実装スケジュール（ガントチャート）

```
Week 1: |======環境構築======|
Week 2: |====命式計算基盤====|
Week 3: |===認証基盤===|
        |===命式管理===|     ← 並列実装可能
Week 4: |======大運分析======|
Week 5: |=ユーザー設定=|
        |=データ管理=|       ← 並列実装可能
Week 6: |==データ移行==|
Week 7: |====統合テスト====|
Week 8: |====E2Eテスト====|
```

**推定工数**:
- 1スライスあたり: 5-10日
- 並列実装による短縮: 約2週間
- 総期間: 約8週間（並列実装あり）

---

## 🔗 クリティカルパス

バックエンド実装の成功には、以下のクリティカルパスが重要です：

1. **環境構築** → すべての前提
2. **命式計算基盤** → コア機能、最重要
3. **大運分析** → CHAIN-002, CHAIN-003 に必須

このクリティカルパス上のスライスを最優先で実装してください。

---

## 🎯 次のアクション

### バックエンド実装エージェントへの引き継ぎ

1. **スライス1（環境構築）から順に実装開始**
2. **スライス3-A と 3-B は並列実装可能**
3. **各スライス完了時に統合テストを作成・実行**
4. **クリティカルパス上のスライスを優先**

### テスト品質検証エージェントへの引き継ぎ

1. **E2Eテスト仕様書（docs/e2e-specs/）を参照**
2. **連鎖テストを優先的に実装**
3. **各スライス完了時にテスト実行**

---

## 📚 参考資料

- **API仕様書**: `docs/api-specs/` - 19エンドポイント
- **E2Eテスト仕様書**: `docs/e2e-specs/` - 85+シナリオ
- **型定義**: `frontend/src/types/index.ts` - 単一真実源
- **既存コード**: `src/manseryeok/` - lunar-python統合済み
- **210年節気DB**: `solar_terms_1900_2109_JIEQI_ONLY.json`
- **ドンサゴンマトリックス**: `docs/DONSAGONG_MASTER_DATABASE.md`

---

**策定日**: 2025年11月2日
**バージョン**: 1.0
**オーケストレーター**: BlueLamp バックエンド計画オーケストレーター
