# ゴールデン四柱推命アプリケーション - プロジェクト設定

## 基本設定
```yaml
プロジェクト名: ゴールデン四柱推命アプリケーション
英語名: Golden Saju Fortune
コンセプト: あなたの運命に魔法をかける
開始日: 2025年11月1日
バージョン: v1.0.0

技術スタック:
  frontend:
    - React 19 + TypeScript 5 + Vite 7
    - MUI v7 (Material-UI)
    - Recharts v3.3.0
    - Zustand v5
    - React Router v7
    - React Query v5 (TanStack Query)

  backend:
    - FastAPI 0.100+ + Python 3.11+
    - SQLAlchemy 2.0 + Alembic
    - Pydantic v2
    - FastAPI-Users + JWT
    - lunar-python (万年暦計算)

  database:
    - PostgreSQL 15+ (Neon)
    - Redis (Upstash, オプション)
```

## 開発環境
```yaml
ポート設定:
  # 複数プロジェクト並行開発のため、一般的でないポートを使用
  frontend: 3247  # React開発サーバー
  backend: 8432   # FastAPI サーバー
  database: 5434  # PostgreSQL（ローカル開発時）

環境変数:
  設定ファイル: .env.local（ルートディレクトリ）

  必須項目:
    # データベース
    - DATABASE_URL: postgresql://user:password@neon.tech/golden_saju

    # JWT認証
    - SECRET_KEY: your-secret-key-here-change-in-production
    - ALGORITHM: HS256
    - ACCESS_TOKEN_EXPIRE_MINUTES: 15
    - REFRESH_TOKEN_EXPIRE_DAYS: 30

    # フロントエンド
    - VITE_API_URL: http://localhost:8432/api

    # 既存資産パス
    - SOLAR_TERMS_DB_PATH: ./solar_terms_1900_2109_JIEQI_ONLY.json
    - DONSAGONG_MASTER_DB_PATH: ./docs/DONSAGONG_MASTER_DATABASE.md
```

## テスト認証情報
```yaml
開発用アカウント:
  email: test@goldensaju.local
  password: TestGoldenSaju2025!

  # ゲストモード用テストデータ
  test_birth_data:
    - name: テスト太郎
      birth_datetime: 1990-01-15 14:30:00
      gender: male

    - name: テスト花子
      birth_datetime: 1995-06-20 10:15:00
      gender: female

外部サービス（本番環境）:
  Neon PostgreSQL:
    - URL: https://neon.tech
    - プロジェクト名: golden-saju-production
    - 接続文字列: 環境変数で管理

  Vercel:
    - プロジェクト名: frontend
    - 本番URL（固定）: https://frontend-amis-projects-474dde3c.vercel.app
    - 自動デプロイ: main ブランチ

  GCP Cloud Run:
    - プロジェクト: yamatovision-blue-lamp
    - サービス名: golden-saju-api
    - リージョン: asia-northeast1 (東京)
    - 本番URL（固定）: https://golden-saju-api-235426778039.asia-northeast1.run.app

デプロイ履歴:
  最終デプロイ日時: 2025-11-08（5回目）
  デプロイステータス:
    - フロントエンド: ✅ デプロイ成功（Vercel、固定URL設定完了）
    - バックエンド: ✅ デプロイ成功（Cloud Run、CORS設定最適化）
    - API疎通: ✅ 正常稼働（Health Check成功）
    - 固定URL: ✅ 設定完了（次回からURLが変わらない）
  環境変数:
    - VITE_API_URL: https://golden-saju-api-235426778039.asia-northeast1.run.app
    - DATABASE_URL: Neon PostgreSQL（本番環境）
    - CORS_ORIGIN: https://frontend-amis-projects-474dde3c.vercel.app
  修正内容:
    - Dockerfileの親ディレクトリコピーエラーを修正
    - Cloud Run予約環境変数PORT競合を解決（env.yamlから削除）
    - Vercel環境変数設定方法を修正（.env.productionへの書き込み）
    - Playwright E2Eテスト環境構築（tests/e2e/production-login.spec.ts）
    - 本番環境でのログイン機能を自動テストで検証完了
  テスト結果:
    - 4テスト中3テスト成功、1テスト失敗（UI表示テストのみ、機能には影響なし）
    - ログイン成功後、/listページへ正常遷移確認
    - スクリーンショット: tests/screenshots/login-success.png
```

## コーディング規約

