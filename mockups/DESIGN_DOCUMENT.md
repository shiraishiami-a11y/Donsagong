# Golden Peppa - UI/UXデザインドキュメント

## 1. プロジェクト概要

### 1.1 アプリケーション名
**Golden Peppa（ゴールデン四柱推命）**
英語名: Golden Saju Fortune

### 1.2 ブランディング
- **タグライン**: あなたの運命に魔法をかける
- **シンボル**: ゴールデンペッパーミル（peppa.png）
- **コンセプト**: 伝統的な四柱推命に「魔法」のような親しみやすさとワクワク感を加えた、現代的で楽しいアプリケーション

### 1.3 デザインコンセプト
210年節気データベース統合による高精度四柱推命アプリケーションとして、**伝統と遊び心の融合**をテーマに、ゴールドの輝きと手書き風のフレンドリーなタイポグラフィで、専門性と親しみやすさを両立させたデザイン。

### 1.4 設計思想
- **信頼性の視覚化**: 210年データベースの正確性を表現
- **親しみやすさ**: 専門的な内容を初心者にも分かりやすく、楽しく
- **効率性**: 複雑な計算結果を直感的に理解できる表示
- **継続利用**: ユーザーが長期的に使い続けたくなるUX
- **魔法のような体験**: ゴールドとキラキラエフェクトで特別感を演出

## 2. 作成済みモックアップ一覧

### 2.1 完成ページ
- **P-001**: 四柱推命入力・計算ページ (`P-001-saju-calculation.html`)
- **P-002**: 相性診断ページ (`P-002-compatibility-analysis.html`)
- **P-003**: 大運分析ページ (`P-003-daeun-analysis.html`)
- **P-004**: データ管理ページ (`P-004-data-management.html`)

### 2.2 技術スタック
- **フレームワーク**: React 18 + TypeScript
- **UIライブラリ**: Material-UI v5
- **スタイリング**: CSS-in-JS + カスタムCSS
- **レスポンシブ**: Mobile-first アプローチ

## 3. デザインシステム

### 3.1 カラーパレット

#### ゴールデンパレット（メインカラー）
```css
/* プライマリゴールド */
PRIMARY_GOLD: #D4AF37     /* メインゴールド - ボタン、アイコン、ブランディング */
LIGHT_GOLD: #EBCC42       /* ライトゴールド - ボタンホバー、ハイライト */
DARK_GOLD: #B8941C        /* ダークゴールド - ボタンホバー、シャドウ */
PALE_GOLD: #fffbf0        /* ペールゴールド - 背景、ホバーエフェクト */

/* グラデーション背景 */
Background Primary: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%)
Card Background: white
```

#### 五行カラー（四柱推命表示用）
```css
WOOD: #4CAF50            /* 木（緑） */
FIRE: #F44336            /* 火（赤） */
EARTH: #FFB300           /* 土（黄/オレンジ） */
METAL: #BDBDBD           /* 金（グレー/白） */
WATER: #424242           /* 水（黒/ダークグレー） */
```

#### 吉凶カラー（運勢レベル表示用）
```css
GREAT_FORTUNE: #FFD700   /* 大吉（ゴールド） */
FORTUNE: #4CAF50         /* 吉（緑） */
NEUTRAL: #9E9E9E         /* 平（グレー） */
MISFORTUNE: #FF9800      /* 凶（オレンジ） */
GREAT_MISFORTUNE: #F44336 /* 大凶（赤） */
```

#### システムカラー
```css
/* 成功・警告・エラー */
Success: #4caf50
Warning: #ff9800
Error: #f44336
Info: #2196f3

/* テキスト */
Text Primary: #1a1a2e
Text Secondary: #333
Text Tertiary: #666

/* ボーダー・背景 */
Border: #e0e0e0
Background Card: white
Background Overlay: rgba(255, 255, 255, 0.95)
```

### 3.2 タイポグラフィ

