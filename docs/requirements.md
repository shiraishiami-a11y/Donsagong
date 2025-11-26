# ゴールデン四柱推命アプリケーション - 要件定義書

## 要件定義の作成原則
- **「あったらいいな」は絶対に作らない**
- **拡張可能性のための余分な要素は一切追加しない**
- **将来の「もしかして」のための準備は禁止**
- **今、ここで必要な最小限の要素のみ**

---

## 1. プロジェクト概要

### 1.1 成果目標
既存の210年節気データベース（1900-2109年）と検証済み万年暦計算システムを統合し、ゴールドテーマの美しいUIで四柱推命・大運・年月日運を網羅的に分析し、5段階吉凶判定と折れ線グラフで視覚化する個人利用型四柱推命Webアプリケーション。

**ブランド名**: Golden Peppa（ゴールデンペッパー）
**コンセプト**: 「あなたの運命に魔法をかける」
**シンボル**: ゴールデンペッパーミル + キラキラエフェクト
**デザインテーマ**: 伝統的な四柱推命に「魔法のような」親しみやすさとワクワク感を加えた、ゴールド×手書き風の現代的デザイン

### 1.2 成功指標

#### 定量的指標
- 命式計算の正確性：100%（210年データベース検証済み）
- 複数の命式を保存・管理できる（最低20件以上）
- 大運・年運・月運・日運すべてを1画面で確認可能
- 人生グラフ（大運ベース折れ線）の生成時間5秒以内
- 吉凶判定7段階（大吉・小吉・吉・吉凶・平・凶・大凶）で明確に表示
- ユーザーの日干を基準にした正確な吉凶判定
- ローディングアニメーションの完全統合
- API応答時間：2秒以内
- ページ総数：6ページ（シンプル設計）
- モバイルレスポンシブ対応完了（xs/sm/md各ブレークポイント最適化）

#### 定性的指標
- 誰でも簡単に命式を記入・保存できる
- ゴールドテーマで高級感とエレガンスを感じられる
- キラキラエフェクトで魔法をかけるような体験
- 複雑な運勢情報が視覚的にわかりやすい
- 五行カラーシステムで命式が一目瞭然
- 人生の波が美しいグラフで一目瞭然
- ログイン不要で即座に使える（ゲストモード）
- ログインすれば複数端末で同期可能
- ダウンロード後、個人環境で利用可能

---

## 2. システム全体像

### 2.1 主要機能一覧

#### カテゴリ1：命式管理
- 生年月日時入力と自動計算
- 複数命式の保存・編集・削除
- 命式一覧表示・検索・フィルタ

#### カテゴリ2：運勢分析
- 四柱推命表示（五行カラー統合、モバイル最適化済み）
- 大運分析（10年周期、開始年齢表記）
- 年運・月運・日運分析（水平スクロール対応）
- 7段階吉凶判定（大吉・小吉・吉・吉凶・平・凶・大凶）
- ユーザーの日干を基準にした正確な吉凶判定
- 人生グラフ（大運ベース折れ線、レスポンシブ対応）

#### カテゴリ3：ユーザー管理
- ゲストモード（ローカルストレージ）
- ログインモード（クラウドDB同期）
- 自動ログイン機能（セッション保持）
- ゲスト→ログインユーザー移行

#### カテゴリ4：デザイン・UX
- ゴールドテーマ統合（Golden Peppa）
- golden-peppaアニメーション（ローディング）
- キラキラエフェクト
- レスポンシブ対応（完全実装済み）
- 統一デザインシステム（cardStyles.ts）
- 命式表示の視認性向上（1.5倍拡大）
- タップ領域最適化（Apple HIG準拠、最小48px）

### 2.2 ユーザーロールと権限

#### ゲストユーザー
- **認証**: 不要
- **データ保存**: ローカルストレージのみ
- **アクセス範囲**: その端末のみ
- **アクセス可能な機能**:
  - 命式記入・計算・保存（ローカル）
  - 命式リスト表示（ローカルデータのみ）
  - 命式詳細・グラフ表示
  - 設定（限定機能）
- **制限**: 複数端末での同期不可、データはその端末のみ

