# 技術的負債レポート

**生成日時**: 2025-11-03
**プロジェクト**: ゴールデン四柱推命アプリケーション

---

## 📊 サマリー

| 指標 | 値 |
|------|-----|
| **総コメント数** | 10件 |
| **優先度：高** | 3件 |
| **優先度：中** | 5件 |
| **優先度：低** | 2件 |

---

## 🔴 優先度：高（実装必須・動作に影響）

### 1. ドンサゴンマトリックス統合（未実装）

**影響度**: 🔴🔴🔴 **CRITICAL**

#### 該当箇所

##### backend/app/services/saju_calculator.py:414
```python
# TODO: ドンサゴンマトリックス統合
return "平"
```
- **関数**: `_analyze_gan_branch_relation()`
- **現状**: 全て「平」を返す暫定実装
- **影響**: 命式分析の精度が著しく低下

##### backend/app/services/fortune_service.py:285
```python
# TODO: ドンサゴンマトリックスを使用した正確な判定
# 現在は簡易的な実装
```
- **関数**: `_judge_fortune_level()`
- **現状**: 簡易的な比肩判定と天干の合判定のみ
- **影響**: 吉凶判定が不正確

#### 推奨対応
1. `docs/DONSAGONG_MASTER_DATABASE.md` から天干100マトリックス・地支144マトリックスをパース
2. マトリックスデータをJSON化してキャッシュ
3. `_analyze_gan_branch_relation()` と `_judge_fortune_level()` で使用
4. ユニットテストで検証（実際の命式データで精度確認）

#### ステータス
- [ ] 未着手
- **予想工数**: 3-5時間
- **ブロッカー**: なし（データベースは既に存在）

---

### 2. 大運計算情報のDB保存（デフォルト値使用中）

**影響度**: 🔴🔴 **HIGH**

#### 該当箇所

##### backend/app/api/saju.py:649
```python
# TODO: DBに保存されていない場合は再計算が必要
daeun_number = 7  # デフォルト値（実際はDBから取得）
is_forward = True  # デフォルト値（実際はDBから取得）
after_birth_years = 7
after_birth_months = 5
after_birth_days = 2
```
- **エンドポイント**: `GET /api/saju/{saju_id}/daeun`
- **現状**: ハードコードされたデフォルト値使用
- **影響**: 全ての命式で同じ大運計算パラメータになる（性別・生年月日時の違いが反映されない）

#### 推奨対応
1. `SajuModel` に大運計算パラメータカラムを追加
   - `daeun_number: int`
   - `is_forward: bool`
   - `after_birth_years: int`
   - `after_birth_months: int`
   - `after_birth_days: int`
2. Alembicマイグレーション作成・実行
3. 命式計算時（`POST /api/saju/calculate`）に保存
4. 既存データのマイグレーション（再計算）

#### ステータス
- [ ] 未着手
- **予想工数**: 2-3時間
- **ブロッカー**: DBスキーマ変更（マイグレーション必須）

---

### 3. 認証実装後のユーザーフィルタリング

**影響度**: 🟡 **MEDIUM** （認証実装前は影響なし）

#### 該当箇所

##### backend/app/api/saju.py:392
```python
# TODO: 認証実装後は current_user.id でフィルタリング
existing_ids_query = db.query(SajuModel.id).filter(SajuModel.user_id.is_(None)).all()
```
- **エンドポイント**: `POST /api/saju/import`
- **現状**: 全ユーザーのデータを参照（`user_id.is_(None)` のみ）
- **影響**: 認証実装後にユーザー間でデータ競合の可能性

#### 推奨対応
1. FastAPI-Users統合後、`current_user` をDependencyで取得
2. クエリを `filter(SajuModel.user_id == current_user.id)` に変更
3. ゲストユーザー（`user_id=None`）の場合は別処理

#### ステータス
- [ ] Phase 3（認証実装時）に対応予定
- **予想工数**: 0.5時間
- **ブロッカー**: 認証機能の実装完了待ち

---

## 🟡 優先度：中（機能追加・改善）

### 4. フロントエンド：保存処理の実装

**影響度**: 🟡 **MEDIUM**

#### 該当箇所

##### frontend/src/pages/SajuDetailPage/index.tsx:175
```tsx
onClick={() => {
  // TODO: 保存処理を実装
  alert('命式を保存しました');
}}
```
- **コンポーネント**: `SajuDetailPage`
- **現状**: `alert()` による仮実装
- **影響**: ユーザーが命式を保存できない

#### 推奨対応
1. `POST /api/saju/save` を呼び出す関数を実装
2. ゲストモード時はLocalStorageに保存
3. ログインモード時はAPIに送信
4. ローディング状態とエラーハンドリング追加
5. Snackbar等でフィードバック表示

#### ステータス
- [ ] 未着手
- **予想工数**: 1-2時間
- **ブロッカー**: なし（API既存）

---

### 5. フロントエンド：認証状態の取得

**影響度**: 🟡 **MEDIUM**

#### 該当箇所

##### frontend/src/pages/SettingsPage/index.tsx:15
```tsx
// TODO: 認証実装後に useAuth() などから取得
const [isLoggedIn] = useState(false);
const [userEmail] = useState('test@goldensaju.local');
```
- **コンポーネント**: `SettingsPage`
- **現状**: ハードコードされた仮データ
- **影響**: 設定ページが正しく動作しない

#### 推奨対応
1. `useAuth()` Context/Hook実装
2. JWTトークンをLocalStorageから取得
3. トークン検証（有効期限チェック）
4. ユーザー情報API（`GET /api/users/me`）から取得