#### フォントファミリー
```css
/* ブランディング（Golden Peppa ロゴ専用） */
Brand: 'Indie Flower', cursive
  - 適用箇所: "Golden Peppa" ロゴタイトル
  - 特徴: 手書き風、親しみやすい、子供っぽくない大人のカジュアル
  - ウェイト: 400（通常）
  - レタースペーシング: 1px

/* 本文・UI */
Primary: 'Roboto', 'Noto Sans JP', sans-serif
  - 適用箇所: ボタン、フォーム、ナビゲーション、本文
  - 可読性重視の標準フォント

/* 四柱推命表示（任意） */
Secondary: 'Noto Serif JP', serif
  - 適用箇所: 天干・地支などの四柱推命文字
  - 伝統的な表示が必要な箇所のみ使用
```

#### Google Fonts読み込み
```html
<!-- index.html に追加済み -->
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Indie+Flower&display=swap" rel="stylesheet" />
```

#### フォントサイズ階層
```css
/* ブランドタイトル（Golden Peppa） */
Brand Title:
  - Desktop (lg): 68px
  - Tablet (md): 52px
  - Mobile (xs): 40px
  - fontWeight: 400
  - color: #D4AF37
  - letterSpacing: 1px
  - fontFamily: 'Indie Flower', cursive

/* セクションタイトル */
h1 (Main Title): 2.5rem (40px) - モバイル: 2rem (32px)
h2 (Section Title): 1.5rem (24px)
h3 (Subsection): 1.2rem (19px)

/* 本文 */
Body: 1rem (16px)
Small: 0.9rem (14px)
Caption: 0.8rem (13px)
Micro: 0.7rem (11px)
```

### 3.3 レイアウトシステム

#### グリッドシステム
```css
/* デスクトップ */
Container Max-width: 1200px - 1400px
Columns: 12 column grid
Gutter: 20px - 30px

/* タブレット */
Container: 100% with 20px padding
Columns: Flexible 2-3 columns

/* モバイル */
Container: 100% with 15px padding
Columns: Single column
```

#### 間隔システム
```css
Space-xs: 5px
Space-sm: 10px
Space-md: 15px
Space-lg: 20px
Space-xl: 30px
Space-2xl: 40px
```

### 3.4 ビジュアルアセット

#### ロゴとアイコン
```yaml
メインロゴ:
  - ファイル: /public/images/peppa-with-sparkles.png
  - 説明: ゴールデンペッパーミル + キラキラエフェクト統合画像
  - サイズ:
    - Desktop (lg): 240x240px
    - Tablet (md): 200x200px
    - Mobile (xs): 160x160px
  - 配置: 中央揃え（marginLeft/Right: auto）
  - 備考: 以前は peppa.png + キラキラ1-4.png の5枚を個別配置していたが、
         レイアウトの安定性のため1枚の統合画像に変更（2025-11-07）

旧アセット（非推奨）:
  - /public/images/peppa.png（80-120px）
  - /public/images/キラキラ1.png
  - /public/images/キラキラ2.png
  - /public/images/キラキラ3.png
  - /public/images/キラキラ4.png
  - /public/images/左下光線.png
  - /public/images/右上光線.png
  ※ ローディングアニメーション（GoldenPeppaLoading）では引き続き使用
```

#### キラキラエフェクト
```css
/* ローディングアニメーション用 */
- キラキラ1: 25x25px
- キラキラ2: 25x25px（opacity: 0.8）
- キラキラ3: 20x20px（45度回転）
- キラキラ4: 12.5x12.5px
- アニメーション: sparkleFall（3.2s、降下＆回転）
```

### 3.5 コンポーネント設計