#### ログインユーザー
- **認証**: メールアドレス＋パスワード
- **データ保存**: PostgreSQL（クラウドDB）
- **アクセス範囲**: どの端末からでもOK（Web・アプリ両対応）
- **アクセス可能な機能**:
  - すべてのゲスト機能
  - クラウドDB同期
  - 複数端末でのデータ共有
  - 自動ログイン（セッション保持）
  - データエクスポート/インポート
- **特典**: データバックアップ、永続保存

#### 管理者
- **不要**（個人利用のため）

### 2.3 認証・認可要件

#### 認証方式
- **メールアドレス＋パスワード**（ログインモードのみ）
- **ゲストモードは認証スキップ**

#### セッション管理
- **方式**: JWT (Access Token) + Refresh Token
- **Access Token**: 有効期限15分、API呼び出し時の認証
- **Refresh Token**: 有効期限7日/30日/無期限（ユーザー選択）
- **自動ログイン**: Refresh Tokenが有効なら自動認証
- **セキュリティ**: Refresh Token rotation、デバイス制限

#### セキュリティレベル
- **ゲストモード**: なし（ローカルのみ）
- **ログインモード**: 中レベル
  - パスワードハッシュ化（bcrypt）
  - HTTPS通信必須
  - user_id によるデータ分離
  - CORS設定
  - Rate Limiting

#### 管理機能
- **必要性**: 不要
- **理由**: 個人利用、ユーザー自身が全権限、管理画面不要

---

## 3. ページ構成

**全6ページ実装完了**

1. TopPage（命式記入）
2. ListPage（命式一覧）
3. SajuDetailPage（命式詳細・大運グラフ）
4. SettingsPage（設定）
5. LoginPage（ログイン）
6. RegisterPage（新規登録）

---

## 4. データモデル

**実装完了**（`backend/app/models/__init__.py`）

- User（ユーザー）
- Saju（命式）
- RefreshToken（リフレッシュトークン）

---

## 5. 制約事項

### 外部ライブラリ制限
- **lunar-python**: 1900-2100年範囲サポート（210年データベースは2109年まで対応）
- **PostgreSQL**: 同時接続制限あり（Neon無料枠: 1接続）

### 技術的制約
- **データ正確性**: 210年節気データベース範囲内（1900-2109年）でのみ100%正確
- **計算複雑度**: 大運・年月日運・グラフ計算で応答時間が増加する可能性
- **ローカルストレージ**: ブラウザデータクリアで消失
- **タイムゾーン統一**: 必ずKST（韓国標準時、UTC+9）で統一
  - 入力：KST形式（例：`2025-01-01T12:00:00+09:00`）
  - 保存：KST形式でデータベース・LocalStorageに保存
  - 表示：KST形式のISO文字列から直接抽出（タイムゾーン変換を避ける）
  - 時間不明の場合：12:00または00:00をデフォルト値として使用

### ドンサゴン分析の絶対禁止事項
- ❌ 五行論（木火土金水、相生相剋）使用禁止
- ❌ 十神論（偏印、正財等）使用禁止
- ❌ 身強・身弱論使用禁止
- ❌ 年柱での用神抽出禁止
- ❌ 月地支は用神不可

### ドンサゴン分析の必須原則
- ✅ 用神 = 武器（不足を補うものではない）
- ✅ 日支の合は無条件吉
- ✅ 調候用神 80% : 原局 20%
- ✅ 天干の合は基本的に凶
- ✅ 月地支は用神不可

---

## 5. API実装状況

**コア機能実装完了**（`backend/app/api/`）

### 認証API（auth.py）
- POST /api/auth/register
- POST /api/auth/login
- POST /api/auth/logout
- GET /api/auth/me

### 命式API（saju.py）
- POST /api/saju/calculate
- POST /api/saju/save
- GET /api/saju/list
- GET /api/saju/{id}
- DELETE /api/saju/{id}
- GET /api/saju/export
- POST /api/saju/migrate

### 運勢API（saju.py）
- GET /api/saju/{id}/daeun
- GET /api/saju/{id}/current
- GET /api/saju/{id}/year/{daeun_start_age}
- GET /api/saju/{id}/month/{year}
- GET /api/saju/{id}/day/{year}/{month}