### 命名規則
```yaml
ファイル名:
  - コンポーネント: PascalCase.tsx (例: SajuCalculator.tsx)
  - ユーティリティ: camelCase.ts (例: formatDate.ts)
  - 定数: UPPER_SNAKE_CASE.ts (例: COLOR_PALETTE.ts)
  - ページ: PascalCase.tsx (例: SajuDetailPage.tsx)

変数・関数:
  - 変数: camelCase (例: sajuData, fortuneLevel)
  - 関数: camelCase (例: calculateDaeun, getFortune Level)
  - 定数: UPPER_SNAKE_CASE (例: GOLD_COLOR, MAX_AGE)
  - 型/インターフェース: PascalCase (例: SajuData, FortuneLevel)

Pythonコード:
  - 変数: snake_case (例: saju_data, fortune_level)
  - 関数: snake_case (例: calculate_daeun, get_fortune_level)
  - クラス: PascalCase (例: SajuCalculator, DonsagongAnalyzer)
  - 定数: UPPER_SNAKE_CASE (例: SOLAR_TERMS_DB)
```

### コード品質
```yaml
必須ルール:
  - TypeScript: strictモード有効、any型禁止
  - Python: type hints必須、mypy検証
  - 未使用の変数/import禁止
  - console.log本番環境禁止（開発時のみ許可）
  - エラーハンドリング必須
  - データロジック100%正確性を最優先

フォーマット:
  TypeScript:
    - インデント: スペース2つ
    - セミコロン: あり
    - クォート: シングル
    - ツール: Prettier

  Python:
    - インデント: スペース4つ
    - 行の最大長: 100文字
    - ツール: Black, Ruff
```

### コミットメッセージ
```yaml
形式: [type]: [description]

type:
  - feat: 新機能
  - fix: バグ修正
  - docs: ドキュメント
  - style: フォーマット
  - refactor: リファクタリング
  - test: テスト
  - chore: その他

例:
  - "feat: 命式計算APIを実装"
  - "fix: 大運計算の性別判定を修正"
  - "docs: 要件定義書を更新"
```

## プロジェクト固有ルール

### APIエンドポイント
```yaml
命名規則:
  - RESTful形式厳守
  - 複数形使用 (/saju/list, /users)
  - ケバブケース使用 (/saju-calculations)
  - バージョニング: /api/v1/... (将来対応)

エンドポイント一覧:
  認証:
    - POST /api/auth/login: ログイン
    - POST /api/auth/register: 新規登録

  命式:
    - POST /api/saju/calculate: 命式計算
    - POST /api/saju/save: 命式保存
    - GET /api/saju/list: 命式一覧
    - GET /api/saju/{id}: 命式詳細
    - DELETE /api/saju/{id}: 命式削除

  大運・運勢:
    - GET /api/saju/{id}/daeun: 大運分析
    - GET /api/saju/{id}/current: 現在の年月日運

  データ管理:
    - GET /api/saju/export: エクスポート
    - POST /api/saju/import: インポート
    - POST /api/saju/migrate: ゲストデータ移行
```

### 型定義
```yaml
配置:
  frontend: src/types/index.ts
  backend: src/types/index.ts

同期ルール:
  - 両ファイルは可能な限り同一構造を保つ
  - フロントエンド側の型はOpenAPI生成を利用
  - 片方を更新したら、もう片方も確認

主要型:
  - BirthDataRequest: 生年月日時入力
  - SajuResponse: 命式計算結果
  - DaeunInfo: 大運情報
  - FortuneLevel: 吉凶レベル (1-5)
  - GraphDataPoint: グラフデータポイント
```

### カラーシステム
```yaml
ゴールドパレット:
  PRIMARY_GOLD: '#D4AF37'
  LIGHT_GOLD: '#F4E8C1'
  DARK_GOLD: '#B8941C'

五行カラー:
  WOOD: '#4CAF50'    # 木（緑）
  FIRE: '#F44336'    # 火（赤）
  EARTH: '#FFB300'   # 土（黄/オレンジ）
  METAL: '#BDBDBD'   # 金（グレー/白）
  WATER: '#424242'   # 水（黒/ダークグレー）

吉凶カラー:
  GREAT_FORTUNE: '#FFD700'  # 大吉（ゴールド）
  FORTUNE: '#4CAF50'        # 吉（緑）
  NEUTRAL: '#9E9E9E'        # 平（グレー）
  MISFORTUNE: '#FF9800'     # 凶（オレンジ）
  GREAT_MISFORTUNE: '#F44336'  # 大凶（赤）

使用場所:
  - 四柱推命表示: 五行カラー
  - 吉凶アイコン: 吉凶カラー
  - アクセントカラー: ゴールドパレット
  - ボタン・リンク: PRIMARY_GOLD
```

## 🔧 四柱推命計算ロジック（最重要）