#### 基本コンポーネント
```css
/* カード */
.card {
  background: white;
  border-radius: 16px-24px;  /* レスポンシブ対応 */
  padding: 24px-60px;        /* レスポンシブ対応 */
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

/* ボタン - プライマリ */
.button-primary {
  background: #D4AF37;      /* PRIMARY_GOLD */
  color: white;
  border-radius: 12px-16px; /* レスポンシブ対応 */
  padding: 16px-20px;
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);
  transition: all 0.2s;
  text-transform: none;     /* MUIデフォルトの大文字化を無効 */
}

.button-primary:hover {
  background: #B8941C;      /* DARK_GOLD */
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(212, 175, 55, 0.4);
}

.button-primary:active {
  transform: translateY(0);
}

/* ボタン - セカンダリ（命式詳細ページ等） */
.button-secondary {
  background: #EBCC42;      /* LIGHT_GOLD */
  color: white;
  border-radius: 8px;
  padding: 10px 24px;
  font-weight: 600;
  box-shadow: none;         /* シャドウなし */
  transition: all 0.2s;
}

.button-secondary:hover {
  background: #D4AF37;
}

/* 入力フィールド */
.input-field {
  border: 2px solid #e0e0e0;
  border-radius: 8px-12px;  /* レスポンシブ対応 */
  padding: 12px-20px;
  transition: border-color 0.3s ease;
}

.input-field:hover {
  border-color: #D4AF37;
}

.input-field:focus {
  border-color: #D4AF37;
  box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.1);
}
```

## 4. 最新の実装変更履歴（2025-11-07）

### 4.1 ブランディング変更
```yaml
変更内容:
  - アプリ名: 四柱推命アプリ → Golden Peppa
  - タグライン: あなたの運命に魔法をかける
  - ロゴ: ゴールデンペッパーミル + キラキラエフェクト
  - コンセプト: 伝統的 → 親しみやすく魔法のような体験

影響範囲:
  - TopPage（トップページ）
  - GoldenPeppaLoading（ローディングアニメーション）
  - index.html（タイトルタグ）
```

### 4.2 フォント変更
```yaml
変更内容:
  - "Golden Peppa" ロゴ専用フォント追加
  - フォント名: Indie Flower（Google Fonts）
  - 特徴: 手書き風、親しみやすい、大人のカジュアル
  - 検討候補: Great Vibes（却下：装飾的すぎ）、Caveat、Patrick Hand、Shadows Into Light

実装:
  - index.html: Google Fonts CDN追加
  - TopPage: fontFamily: "'Indie Flower', cursive"
  - GoldenPeppaLoading: fontFamily: "'Indie Flower', cursive"

サイズ:
  - TopPage: xs: 40px, md: 52px, lg: 68px
  - GoldenPeppaLoading: 48px（固定）
```

### 4.3 ロゴ画像統合
```yaml
変更前（2025-11-06まで）:
  - peppa.png（80-120px）を中央配置
  - キラキラ1-4.png を absolute positioning で個別配置
  - 合計5枚の画像を複雑な座標計算で配置
  - 問題: レスポンシブ時にレイアウトが崩れやすい

変更後（2025-11-07）:
  - peppa-with-sparkles.png 1枚の統合画像
  - 160-240px レスポンシブサイズ
  - display: block, margin: auto で中央揃え
  - メリット: レイアウト安定、コード簡潔化

旧実装（20回以上の位置調整を経て統合決定）:
  - キラキラ1: 右40px、下50px 移動
  - キラキラ2: opacity 0.8、下80px
  - キラキラ3: 45度回転、20x20px
  - キラキラ4: 右左微調整
  - ペッパーミル: 左80px移動
  → 最終的に1枚画像に統合して解決
```

### 4.4 ボタンスタイリング統一
```yaml
トップページ（計算ボタン）:
  - background: #D4AF37（PRIMARY_GOLD）
  - color: white
  - boxShadow: 0 4px 12px rgba(212, 175, 55, 0.3)
  - hover: #B8941C、translateY(-2px)

命式詳細ページ（保存・削除ボタン）:
  - background: #EBCC42（LIGHT_GOLD）
  - color: white
  - boxShadow: none（シャドウなし）
  - padding: 10px 24px
  - borderRadius: 8px

変更理由:
  - 統一感のあるゴールドテーマ
  - 視認性向上（白文字）
  - シャドウ削減でモダンな印象
```