---

## 6. 技術スタック

**実装済み**

- フロントエンド: React 19 + TypeScript 5 + Vite 7 + MUI v7 + Recharts v3.3.0
- バックエンド: FastAPI 0.109 + Python 3.9 + SQLAlchemy 2.0
- データベース: PostgreSQL 15 (Neon)
- 万年暦計算: lunar-python
- 210年節気DB: 1900-2109年

---

## 7. デプロイ環境

**本番稼働中**

- フロントエンド: Vercel
- バックエンド: GCP Cloud Run
- データベース: Neon PostgreSQL

---

## 8. 今後の拡張予定

### Phase 2
- パスワードリセット機能
- メールアドレス変更機能
- 多言語対応（英語・韓国語）

### Phase 3
- 相性診断機能
- 択日システム
- モバイルアプリ版

---

## 付録：デザイン仕様

### ゴールドカラーパレット（最終版 2025-11-07更新）
```yaml
# プライマリゴールド
PRIMARY_GOLD: #D4AF37      # メインゴールド - ボタン、アイコン、ブランディング
LIGHT_GOLD: #EBCC42        # ライトゴールド - セカンダリボタン、ハイライト
DARK_GOLD: #B8941C         # ダークゴールド - ボタンホバー、シャドウ
PALE_GOLD: #fffbf0         # ペールゴールド - 背景、ホバーエフェクト

# 背景
Background Primary: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%)
Card Background: #FFFFFF
```

### タイポグラフィ（最終版 2025-11-07更新）
```yaml
# ブランドフォント（Golden Peppa ロゴ専用）
Brand Font: 'Indie Flower', cursive
  - Google Fonts CDN: https://fonts.googleapis.com/css2?family=Indie+Flower
  - 特徴: 手書き風、親しみやすい、大人のカジュアル
  - 適用箇所: "Golden Peppa" ロゴタイトルのみ
  - サイズ: xs: 40px, md: 52px, lg: 68px
  - ウェイト: 400
  - レタースペーシング: 1px
  - 色: #D4AF37

# 本文フォント
Primary Font: 'Roboto', 'Noto Sans JP', sans-serif
  - 適用箇所: ボタン、フォーム、ナビゲーション、本文

# 四柱推命表示フォント（任意）
Secondary Font: 'Noto Serif JP', serif
  - 適用箇所: 天干・地支などの伝統的表記
```

### ビジュアルアセット（最終版 2025-11-07更新）
```yaml
# メインロゴ（現行）
Logo Image: /public/images/peppa-with-sparkles.png
  - 説明: ゴールデンペッパーミル + キラキラエフェクト統合画像
  - サイズ: xs: 160px, md: 200px, lg: 240px
  - 配置: 中央揃え（display: block, margin: auto）
  - 変更日: 2025-11-07
  - 変更理由: レイアウト安定性向上（5枚→1枚統合）

# 旧アセット（非推奨、ローディングアニメーションでのみ使用）
Old Assets:
  - /public/images/peppa.png
  - /public/images/キラキラ1.png
  - /public/images/キラキラ2.png
  - /public/images/キラキラ3.png
  - /public/images/キラキラ4.png
  - /public/images/左下光線.png
  - /public/images/右上光線.png
```

### 五行カラーシステム
```yaml
木: #4CAF50（緑）
火: #F44336（赤）
土: #FFB300（黄/オレンジ）
金: #BDBDBD（グレー/白）
水: #424242（黒/ダークグレー）
```

### 吉凶カラーシステム（7段階）
```yaml
大吉: #FFD700（ゴールド）
小吉: #4CAF50（緑）
吉: #4CAF50（緑）
吉凶: #9E9E9E（グレー）
平: #9E9E9E（グレー）
凶: #FF9800（オレンジ）
大凶: #F44336（赤）
```

**注**: FortuneLevel型は7段階だが、表示上は5色で視覚化（小吉=吉、吉凶=平）

---

## 9. UI/UXデザイン指針

**実装済み**（2025-11-09）