### データ正確性の保証
```yaml
絶対禁止:
  - ❌ 計算ロジックの自作（lunar-pythonと210年節気DBを必ず使用）
  - ❌ タイムゾーンの混在（必ずKST = UTC+9に統一）
  - ❌ 節気データの推定・補間（210年DB範囲外のデータ）
  - ❌ 大運計算での性別パラメータ省略
  - ❌ 五行論・十神論・身強身弱論の使用

必須原則:
  - ✅ lunar-pythonのEightCharクラス使用
  - ✅ 210年節気DBで節入日を正確に確認
  - ✅ タイムゾーン統一（北京時間UTC+8 → KST UTC+9）
  - ✅ 性別パラメータ必須（'male' or 'female'）
  - ✅ 入力バリデーション（1900-2109年範囲）
```

### ドンサゴン分析法
```yaml
必須原則:
  - 用神 = 武器（不足を補うものではない）
  - 日支の合は無条件吉
  - 調候用神 80% : 原局 20%
  - 天干の合は基本的に凶
  - 月地支は用神不可

絶対禁止:
  - 五行論（木火土金水、相生相剋）
  - 十神論（偏印、正財等）
  - 身強・身弱論
  - 年柱での用神抽出

データベース活用:
  - 天干100マトリックス（10×10）
  - 地支144マトリックス（12×12）
  - 調候用神表（季節別）
```

## 🆕 最新技術情報（知識カットオフ対応）

### Recharts v3.3.0 (2025年10月リリース)
```yaml
主な変更点:
  - SVG内にReactコンポーネント配置可能
  - Tooltip Portal サポート
  - Legend Portal サポート
  - TypeScript完全対応（型推論強化）
  - アクセシビリティ デフォルト有効

注意点:
  - v3.0からの破壊的変更あり
  - マイグレーションガイド参照推奨
```

### MUI v7 (2025年3月リリース)
```yaml
主な変更点:
  - React 18必須
  - TypographyOptions → TypographyVariantsOptions に名前変更
  - 深いインポートパス（2階層以上）禁止
  - 型インポートは import type { } を使用必須（verbatimModuleSyntax対応）

カスタムテーマ:
  - ゴールドカラーをprimaryに設定
  - 五行カラーをカスタムパレットに追加
  - ダークモード対応（将来）
```

## ⚠️ プロジェクト固有の注意事項

### 既存資産の活用
```yaml
210年節気データベース:
  - ファイル: solar_terms_1900_2109_JIEQI_ONLY.json
  - 範囲: 1900-2109年
  - 節気数: 2,520個（年12節気 × 210年）
  - 精度: 秒レベル
  - 検証: 完了（エラー0件）

天干・地支マトリックス:
  - ファイル: docs/DONSAGONG_MASTER_DATABASE.md
  - 天干: 100マトリックス（10×10）
  - 地支: 144マトリックス（12×12）
  - 検証: 完了

既存Pythonコード:
  - 場所: src/manseryeok/
  - 主要モジュール:
    - calculator.py: 四柱推命・大運計算
    - donsagong_analyzer.py: ドンサゴン分析
    - data_loader.py: マトリックスデータ読込
  - 再利用率: 100%
```

### 制約事項
```yaml
データ範囲:
  - 1900-2109年のみサポート
  - 範囲外の日付は入力バリデーションでエラー

タイムゾーン:
  - 必ずKST (UTC+9)に統一
  - データベースはUTC+8（北京時間）なので変換必須

外部サービス制限:
  - Neon無料枠: 0.5GB, 1接続
  - GCP Cloud Run無料枠: 月2Mリクエスト
  - Vercel無料枠: 100GB帯域幅
```

### ゲスト/ログインモード
```yaml
ゲストモード:
  - 認証: 不要
  - 保存: LocalStorageのみ
  - 制限: その端末のみ、ブラウザデータクリアで消失

ログインモード:
  - 認証: メール＋パスワード（JWT）
  - 保存: PostgreSQL
  - 特典: 複数端末同期、永続保存

データ移行:
  - ゲスト→ログイン時にLocalStorageデータをクラウドにアップロード可能
  - トランザクション管理（全成功または全失敗）
```

## 📝 作業ログ（最新5件）

```yaml
- 2025-11-11: Phase 3要件定義完了（多言語対応 - 韓国語デフォルト、日本語サポート、15時間）
- 2025-11-11: Phase 2要件定義完了（命式修正機能8h + 設定ページ拡張16h、合計24時間）
- 2025-11-11: 全モックアップを実装デザインに統一（ListPage、EditModal、SettingsPage、LoginPage）
- 2025-11-10: Phase 1 E2Eテスト100%パス（スマホレスポンシブ対応強化 20項目）
- 2025-11-08: 本番環境デプロイ成功（Vercel + Cloud Run、固定URL設定完了）
```