### 4.5 機能実装
```yaml
保存機能:
  - LocalStorage へ命式データ保存
  - 既存データがあれば更新、なければ追加
  - 実装箇所: TopPage handleCalculate関数

削除機能:
  - LocalStorage から命式データ削除
  - 削除後に一覧ページへ遷移
  - 実装箇所: SajuDetailPage handleDelete関数

ナビゲーション:
  - 全ページにボトムナビゲーション追加
  - paddingBottom: 90-100px で余白確保
  - BottomNavigation コンポーネント共通化

ページクリーンアップ:
  - ListPage: 重複ボタン削除
  - SettingsPage: サイドバー削除（シンプル化）
```

### 4.6 既知の問題（未修正）
```yaml
SajuDetailPage レスポンシブ問題:
  - 現象: 小画面で右側が切れる
  - 原因: レスポンシブレイアウト設計の問題
  - ステータス: 要件定義レベルで修正予定
  - 優先度: 高（次のタスク）

対応方針:
  1. DESIGN_DOCUMENT.md でレスポンシブ要件を明確化
  2. requirements.md で実装要件を更新
  3. 実装修正
```

## 5. 各ページ詳細設計

### 5.1 P-001: 四柱推命計算ページ（TopPage）

#### 設計意図
- **魔法のような体験**: Golden Peppa ブランディングで親しみやすく
- **シンプルな入力**: 必要最小限の入力項目で操作の迷いを排除
- **即時保存**: 計算後すぐに LocalStorage（ゲスト）or サーバー（ログイン）に保存
- **スムーズな遷移**: 計算 → 保存 → 詳細ページへ自動遷移

#### 現在の実装（2025-11-07時点）
```yaml
ヘッダーセクション:
  - Golden Peppa ロゴ画像: peppa-with-sparkles.png（160-240px）
  - タイトル: "Golden Peppa"（Indie Flower、40-68px）
  - タグライン: "あなたの運命に魔法をかける"

入力フォーム:
  1. 名前入力（任意）
     - プレースホルダー: "白石"
     - フォーカス時: ゴールドボーダー (#D4AF37)

  2. 生年月日時入力
     - DatePicker: yyyy年MM月dd日形式
     - TimePicker: HH:mm形式（24時間）
     - チェックボックス: "時刻不明（正午12:00で計算）"
     - 範囲制限: 1900-2109年
     - フォーカス時: ゴールドボーダー + シャドウ

  3. 性別選択
     - ビジュアルボタン: 男性👨、女性👩
     - 選択時: ゴールド背景 (#D4AF37)、白文字
     - ホバー時: ペールゴールド背景 (#fffbf0)

計算ボタン:
  - テキスト: "命式を計算"
  - アイコン: Calculate
  - スタイル: PRIMARY_GOLD、白文字、シャドウあり
  - ホバー: DARK_GOLD、上昇アニメーション

処理フロー:
  1. バリデーション実行
  2. ローディングアニメーション表示（GoldenPeppaLoading）
  3. FastAPI へ命式計算リクエスト
  4. LocalStorage へ自動保存（ゲストモード）
  5. 詳細ページへ遷移（/detail/:id）
```

#### 主要機能
1. **生年月日時入力フォーム**: 直感的な日時ピッカー
2. **性別選択**: ビジュアルなボタン選択
3. **時刻不明対応**: 正午12:00でデフォルト計算
4. **自動保存**: 計算完了後に即保存
5. **ローディング**: Golden Peppa アニメーション表示