#### ステータス
- [ ] Phase 3（認証実装時）に対応予定
- **予想工数**: 1-2時間
- **ブロッカー**: 認証機能の実装完了待ち

---

### 6. フロントエンド：命式入力フォームの実装

**影響度**: 🟡 **MEDIUM**

#### 該当箇所

##### frontend/src/pages/HomePage.tsx:20
```tsx
{/* TODO: 命式入力フォームを実装 */}
<Box sx={{ p: 4, backgroundColor: 'white', ... }}>
  ...
</Box>
```
- **コンポーネント**: `HomePage`（トップページ）
- **現状**: プレースホルダーのみ
- **影響**: アプリの核心機能が未実装

#### 推奨対応
1. MUI DatePicker + TimePicker 使用
2. 名前・性別入力フォーム
3. バリデーション（1900-2109年範囲チェック）
4. `POST /api/saju/calculate` 呼び出し
5. 計算結果を `SajuDetailPage` に表示

#### ステータス
- [ ] Phase 1 で最優先実装予定
- **予想工数**: 3-4時間
- **ブロッカー**: なし（API既存）

---

### 7. バックエンド：十神計算ロジックの実装

**影響度**: 🟢 **LOW** （ドンサゴン分析法では十神を使わないため）

#### 該当箇所

##### backend/app/services/fortune_service.py:317
```python
# TODO: 正確な十神計算ロジックを実装
```
- **関数**: 未特定（コンテキストから推測）
- **現状**: おそらく未実装または簡易実装
- **影響**: ドンサゴン分析法では十神論を使用しないため影響小

#### 推奨対応
**対応不要または低優先**
- プロジェクトの基本理念（ドンサゴン分析法）では十神論を使用しない
- 将来的な機能拡張として保留
- コメントを削除または `WONTFIX` に変更検討

#### ステータス
- [ ] 対応保留（WONTFIX候補）
- **予想工数**: N/A
- **ブロッカー**: 要件定義の再確認

---

## 🟢 優先度：低（テスト・検証）

### 8. テストケース：実際の命式データでの検証

**影響度**: 🟢 **LOW**

#### 該当箇所

##### backend/tests/test_fortune_analyzer.py:159
```python
def test_scenario_test_taro(self, analyzer):
    """テスト太郎（1990年1月15日14:30）のテスト"""
    # TODO: 実際の命式データで検証
    pass
```

##### backend/tests/test_fortune_analyzer.py:165
```python
def test_scenario_test_hanako(self, analyzer):
    """テスト花子（1995年6月20日10:15）のテスト"""
    # TODO: 実際の命式データで検証
    pass
```
- **ファイル**: `test_fortune_analyzer.py`
- **現状**: `pass` のみの空テスト
- **影響**: テストカバレッジ不足

#### 推奨対応
1. `POST /api/saju/calculate` でテストユーザーの命式を計算
2. 期待値を手動計算または既存システムで検証
3. アサーション追加（四柱、大運、吉凶レベル等）
4. エッジケース追加（節気境界、うるう年等）

#### ステータス
- [ ] Phase 2-3 で対応予定
- **予想工数**: 2-3時間
- **ブロッカー**: ドンサゴンマトリックス統合完了後

---

## 📈 カテゴリ別分類

### 機能追加（6件）
1. ドンサゴンマトリックス統合 ×2箇所
2. 大運計算情報のDB保存
3. フロントエンド保存処理
4. 命式入力フォーム
5. 十神計算ロジック（低優先）

### バグ修正（0件）
なし

### リファクタリング（2件）
1. 認証実装後のユーザーフィルタリング
2. 認証状態の取得（仮データ → Context）

### テスト・検証（2件）
1. テスト太郎の検証
2. テスト花子の検証

---

## 🎯 推奨対応順序（優先度順）

### Phase 1（即時対応）
1. **命式入力フォームの実装**（frontend/HomePage.tsx）
   - アプリの核心機能
   - 工数: 3-4時間

2. **ドンサゴンマトリックス統合**（backend/services/）
   - 命式分析の精度向上
   - 工数: 3-5時間

3. **大運計算情報のDB保存**（backend/api/saju.py, models）
   - データ正確性の担保
   - 工数: 2-3時間

### Phase 2（機能拡張）
4. **フロントエンド保存処理の実装**（frontend/SajuDetailPage）
   - UX改善
   - 工数: 1-2時間

5. **テストケース実装**（backend/tests/）
   - 品質保証
   - 工数: 2-3時間

### Phase 3（認証実装後）
6. **認証状態の取得**（frontend/SettingsPage, AuthContext）
   - 認証機能依存
   - 工数: 1-2時間

7. **ユーザーフィルタリング**（backend/api/saju.py）
   - 認証機能依存
   - 工数: 0.5時間

### 保留・WONTFIX
8. **十神計算ロジック**（要件定義の再確認後判断）

---

## 🧹 クリーンアップ推奨

### 削除候補コメント
なし（全てのTODOは有効な技術的負債）

### 追加推奨コメント
以下の箇所に実装完了の目安時期をコメント追加推奨:

```python
# TODO (Phase 1): ドンサゴンマトリックス統合
# TODO (Phase 3): 認証実装後に current_user.id でフィルタリング
```

---

## 📝 備考

- **dist/build ディレクトリは除外済み**: トランスパイル済みコードのコメントは含まれていません
- **総工数見積もり**: 13-22時間（Phase 1-2のみ）
- **最優先課題**: ドンサゴンマトリックス統合（命式分析の核心ロジック）

---

**次のアクション**:
1. このレポートを `docs/SCOPE_PROGRESS.md` と統合
2. Phase 1タスクをIssue化
3. ドンサゴンマトリックスパーサーの実装開始