- Golden Peppaローディングアニメーション
- ゴールドテーマボタン
- レスポンシブ対応完全実装
- 統一デザインシステム（`cardStyles.ts`）
- 水平スクロール対応
- タップ領域最適化（Apple HIG準拠）
- エラー表示・削除確認ダイアログ

**参照先**
- `frontend/src/components/GoldenPeppaLoading.tsx`
- `frontend/src/constants/cardStyles.ts`
- `frontend/src/App.tsx`

---

## 🆕 機能拡張要件 - 命式修正機能（Phase 2）

### 拡張概要
- **機能名**: 命式修正機能（モーダルダイアログ形式）
- **目的**: ListPageで保存済み命式を編集できるようにする
- **解決する課題**: 現在は削除して再入力するしかない（ユーザーの負担が大きい）
- **期待効果**: 入力ミスの修正が容易になり、ユーザー体験が向上

### 確定した仕様

| 項目 | 仕様 |
|------|------|
| **編集ボタン配置** | 削除ボタンの横に編集アイコン（鉛筆マーク） |
| **編集画面UI** | モーダルダイアログ（ListPage上にオーバーレイ表示） |
| **編集可能項目** | 名前・生年月日時・性別すべて編集可能 |
| **ゲストモード** | ゲストモードでも編集可能（LocalStorage更新） |
| **保存後の遷移** | モーダルを閉じて、ListPageで更新された命式を表示 |

### 実装計画

#### 新規作成するファイル
1. **frontend/src/components/SajuInputForm.tsx** - TopPageとモーダルで共用するフォームコンポーネント
2. **frontend/src/pages/ListPage/components/EditSajuModal.tsx** - 編集モーダルコンポーネント
3. **frontend/src/services/api/sajuUpdateService.ts** - 命式更新API呼び出しサービス
4. **backend/app/api/saju.py** - PUT /api/saju/:id エンドポイント追加

#### 修正するファイル
1. **frontend/src/pages/ListPage/components/SajuCard.tsx** - 編集ボタン追加
2. **frontend/src/pages/ListPage/index.tsx** - モーダル状態管理追加
3. **frontend/src/pages/TopPage/index.tsx** - フォームをSajuInputFormに置き換え

#### APIエンドポイント
- **PUT /api/saju/:id** - 命式更新専用エンドポイント
  - 権限チェック（自分の命式のみ更新可能）
  - 生年月日時・性別が変更された場合は四柱推命を自動で再計算
  - 名前のみ変更の場合は再計算不要

#### モックアップ
- **mockups/ListPage-EditButton.html** - 編集ボタン付きSajuCard
- **mockups/EditSajuModal.html** - 編集モーダルダイアログ

### 見積もり
- **合計工数**: 8時間
- **新規ファイル**: 3個
- **修正ファイル**: 3個
- **新規APIエンドポイント**: 1個

---

## 🆕 機能拡張要件 - 設定ページ拡張（Phase 2）

### 拡張概要
- **機能名**: 設定ページ機能拡張
- **目的**: SettingsPage_Responsive.htmlモックアップに合わせた機能追加
- **解決する課題**: 現在の設定ページは基本的な機能のみ（ログイン/ログアウト、データエクスポート、アプリ情報表示のみ）
- **期待効果**: ユーザーがアプリの動作をカスタマイズでき、より充実した設定画面を提供

### 追加する機能

#### 1. ユーザー情報カード（ログインユーザーのみ）
- **デザイン**: ゴールドグラデーション背景
- **表示内容**:
  - アバター（白い円に名前の最初の文字）
  - ユーザー名
  - メールアドレス

#### 2. アカウント設定セクション拡張
- **パスワード変更機能** - クリックでパスワード変更モーダル表示
- **アカウント削除機能** - クリックで確認ダイアログ→削除実行
- **ログアウト後の遷移** - ログアウト後はLoginPageに遷移（現在は設定ページリロード）

#### 3. 通知設定セクション（新規）
- **プッシュ通知** - ON/OFFスイッチ
- **メール通知** - ON/OFFスイッチ
- **運勢リマインダー** - ON/OFFスイッチ（毎日の運勢を通知）