#### 実装注意点
```typescript
// API統合ポイント
interface BirthDataRequest {
  birth_datetime: Date;
  gender: 'male' | 'female';
  timezone_offset: number;
}

// 状態管理
const [calculationResult, setCalculationResult] = useState<SajuResponse | null>(null);
const [isLoading, setIsLoading] = useState(false);

// バリデーション
const validateBirthData = (data: BirthDataRequest): boolean => {
  // 生年月日の範囲チェック（1900-2109年）
  // 時刻の有効性チェック
  // 性別選択チェック
}
```

### 4.2 P-002: 相性診断ページ

#### 設計意図
- **比較の明確化**: 二人の情報を対比しやすいレイアウト
- **スコアの視覚化**: 数値だけでなく色とグラフで直感的理解
- **マトリックス表示**: 複雑な分析結果を整理して表示

#### 主要機能
1. **二人分入力フォーム**: 区別しやすいデザイン
2. **総合スコア表示**: 大きく分かりやすい数値
3. **天干マトリックス**: インタラクティブな表示
4. **詳細解説**: ドンサゴン分析による説明

#### 実装注意点
```typescript
// 複雑な計算結果の処理
interface CompatibilityResponse {
  overall_score: number;
  stem_analysis: Record<string, StemCompatibility>;
  branch_analysis: Record<string, BranchCompatibility>;
  detailed_explanation: string;
}

// マトリックス表示の最適化
const renderMatrix = useMemo(() => {
  // 100組合せの天干マトリックス
  // 144組合せの地支調候表
  // パフォーマンス考慮した描画
}, [compatibilityData]);
```

### 4.3 P-003: 大運分析ページ

#### 設計意図
- **時系列の明確化**: タイムライン形式で人生の流れを表現
- **現在の強調**: 現在運勢を視覚的にハイライト
- **未来予測**: 重要時期の予測を分かりやすく表示

#### 主要機能
1. **サイドバー概要**: 現在状況と重要時期の要約
2. **大運タイムライン**: 10年周期の流れ表示
3. **詳細分析**: 各大運期の特徴と対策
4. **年運組み合わせ**: 近年の詳細予測

#### 実装注意点
```typescript
// タイムライン表示の最適化
interface DaeunPeriod {
  start_age: number;
  end_age: number;
  daeun_stem: string;
  daeun_branch: string;
  characteristics: string[];
  is_current: boolean;
}

// スクロール連動ナビゲーション
const handleScroll = useCallback(() => {
  // セクション判定とナビゲーション更新
}, []);
```

### 4.4 P-004: データ管理ページ

#### 設計意図
- **効率的な検索**: 複数フィルターによる絞り込み機能
- **履歴管理**: 使いやすい一覧表示と操作
- **データ保護**: バックアップ・復元機能の提供

#### 主要機能
1. **検索・フィルター**: リアルタイム検索と複数条件絞り込み
2. **データ一覧**: カード形式での見やすい表示
3. **お気に入り管理**: 重要データの迅速アクセス
4. **エクスポート機能**: 複数形式での出力対応

#### 実装注意点
```typescript
// ページネーションとフィルタリング
interface DataFilter {
  type?: 'saju' | 'compatibility' | 'daeun';
  date_range?: string;
  favorite_only?: boolean;
  search_query?: string;
}

// 大量データの効率的処理
const useDataList = () => {
  const [data, setData] = useState<CalculationHistory[]>([]);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);

  // 仮想スクロール or ページネーション実装
};
```

## 6. レスポンシブデザイン戦略

### 6.1 ブレークポイント（MUI標準準拠）
```css
/* モバイル優先設計 */
xs (mobile): 0px - 599px
sm (small tablet): 600px - 899px
md (tablet): 900px - 1199px
lg (desktop): 1200px - 1535px
xl (large desktop): 1536px+
```

### 6.2 各デバイスでの最適化