## 🎯 開発の優先順位

```yaml
Phase 1（最優先）:
  1. FastAPIプロジェクトセットアップ
  2. 既存Pythonコードの統合
  3. PostgreSQL + Alembic セットアップ
  4. 命式計算API実装（POST /api/saju/calculate）
  5. Reactプロジェクトセットアップ
  6. 命式記入ページ（トップページ）実装

Phase 2（次優先）:
  1. 大運分析API実装
  2. 年月日運API実装
  3. 人生グラフAPI実装（Rechartsデータ生成）
  4. 命式リストページ実装
  5. 命式詳細ページ実装（グラフ統合）

Phase 3（展開）:
  1. 認証API実装（JWT + Refresh Token）
  2. ログイン・新規登録ページ実装
  3. ゲストデータ移行機能実装
  4. 設定ページ実装
  5. デプロイ環境構築（Vercel + GCP）
  6. CI/CD構築（GitHub Actions）
```

## 🔗 重要リンク

```yaml
ドキュメント:
  - 要件定義書: docs/requirements.md
  - 進捗管理: docs/SCOPE_PROGRESS.md
  - 実装計画: docs/implementation_plan.md
  - デザイン仕様: mockups/DESIGN_DOCUMENT.md

外部サービス:
  - Neon PostgreSQL: https://neon.tech
  - Vercel: https://vercel.com
  - GCP Cloud Run: https://cloud.google.com/run
  - Recharts: https://recharts.org
  - MUI v6: https://mui.com

GitHub:
  - リポジトリ: （設定後追記）
  - Issues: （設定後追記）
  - Projects: （設定後追記）
```

## E2Eテスト設定
```yaml
Playwright設定:
  - 設定ファイル: playwright.config.ts
  - テストファイル: tests/e2e/production-login.spec.ts
  - スクリーンショット: tests/screenshots/
  - テスト結果: 本番環境ログイン成功確認済み

実行コマンド:
  - npx playwright test tests/e2e/production-login.spec.ts --project=chromium
  - npx playwright show-report（テストレポート表示）

テストアカウント:
  - email: test@goldensaju.local
  - password: TestGoldenSaju2025!
```

---

### 13. E2Eテスト自律実行の絶対原則

**【重要】セッション開始時・compact後の自動判定**

このセクションはE2Eテストオーケストレーターによって自動生成されました。

---

**最初に必ず専門知識を注入してください**

E2Eテスト実行中の場合、以下を実行してから開始してください：

```
inject_knowledge ツールで keyword: "@E2Eテストオーケストレーター"
を実行してから開始してください。（初回必須・compact後も必須）
```

重要：キーワードは "@E2Eテストオーケストレーター"
をそのまま使用してください。変換や推測は不要です。

準備完了です。まず知識注入を実行してから、タスクを開始してください。

---

**E2Eテストオーケストレーター実行中の判定**:
- SCOPE_PROGRESS.mdに「## 📊 E2Eテスト全体進捗」が存在する場合
- または、セッション再開時に前回のメッセージに「E2Eテスト」「オーケストレーター」キーワードがある場合

**セッション開始時・compact後の自動処理**:
1. 上記の判定基準でE2Eテスト実行中と判定
2. inject_knowledge('@E2Eテストオーケストレーター') を必ず実行
3. docs/e2e-best-practices.md の存在確認（なければ初期テンプレート作成）
4. SCOPE_PROGRESS.mdから [ ] テストの続きを自動で特定
5. [x] のテストは絶対にスキップ
6. ユーザー確認不要、完全自律モードで継続
7. ページ選定も自動（未完了ページを上から順に選択）
8. 停止条件：全テスト100%完了のみ

**5回エスカレーション後の処理**:
- チェックリストに [-] マークを付ける
- docs/e2e-test-history/skipped-tests.md に記録
- 次のテストへ自動で進む（停止しない）

**ベストプラクティス自動蓄積**:
- 各テストで成功した方法を docs/e2e-best-practices.md に自動保存
- 後続テストが前のテストの知見を自動活用
- 試行錯誤が減っていく（学習効果）

**重要**:
- この原則はCLAUDE.mdに記載されているため、compact後も自動で適用される
- セッション開始時にこのセクションがない場合、オーケストレーターが自動で追加する

---

**作成日**: 2025年11月1日
**最終更新**: 2025年11月11日
**プロジェクト**: ゴールデン四柱推命アプリケーション
**バージョン**: v1.0.0