#### 4. 表示設定セクション（新規）
- **ダークモード** - ON/OFFスイッチ（全画面のテーマ切り替え）
- **グラフアニメーション** - ON/OFFスイッチ（人生グラフのアニメーション有無）

#### 5. データ管理セクション拡張
- **データインポート機能** - JSON形式でデータをインポート

#### 6. その他セクション（新規）
- **利用規約** - クリックで利用規約ページに遷移
- **プライバシーポリシー** - クリックでプライバシーポリシーページに遷移
- **アプリバージョン** - 現在のバージョン表示（v1.0.0）

### 実装計画

#### 新規作成するファイル
1. **frontend/src/pages/SettingsPage/components/UserCard.tsx** - ユーザー情報カード
2. **frontend/src/pages/SettingsPage/components/SettingSwitch.tsx** - ON/OFFスイッチコンポーネント
3. **frontend/src/pages/SettingsPage/components/PasswordChangeModal.tsx** - パスワード変更モーダル
4. **frontend/src/pages/SettingsPage/components/AccountDeleteDialog.tsx** - アカウント削除確認ダイアログ
5. **frontend/src/pages/SettingsPage/hooks/useSettings.ts** - 設定管理カスタムフック
6. **frontend/src/services/api/settingsService.ts** - 設定API呼び出しサービス
7. **frontend/src/pages/TermsPage.tsx** - 利用規約ページ
8. **frontend/src/pages/PrivacyPage.tsx** - プライバシーポリシーページ
9. **backend/app/api/settings.py** - 設定管理APIエンドポイント
10. **backend/app/api/auth.py** - パスワード変更・アカウント削除エンドポイント追加

#### 修正するファイル
1. **frontend/src/pages/SettingsPage.tsx** - 全機能を統合 + ログアウト後にLoginPageへ遷移
2. **frontend/src/App.tsx** - 利用規約・プライバシーポリシーページのルート追加
3. **backend/app/models/user.py** - 通知設定・表示設定フィールド追加
4. **backend/app/models/saju.py** - データインポート対応

#### APIエンドポイント
- **GET /api/settings** - ユーザー設定取得
- **PUT /api/settings** - ユーザー設定更新
- **POST /api/auth/change-password** - パスワード変更
- **DELETE /api/auth/account** - アカウント削除
- **POST /api/saju/import** - データインポート

#### データベース（PostgreSQL）
- **user_settings テーブル追加**
  ```sql
  CREATE TABLE user_settings (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    push_notifications BOOLEAN DEFAULT TRUE,
    email_notifications BOOLEAN DEFAULT FALSE,
    fortune_reminder BOOLEAN DEFAULT TRUE,
    dark_mode BOOLEAN DEFAULT FALSE,
    graph_animation BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
  );
  ```

### 見積もり
- **合計工数**: 16時間
- **新規ファイル**: 10個（フロントエンド8個、バックエンド2個）
- **修正ファイル**: 4個
- **新規APIエンドポイント**: 5個
- **データベース変更**: 1テーブル追加

### 優先度
- **Phase 2-B**: 命式修正機能（Phase 2-A）の後に実装

---

## 🆕 機能拡張要件 - 多言語対応（韓国語化）（Phase 3）

### 拡張概要
- **機能名**: 多言語対応（韓国語・日本語）
- **目的**: 韓国語ユーザーをメインターゲットにする
- **解決する課題**: 現在は日本語のみで韓国語話者が利用できない
- **期待効果**: 韓国市場への展開が可能になる

### 確定した仕様

| 項目 | 仕様 |
|------|------|
| **対応言語** | 韓国語（デフォルト）、日本語 |
| **デフォルト言語** | 韓国語（ko） |
| **言語切り替え方法** | 設定ページに言語選択ドロップダウン追加 |
| **翻訳対象** | UIテキスト全体（ボタン、ラベル、メッセージ、エラー、吉凶、十神等） |
| **翻訳対象外** | 命式ボックス内の天干・地支（甲子、壬申等）のみ、ユーザー入力データ |
| **初回起動時** | 韓国語で表示 |
| **言語設定保存** | LocalStorage（ゲストモード）、DB（ログインモード） |

### 実装計画