#### モバイル（xs: 0-599px）
```yaml
レイアウト:
  - シングルカラムレイアウト
  - 全幅カード（padding: 15-20px）
  - ボトムナビゲーション固定

タイポグラフィ:
  - Golden Peppa ロゴ: 40px
  - タグライン: 14px
  - セクションタイトル: 20px
  - 本文: 16px

インタラクション:
  - タッチターゲット: 最低44x44px
  - ボタン padding: 16px
  - スワイプ操作対応
  - ホバー効果なし

間隔:
  - カード間: 20px
  - セクション間: 24px
  - paddingBottom: 90px（ボトムナビ分）
```

#### タブレット（md: 900-1199px）
```yaml
レイアウト:
  - 2カラムレイアウト（必要に応じて）
  - カードmax-width: 600px
  - 中央揃え配置

タイポグラフィ:
  - Golden Peppa ロゴ: 52px
  - タグライン: 16px
  - セクションタイトル: 24px

インタラクション:
  - タッチ + マウス両対応
  - ホバー効果あり

間隔:
  - カード間: 30px
  - セクション間: 32px
  - paddingBottom: 100px
```

#### デスクトップ（lg: 1200px+）
```yaml
レイアウト:
  - マルチカラムレイアウト
  - カードmax-width: 800px
  - サイドバー表示（一部ページ）

タイポグラフィ:
  - Golden Peppa ロゴ: 68px
  - タグライン: 18px
  - セクションタイトル: 28px

インタラクション:
  - マウス操作最適化
  - ホバー効果フル活用
  - キーボードショートカット

間隔:
  - カード間: 40px
  - セクション間: 40px
```

### 6.3 レスポンシブ実装パターン

#### MUI sx prop パターン
```typescript
<Box sx={{
  // モバイルファースト: デフォルト値 = xs
  fontSize: '14px',
  padding: '16px',
  width: '100%',

  // タブレット以上
  md: {
    fontSize: '16px',
    padding: '24px',
    maxWidth: '600px',
  },

  // デスクトップ以上
  lg: {
    fontSize: '18px',
    padding: '32px',
    maxWidth: '800px',
  },
}}>
```

#### 統一されたブレークポイント使用
```typescript
// 全コンポーネントで統一
sx={{
  fontSize: { xs: '14px', md: '16px', lg: '18px' },
  padding: { xs: '16px', md: '24px', lg: '32px' },
  borderRadius: { xs: '8px', md: '12px', lg: '16px' },
}}
```

### 6.4 既知のレスポンシブ問題と修正方針

#### SajuDetailPage 右側切れ問題
```yaml
現象:
  - 小画面（xs, sm）で右側コンテンツが画面外に
  - 水平スクロールバーが表示される場合あり
  - 主に命式表示部分（四柱表示）で発生

原因推定:
  - 固定幅のテーブルまたはグリッド使用
  - overflow 設定不足
  - min-width 制約が厳しすぎる

修正方針:
  1. 全てのテーブル・グリッドを responsive 化
  2. xs, sm ブレークポイントでシングルカラム化
  3. overflow-x: auto 追加（必要な箇所のみ）
  4. min-width 制約を見直し
  5. テスト: 320px幅で全ページ確認

優先度: 高（次のタスク）
```

### 5.3 実装例
```css
/* Mobile First */
.main-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}

/* Tablet */
@media (min-width: 768px) {
  .main-content {
    grid-template-columns: 300px 1fr;
    gap: 25px;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .main-content {
    grid-template-columns: 300px 1fr 300px;
    gap: 30px;
  }
}
```

## 6. アクセシビリティ対応

### 6.1 WCAG 2.1 AA準拠

#### 色彩設計
- **コントラスト比**: 4.5:1以上確保
- **色だけに依存しない情報伝達**
- **カラーブラインド対応**

#### キーボード操作
```typescript
// キーボードナビゲーション
const handleKeyDown = (event: KeyboardEvent) => {
  switch (event.key) {
    case 'Tab':
      // フォーカス順序管理
      break;
    case 'Enter':
    case ' ':
      // ボタン・リンク実行
      break;
    case 'Escape':
      // モーダル・ドロップダウン閉じる
      break;
  }
};
```

#### スクリーンリーダー対応
```html
<!-- 適切なARIAラベル -->
<button
  aria-label="四柱推命を計算する"
  aria-describedby="calculation-help"
>
  計算実行
</button>

<!-- セマンティックHTML -->
<main role="main">
  <section aria-labelledby="results-title">
    <h2 id="results-title">計算結果</h2>
  </section>
</main>
```

### 6.2 ユーザビリティ配慮
- **明確なフィードバック**: 処理状況の表示
- **エラーハンドリング**: 分かりやすいエラーメッセージ
- **ヘルプ機能**: 初心者向けガイダンス

## 7. パフォーマンス最適化

### 7.1 読み込み速度最適化

#### Code Splitting
```typescript
// ページレベルの遅延読み込み
const SajuCalculation = lazy(() => import('./pages/SajuCalculation'));
const CompatibilityAnalysis = lazy(() => import('./pages/CompatibilityAnalysis'));
const DaeunAnalysis = lazy(() => import('./pages/DaeunAnalysis'));
const DataManagement = lazy(() => import('./pages/DataManagement'));
```

#### 画像最適化
```css
/* WebP対応とフォールバック */
.background-image {
  background-image: url('image.webp');
  background-image: url('image.jpg'); /* フォールバック */
}

/* レスポンシブ画像 */
img {
  max-width: 100%;
  height: auto;
  loading: lazy;
}
```

### 7.2 レンダリング最適化

#### React最適化
```typescript
// メモ化による再レンダリング防止
const PillarCard = memo(({ pillar }: { pillar: Pillar }) => {
  return (
    <div className="pillar-card">
      {/* ... */}
    </div>
  );
});

// 重い計算のメモ化
const calculatedData = useMemo(() => {
  return expensiveCalculation(inputData);
}, [inputData]);
```

### 7.3 ネットワーク最適化
```typescript
// API呼び出しの最適化
const useApiWithCache = (endpoint: string) => {
  return useQuery({
    queryKey: [endpoint],
    queryFn: () => fetchData(endpoint),
    staleTime: 5 * 60 * 1000, // 5分キャッシュ
    cacheTime: 10 * 60 * 1000, // 10分保持
  });
};
```

## 8. 実装時の技術的注意点

### 8.1 State Management
```typescript
// Zustand による状態管理
interface AppState {
  user: User | null;
  calculations: Calculation[];
  favorites: string[];
  setUser: (user: User) => void;
  addCalculation: (calc: Calculation) => void;
  toggleFavorite: (id: string) => void;
}

const useAppStore = create<AppState>((set) => ({
  user: null,
  calculations: [],
  favorites: [],
  setUser: (user) => set({ user }),
  addCalculation: (calc) => set((state) => ({
    calculations: [...state.calculations, calc]
  })),
  toggleFavorite: (id) => set((state) => ({
    favorites: state.favorites.includes(id)
      ? state.favorites.filter(fav => fav !== id)
      : [...state.favorites, id]
  })),
}));
```

### 8.2 API統合
```typescript
// OpenAPI Generator使用
import { DefaultApi, Configuration } from './generated/api';

const api = new DefaultApi(new Configuration({
  basePath: process.env.REACT_APP_API_BASE_URL,
  accessToken: () => getAuthToken(),
}));

// エラーハンドリング
const useSajuCalculation = () => {
  return useMutation({
    mutationFn: (data: BirthDataRequest) => api.calculateSaju(data),
    onError: (error) => {
      console.error('Calculation failed:', error);
      toast.error('計算に失敗しました。もう一度お試しください。');
    },
    onSuccess: (result) => {
      toast.success('計算が完了しました');
    },
  });
};
```