#### 新規作成するファイル
1. **frontend/src/i18n.ts** - i18n設定ファイル
2. **frontend/src/locales/ko/translation.json** - 韓国語翻訳ファイル
3. **frontend/src/locales/ja/translation.json** - 日本語翻訳ファイル
4. **frontend/src/pages/SettingsPage/components/LanguageSelector.tsx** - 言語選択コンポーネント

#### 修正するファイル
1. **frontend/src/App.tsx** - i18nインポート追加
2. **frontend/src/pages/TopPage/index.tsx** - i18n対応
3. **frontend/src/pages/ListPage/index.tsx** - i18n対応
4. **frontend/src/pages/DetailPage.tsx** - i18n対応
5. **frontend/src/pages/LoginPage.tsx** - i18n対応
6. **frontend/src/pages/RegisterPage.tsx** - i18n対応
7. **frontend/src/pages/SettingsPage.tsx** - i18n対応 + LanguageSelector追加
8. **frontend/src/components/BottomNavigation.tsx** - i18n対応
9. **backend/app/models/user_settings.py** - languageフィールド追加
10. **backend/app/types/settings.py** - languageフィールド追加

#### データベース（PostgreSQL）
- **user_settings テーブル更新**
  ```sql
  ALTER TABLE user_settings ADD COLUMN language VARCHAR(5) DEFAULT 'ko';
  ```

#### パッケージ追加
- **frontend**: react-i18next, i18next, i18next-browser-languagedetector

### 翻訳例

**重要**: 命式ボックス内の天干・地支（甲子、壬申等）は翻訳しません。それ以外は翻訳します。

#### UIテキストの翻訳

| 日本語 | 韓国語 |
|--------|--------|
| ログイン | 로그인 |
| 命式記入 | 사주 기입 |
| 保存した命式 | 저장된 사주 |
| 設定 | 설정 |
| 生年月日 | 생년월일 |
| 性別 | 성별 |
| 男性 | 남성 |
| 女性 | 여성 |
| 計算 | 계산 |
| 保存 | 저장 |

#### 吉凶・十神の翻訳（命式ボックス外）

| 日本語 | 韓国語 | 備考 |
|--------|--------|------|
| 大吉 | 대길 | 翻訳する |
| 吉 | 길 | 翻訳する |
| 凶 | 흉 | 翻訳する |
| 大凶 | 대흉 | 翻訳する |
| 比肩 | 비견 | 翻訳する |
| 偏印 | 편인 | 翻訳する |
| 正財 | 정재 | 翻訳する |
| 年柱 | 연주 | 翻訳する |
| 月柱 | 월주 | 翻訳する |
| 日柱 | 일주 | 翻訳する |
| 時柱 | 시주 | 翻訳する |

#### 翻訳しないもの（命式ボックス内のみ）

| 項目 | 例 | 備考 |
|------|-----|------|
| 天干 | 甲, 乙, 丙, 丁, 戊, 己, 庚, 辛, 壬, 癸 | 漢字のまま |
| 地支 | 子, 丑, 寅, 卯, 辰, 巳, 午, 未, 申, 酉, 戌, 亥 | 漢字のまま |

### 見積もり
- **合計工数**: 15時間
- **新規ファイル**: 4個
- **修正ファイル**: 10個
- **データベース変更**: user_settings.language フィールド追加

### 優先度
- **Phase 3**: Phase 2（命式修正機能・設定ページ拡張）の後に実装

---

## 📝 モックアップ更新履歴

### Phase 2 機能拡張に伴うモックアップ更新

| ファイル | 更新日 | 更新内容 |
|---------|--------|---------|
| **ListPage-EditButton.html** | 2025-11-11 | 実装デザインに統一（ゴールドグラデーションヘッダー、白背景） |
| **EditSajuModal.html** | 2025-11-11 | 実装デザインに統一（白背景） |
| **SettingsPage_Responsive.html** | 2025-11-11 | 実装デザインに統一 + ユーザー情報カードレイアウト変更（アバター横に名前・メールアドレス） |
| **LoginPage_Responsive.html** | 2025-11-11 | ロゴテキストを "Golden Peppa" に統一 |

---

**作成日**: 2025年11月1日
**最終更新**: 2025年11月11日 16:50