### 8.3 データバリデーション
```typescript
// Yup による入力バリデーション
const birthDataSchema = yup.object({
  birth_datetime: yup.date()
    .min(new Date('1900-01-01'), '1900年以降の日付を入力してください')
    .max(new Date('2109-12-31'), '2109年以前の日付を入力してください')
    .required('生年月日は必須です'),
  gender: yup.string()
    .oneOf(['male', 'female'], '性別を選択してください')
    .required('性別は必須です'),
});

// React Hook Form との統合
const { control, handleSubmit, formState: { errors } } = useForm({
  resolver: yupResolver(birthDataSchema),
});
```

## 9. セキュリティ考慮事項

### 9.1 データ保護
```typescript
// 個人情報の暗号化
const encryptPersonalData = (data: PersonalData): string => {
  return CryptoJS.AES.encrypt(JSON.stringify(data), secretKey).toString();
};

// セッション管理
const useSecureSession = () => {
  const [token, setToken] = useState<string | null>(
    () => sessionStorage.getItem('auth_token')
  );

  const logout = useCallback(() => {
    sessionStorage.removeItem('auth_token');
    setToken(null);
  }, []);

  return { token, logout };
};
```

### 9.2 XSS防止
```typescript
// HTML エスケープ
import DOMPurify from 'dompurify';

const SafeHTML: React.FC<{ content: string }> = ({ content }) => {
  const sanitizedContent = DOMPurify.sanitize(content);
  return <div dangerouslySetInnerHTML={{ __html: sanitizedContent }} />;
};
```

## 10. 今後の拡張計画

### 10.1 フェーズ2機能
- **年運詳細分析**: より詳細な年単位分析
- **択日システム**: 重要な日取り選定機能
- **モバイルアプリ**: React Native版開発

### 10.2 UI/UX改善計画
- **ダークモード**: 夜間使用への配慮
- **アニメーション強化**: より滑らかな画面遷移
- **音声ガイド**: アクセシビリティ向上

### 10.3 AI統合
```typescript
// AI による解説文生成
const useAIExplanation = (sajuData: SajuData) => {
  return useQuery({
    queryKey: ['ai-explanation', sajuData.id],
    queryFn: () => api.generateAIExplanation(sajuData),
    enabled: !!sajuData.id,
  });
};
```

## 11. 品質保証

### 11.1 テスト戦略
```typescript
// ユニットテスト
describe('SajuCalculation', () => {
  test('正常な入力で計算が実行される', () => {
    const input = {
      birth_datetime: new Date('1990-03-15T10:30:00'),
      gender: 'male' as const,
      timezone_offset: 9,
    };

    const result = calculateSaju(input);
    expect(result).toBeDefined();
    expect(result.year_stem).toBeTruthy();
  });
});

// インテグレーションテスト
test('API呼び出しと結果表示の統合', async () => {
  render(<SajuCalculationPage />);

  fireEvent.change(screen.getByLabelText('生年月日'), {
    target: { value: '1990-03-15' }
  });
  fireEvent.click(screen.getByText('計算実行'));

  await waitFor(() => {
    expect(screen.getByText('計算結果')).toBeInTheDocument();
  });
});
```

### 11.2 パフォーマンステスト
- **Lighthouse スコア**: 90点以上維持
- **Core Web Vitals**: 全項目Green達成
- **ロードテスト**: 同時100ユーザー対応確認

## 12. 運用・保守

### 12.1 監視項目
- **エラー率**: <1%維持
- **応答時間**: 平均2秒以内
- **ユーザー満足度**: NPS調査実施

### 12.2 更新計画
- **定期バックアップ**: 日次自動実行
- **セキュリティ更新**: 月次適用
- **機能更新**: 四半期ごとリリース

---

## まとめ

本デザインドキュメントに基づいて実装することで、四柱推命の専門性を保ちながら、現代的で使いやすいアプリケーションを構築できます。特に210年データベースの正確性とドンサゴン分析法の独自性を活かした、他にない価値のあるサービスの提供が可能になります。

実装時は段階的な開発を行い、各フェーズでユーザーフィードバックを収集して改善を重ねることで、より良いユーザー体験を実現していきます。