# CHAIN-001: 命式計算全体フロー - E2Eテスト仕様書

## テスト概要

| 項目 | 内容 |
|-----|------|
| 連鎖テストID | CHAIN-001 |
| スライス名 | 命式計算全体フロー |
| ユーザーストーリー | ユーザーが生年月日時を入力して正確な命式を確認する |
| エンドポイント連鎖 | 1.1 (`POST /api/saju/calculate`) → 1.2 (`POST /api/saju/save`) |
| 外部依存 | lunar-python, 210年節気DB (`solar_terms_1900_2109_JIEQI_ONLY.json`) |
| 実装優先度 | 最高 |
| 対応ページ | P-001（トップページ・命式記入ページ） |
| テストツール | Playwright |
| 作成日 | 2025年11月2日 |
| バージョン | 1.0 |

## 前提条件

- ゴールデン四柱推命アプリケーション起動済み
  - フロントエンド: `http://localhost:3247`
  - バックエンド: `http://localhost:8432`
- トップページ (`/`) にアクセス可能
- lunar-pythonライブラリが正しくインストール済み
- 210年節気DBファイルが読み込み可能
- PostgreSQL または LocalStorage が使用可能

## テストシナリオ

### シナリオ1: 正常系 - 男性、1990年3月15日14時30分生まれ

**目的**: 標準的な男性データで命式計算・保存が正常に動作することを確認

#### ステップ

1. トップページ (`/`) にアクセス
2. 生年月日入力: 1990年3月15日
3. 時刻入力: 14時30分
4. 性別選択: 男性
5. 名前入力（オプション）: "テスト太郎"
6. 「計算する」ボタンをクリック
7. ローディングアニメーション（golden-peppa）が表示されることを確認
8. 計算結果が表示されることを確認
9. 「保存する」ボタンをクリック
10. 保存成功メッセージが表示されることを確認
11. 命式リストページ (`/list`) にリダイレクトされることを確認

#### 期待結果

**エンドポイント 1.1: POST /api/saju/calculate**

- HTTPステータス: `200 OK`
- レスポンス型: `SajuResponse`
- 検証項目:
  - ✅ `id`: UUID形式の文字列
  - ✅ `name`: "テスト太郎"
  - ✅ `birthDatetime`: "1990-03-15T14:30:00+09:00"
  - ✅ `gender`: "male"
  - ✅ `yearStem`: "庚" (1990年は庚午年)
  - ✅ `yearBranch`: "午"
  - ✅ `monthStem`: "己" (3月は卯月、節入日基準)
  - ✅ `monthBranch`: "卯"
  - ✅ `dayStem`: 正確な干支（210年節気DBで検証）
  - ✅ `dayBranch`: 正確な干支
  - ✅ `hourStem`: 14時30分に対応する正確な干支
  - ✅ `hourBranch`: 14時30分に対応する正確な干支
  - ✅ `daeunNumber`: 7個前後（性別・生年月日に基づく）
  - ✅ `isForward`: `true`（男性 + 陽干[庚] → 順行）
  - ✅ `afterBirthYears`: 数値（生後年数）
  - ✅ `afterBirthMonths`: 0-11の範囲
  - ✅ `afterBirthDays`: 0-30の範囲
  - ✅ `firstDaeunDate`: YYYY-MM-DD形式
  - ✅ `daeunList`: 配列長さ10個前後
    - 各要素が `DaeunInfo` 型に準拠
    - `startAge` < `endAge`
    - `fortuneLevel` が '大吉' | '吉' | '平' | '凶' | '大凶' のいずれか
  - ✅ `fortuneLevel`: '大吉' | '吉' | '平' | '凶' | '大凶' のいずれか
  - ✅ `createdAt`: ISO 8601形式

**エンドポイント 1.2: POST /api/saju/save**

- HTTPステータス: `201 Created`
- レスポンス型: `SaveResponse`
- 検証項目:
  - ✅ `success`: `true`
  - ✅ `id`: 計算時と同じUUID
  - ✅ `message`: "命式を保存しました"

**UI検証**:
- ✅ ローディングアニメーション（golden-peppa）が計算中のみ表示される
- ✅ 計算結果エリアに四柱が表示される
- ✅ 各干支に五行カラーが適用される
  - 庚（金）: #BDBDBD
  - 午（火）: #F44336
  - 己（土）: #FFB300
  - 卯（木）: #4CAF50
- ✅ 吉凶レベルに対応するアイコン・カラーが表示される
- ✅ 保存ボタンをクリック後、成功メッセージが表示される
- ✅ `/list` ページにリダイレクトされる

#### Playwrightテストコード例

```typescript
import { test, expect } from '@playwright/test';

test('CHAIN-001-S1: 正常系 - 男性、1990年3月15日14時30分生まれ', async ({ page }) => {
  // 1. トップページにアクセス
  await page.goto('/');
  await expect(page).toHaveURL('/');

  // 2-5. 入力フォーム入力
  await page.fill('[data-testid="birth-date"]', '1990-03-15');
  await page.fill('[data-testid="birth-time"]', '14:30');
  await page.click('[data-testid="gender-male"]');
  await page.fill('[data-testid="name"]', 'テスト太郎');

  // 6. 計算ボタンクリック
  await page.click('[data-testid="calculate-button"]');

  // 7. ローディングアニメーション確認
  await expect(page.locator('[data-testid="loading-animation"]')).toBeVisible();

  // API呼び出し確認: POST /api/saju/calculate
  const calculateResponse = await page.waitForResponse(res =>
    res.url().includes('/api/saju/calculate') && res.status() === 200
  );
  const sajuData = await calculateResponse.json();

  // レスポンス検証
  expect(sajuData.id).toBeTruthy();
  expect(sajuData.name).toBe('テスト太郎');
  expect(sajuData.birthDatetime).toBe('1990-03-15T14:30:00+09:00');
  expect(sajuData.gender).toBe('male');
  expect(sajuData.yearStem).toBe('庚');
  expect(sajuData.yearBranch).toBe('午');
  expect(sajuData.monthStem).toBe('己');
  expect(sajuData.monthBranch).toBe('卯');
  expect(sajuData.isForward).toBe(true); // 男性 + 陽干(庚) → 順行
  expect(sajuData.daeunList).toBeInstanceOf(Array);
  expect(sajuData.daeunList.length).toBeGreaterThan(0);
  expect(['大吉', '吉', '平', '凶', '大凶']).toContain(sajuData.fortuneLevel);

  // 8. ローディング終了後、計算結果が表示される
  await expect(page.locator('[data-testid="loading-animation"]')).not.toBeVisible();
  await expect(page.locator('[data-testid="saju-result-section"]')).toBeVisible();

  // UI検証: 四柱表示
  await expect(page.locator('[data-testid="year-stem"]')).toContainText('庚');
  await expect(page.locator('[data-testid="year-branch"]')).toContainText('午');

  // 9. 保存ボタンクリック
  await page.click('[data-testid="save-button"]');

  // API呼び出し確認: POST /api/saju/save
  const saveResponse = await page.waitForResponse(res =>
    res.url().includes('/api/saju/save') && res.status() === 201
  );
  const saveData = await saveResponse.json();

  // 保存レスポンス検証
  expect(saveData.success).toBe(true);
  expect(saveData.id).toBe(sajuData.id);
  expect(saveData.message).toBe('命式を保存しました');

  // 10. 保存成功メッセージ確認
  await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
  await expect(page.locator('[data-testid="success-message"]')).toContainText('命式を保存しました');

  // 11. リダイレクト確認
  await expect(page).toHaveURL('/list');
});
```

---

### シナリオ2: 正常系 - 女性、1995年6月20日10時15分生まれ

**目的**: 女性データで大運が順行になることを確認（女性 + 陰干 → 順行）

#### ステップ

1. トップページ (`/`) にアクセス
2. 生年月日入力: 1995年6月20日
3. 時刻入力: 10時15分
4. 性別選択: 女性
5. 名前入力: "テスト花子"
6. 「計算する」ボタンをクリック
7. 計算結果が表示されることを確認
8. 「保存する」ボタンをクリック

#### 期待結果

**エンドポイント 1.1: POST /api/saju/calculate**

- HTTPステータス: `200 OK`
- 検証項目:
  - ✅ `yearStem`: "乙" (1995年は乙亥年)
  - ✅ `yearBranch`: "亥"
  - ✅ `monthStem`: "壬" (6月は午月、節入日基準)
  - ✅ `monthBranch`: "午"
  - ✅ `isForward`: `true`（女性 + 陰干[乙] → 順行）
  - ✅ `daeunList`: 配列長さ10個前後

**エンドポイント 1.2: POST /api/saju/save**

- HTTPステータス: `201 Created`
- `success`: `true`

#### Playwrightテストコード例

```typescript
test('CHAIN-001-S2: 正常系 - 女性、1995年6月20日10時15分生まれ', async ({ page }) => {
  await page.goto('/');

  await page.fill('[data-testid="birth-date"]', '1995-06-20');
  await page.fill('[data-testid="birth-time"]', '10:15');
  await page.click('[data-testid="gender-female"]');
  await page.fill('[data-testid="name"]', 'テスト花子');

  await page.click('[data-testid="calculate-button"]');

  const calculateResponse = await page.waitForResponse(res =>
    res.url().includes('/api/saju/calculate') && res.status() === 200
  );
  const sajuData = await calculateResponse.json();

  expect(sajuData.yearStem).toBe('乙');
  expect(sajuData.yearBranch).toBe('亥');
  expect(sajuData.monthStem).toBe('壬');
  expect(sajuData.monthBranch).toBe('午');
  expect(sajuData.isForward).toBe(true); // 女性 + 陰干(乙) → 順行

  await page.click('[data-testid="save-button"]');

  const saveResponse = await page.waitForResponse(res =>
    res.url().includes('/api/saju/save') && res.status() === 201
  );
  const saveData = await saveResponse.json();

  expect(saveData.success).toBe(true);
  await expect(page).toHaveURL('/list');
});
```

---

### シナリオ3: エッジケース - 範囲最小値（1900年1月1日0時0分）

**目的**: サポート範囲の最小値でも正常に動作することを確認

#### ステップ

1. トップページにアクセス
2. 生年月日入力: 1900年1月1日
3. 時刻入力: 00時00分
4. 性別選択: 男性
5. 名前入力: "エッジケース1"
6. 「計算する」ボタンをクリック

#### 期待結果

- HTTPステータス: `200 OK`
- 四柱が正確に計算される
- エラーが発生しない

#### Playwrightテストコード例

```typescript
test('CHAIN-001-S3: エッジケース - 範囲最小値（1900年1月1日0時0分）', async ({ page }) => {
  await page.goto('/');

  await page.fill('[data-testid="birth-date"]', '1900-01-01');
  await page.fill('[data-testid="birth-time"]', '00:00');
  await page.click('[data-testid="gender-male"]');
  await page.fill('[data-testid="name"]', 'エッジケース1');

  await page.click('[data-testid="calculate-button"]');

  const calculateResponse = await page.waitForResponse(res =>
    res.url().includes('/api/saju/calculate') && res.status() === 200
  );
  const sajuData = await calculateResponse.json();

  expect(sajuData.id).toBeTruthy();
  expect(sajuData.birthDatetime).toBe('1900-01-01T00:00:00+09:00');
  expect(sajuData.yearStem).toBeTruthy(); // 干支が存在する
  expect(sajuData.yearBranch).toBeTruthy();
});
```

---

### シナリオ4: エッジケース - 範囲最大値（2109年12月31日23時59分）

**目的**: サポート範囲の最大値でも正常に動作することを確認

#### ステップ

1. トップページにアクセス
2. 生年月日入力: 2109年12月31日
3. 時刻入力: 23時59分
4. 性別選択: 女性
5. 名前入力: "エッジケース2"
6. 「計算する」ボタンをクリック

#### 期待結果

- HTTPステータス: `200 OK`
- 四柱が正確に計算される
- エラーが発生しない

#### Playwrightテストコード例

```typescript
test('CHAIN-001-S4: エッジケース - 範囲最大値（2109年12月31日23時59分）', async ({ page }) => {
  await page.goto('/');

  await page.fill('[data-testid="birth-date"]', '2109-12-31');
  await page.fill('[data-testid="birth-time"]', '23:59');
  await page.click('[data-testid="gender-female"]');
  await page.fill('[data-testid="name"]', 'エッジケース2');

  await page.click('[data-testid="calculate-button"]');

  const calculateResponse = await page.waitForResponse(res =>
    res.url().includes('/api/saju/calculate') && res.status() === 200
  );
  const sajuData = await calculateResponse.json();

  expect(sajuData.id).toBeTruthy();
  expect(sajuData.birthDatetime).toBe('2109-12-31T23:59:00+09:00');
  expect(sajuData.yearStem).toBeTruthy();
  expect(sajuData.yearBranch).toBeTruthy();
});
```

---

### シナリオ5: 異常系 - 範囲外の日付（1899年12月31日）

**目的**: サポート範囲外の日付でエラーが返されることを確認

#### ステップ

1. トップページにアクセス
2. 生年月日入力: 1899年12月31日
3. 時刻入力: 12時00分
4. 性別選択: 男性
5. 「計算する」ボタンをクリック

#### 期待結果

- **クライアント側バリデーション**:
  - エラーメッセージ表示: "1900-2109年の範囲内で入力してください"
  - API呼び出しは行われない

**または（サーバー側バリデーション）**:
- HTTPステータス: `400 Bad Request`
- エラーメッセージ: "対応範囲外の日付です（1900-2109年のみ）"

#### Playwrightテストコード例

```typescript
test('CHAIN-001-S5: 異常系 - 範囲外の日付（1899年12月31日）', async ({ page }) => {
  await page.goto('/');

  await page.fill('[data-testid="birth-date"]', '1899-12-31');
  await page.fill('[data-testid="birth-time"]', '12:00');
  await page.click('[data-testid="gender-male"]');

  await page.click('[data-testid="calculate-button"]');

  // クライアント側バリデーションチェック
  await expect(page.locator('[data-testid="error-message"]')).toBeVisible();
  await expect(page.locator('[data-testid="error-message"]')).toContainText('1900-2109年の範囲内で入力してください');

  // API呼び出しが行われないことを確認
  // （タイムアウトするはずなので、try-catchで処理）
  let apiCalled = false;
  try {
    await page.waitForResponse(res => res.url().includes('/api/saju/calculate'), { timeout: 2000 });
    apiCalled = true;
  } catch (e) {
    apiCalled = false;
  }
  expect(apiCalled).toBe(false);
});
```

---

### シナリオ6: 異常系 - 範囲外の日付（2110年1月1日）

**目的**: サポート範囲外の最大値超過でエラーが返されることを確認

#### ステップ

1. トップページにアクセス
2. 生年月日入力: 2110年1月1日
3. 時刻入力: 00時00分
4. 性別選択: 女性
5. 「計算する」ボタンをクリック

#### 期待結果

- エラーメッセージ表示: "1900-2109年の範囲内で入力してください"
- または HTTPステータス: `400 Bad Request`

#### Playwrightテストコード例

```typescript
test('CHAIN-001-S6: 異常系 - 範囲外の日付（2110年1月1日）', async ({ page }) => {
  await page.goto('/');

  await page.fill('[data-testid="birth-date"]', '2110-01-01');
  await page.fill('[data-testid="birth-time"]', '00:00');
  await page.click('[data-testid="gender-female"]');

  await page.click('[data-testid="calculate-button"]');

  await expect(page.locator('[data-testid="error-message"]')).toBeVisible();
  await expect(page.locator('[data-testid="error-message"]')).toContainText('1900-2109年の範囲内で入力してください');
});
```

---

### シナリオ7: 異常系 - 未入力フィールド（生年月日なし）

**目的**: 必須フィールド未入力でエラーが返されることを確認

#### ステップ

1. トップページにアクセス
2. 生年月日入力: （空欄）
3. 時刻入力: 14時30分
4. 性別選択: 男性
5. 「計算する」ボタンをクリック

#### 期待結果

- クライアント側バリデーション:
  - エラーメッセージ表示: "生年月日を入力してください"
  - 計算ボタンが無効化される、または API呼び出しが行われない

#### Playwrightテストコード例

```typescript
test('CHAIN-001-S7: 異常系 - 未入力フィールド（生年月日なし）', async ({ page }) => {
  await page.goto('/');

  // 生年月日は空欄のまま
  await page.fill('[data-testid="birth-time"]', '14:30');
  await page.click('[data-testid="gender-male"]');

  await page.click('[data-testid="calculate-button"]');

  await expect(page.locator('[data-testid="error-message"]')).toBeVisible();
  await expect(page.locator('[data-testid="error-message"]')).toContainText('生年月日を入力してください');
});
```

---

### シナリオ8: 異常系 - 未入力フィールド（性別なし）

**目的**: 性別未選択でエラーが返されることを確認

#### ステップ

1. トップページにアクセス
2. 生年月日入力: 1990年3月15日
3. 時刻入力: 14時30分
4. 性別選択: （未選択）
5. 「計算する」ボタンをクリック

#### 期待結果

- エラーメッセージ表示: "性別を選択してください"
- または HTTPステータス: `400 Bad Request`

#### Playwrightテストコード例

```typescript
test('CHAIN-001-S8: 異常系 - 未入力フィールド（性別なし）', async ({ page }) => {
  await page.goto('/');

  await page.fill('[data-testid="birth-date"]', '1990-03-15');
  await page.fill('[data-testid="birth-time"]', '14:30');
  // 性別は未選択

  await page.click('[data-testid="calculate-button"]');

  await expect(page.locator('[data-testid="error-message"]')).toBeVisible();
  await expect(page.locator('[data-testid="error-message"]')).toContainText('性別を選択してください');
});
```

---

### シナリオ9: 異常系 - ネットワークエラー

**目的**: APIエンドポイントが応答しない場合のエラーハンドリングを確認

#### ステップ

1. トップページにアクセス
2. ネットワークをオフラインにする
3. 生年月日入力: 1990年3月15日
4. 時刻入力: 14時30分
5. 性別選択: 男性
6. 「計算する」ボタンをクリック

#### 期待結果

- ローディングアニメーション表示後、エラーメッセージが表示される
- エラーメッセージ: "ネットワークエラーが発生しました"

#### Playwrightテストコード例

```typescript
test('CHAIN-001-S9: 異常系 - ネットワークエラー', async ({ page }) => {
  // ネットワークをオフラインにする
  await page.route('**/api/saju/calculate', route => route.abort('failed'));

  await page.goto('/');

  await page.fill('[data-testid="birth-date"]', '1990-03-15');
  await page.fill('[data-testid="birth-time"]', '14:30');
  await page.click('[data-testid="gender-male"]');

  await page.click('[data-testid="calculate-button"]');

  // ローディングアニメーション確認
  await expect(page.locator('[data-testid="loading-animation"]')).toBeVisible();

  // エラーメッセージ確認
  await expect(page.locator('[data-testid="error-message"]')).toBeVisible();
  await expect(page.locator('[data-testid="error-message"]')).toContainText('ネットワークエラー');
});
```

---

## API検証詳細

### POST /api/saju/calculate

#### リクエスト検証

```typescript
{
  birthDatetime: "1990-03-15T14:30:00+09:00", // ISO 8601形式、KST (UTC+9)
  gender: "male",                             // 'male' または 'female'
  name: "テスト太郎",                          // オプション
  timezoneOffset: 9                           // KST
}
```

**検証項目**:
- ✅ `birthDatetime`: ISO 8601形式、1900-2109年範囲内
- ✅ `gender`: 'male' または 'female'
- ✅ `name`: 文字列（オプション）
- ✅ `timezoneOffset`: 9（KST）

#### レスポンス検証

```typescript
{
  id: string,                  // UUID形式（例: "saju-1730505600000"）
  name: "テスト太郎",
  birthDatetime: "1990-03-15T14:30:00+09:00",
  gender: "male",
  yearStem: "庚",             // 1990年 = 庚午
  yearBranch: "午",
  monthStem: "己",            // 3月 = 卯月（節入日基準）
  monthBranch: "卯",
  dayStem: string,            // 正確な干支
  dayBranch: string,
  hourStem: string,           // 14:30に対応する干支
  hourBranch: string,
  daeunNumber: number,        // 7個前後
  isForward: true,            // 男性 + 陽干(庚) → 順行
  afterBirthYears: number,
  afterBirthMonths: number,   // 0-11
  afterBirthDays: number,     // 0-30
  firstDaeunDate: string,     // YYYY-MM-DD形式
  daeunList: Array<DaeunInfo>,// 配列長さ10個前後
  fortuneLevel: FortuneLevel, // '大吉' | '吉' | '平' | '凶' | '大凶'
  createdAt: string           // ISO 8601形式
}
```

**検証項目**:
- ✅ 全フィールドが存在する
- ✅ 四柱（年月日時）が正確に計算されている
- ✅ 大運数が正確に計算されている
- ✅ 順行/逆行が性別・陰陽干に基づいて正しく判定されている
- ✅ 吉凶レベルが5段階のいずれかである

### POST /api/saju/save

#### リクエスト検証

```typescript
{
  // SajuResponse型の全フィールド
  id: string,
  name: string,
  birthDatetime: string,
  gender: string,
  yearStem: string,
  yearBranch: string,
  // ... 以下省略
}
```

**検証項目**:
- ✅ 計算APIのレスポンスと同じ構造
- ✅ すべての必須フィールドが存在する

#### レスポンス検証

```typescript
{
  success: true,
  id: "saju-1730505600000", // 計算時と同じUUID
  message: "命式を保存しました"
}
```

**検証項目**:
- ✅ `success`: `true`
- ✅ `id`: 計算時と同じUUID
- ✅ `message`: 成功メッセージ

---

## パフォーマンス要件

| 指標 | 閾値 | 理想値 |
|------|-----|-------|
| 計算API応答時間 | 2秒以内 | 1秒以内 |
| 保存API応答時間 | 1秒以内 | 500ms以内 |
| ローディングアニメーション表示時間 | 計算中のみ | 計算中のみ |
| ページ遷移時間 | 500ms以内 | 300ms以内 |

**Playwrightテストコード例**:

```typescript
test('CHAIN-001-P1: パフォーマンス - 計算API応答時間', async ({ page }) => {
  await page.goto('/');

  await page.fill('[data-testid="birth-date"]', '1990-03-15');
  await page.fill('[data-testid="birth-time"]', '14:30');
  await page.click('[data-testid="gender-male"]');

  const startTime = Date.now();
  await page.click('[data-testid="calculate-button"]');

  await page.waitForResponse(res =>
    res.url().includes('/api/saju/calculate') && res.status() === 200
  );

  const endTime = Date.now();
  const responseTime = endTime - startTime;

  // 2秒以内
  expect(responseTime).toBeLessThan(2000);

  // 理想値: 1秒以内
  console.log(`計算API応答時間: ${responseTime}ms`);
});
```

---

## セキュリティ検証

### XSS脆弱性チェック

**目的**: 名前入力フィールドに悪意のあるスクリプトを入力してもXSSが発生しないことを確認

```typescript
test('CHAIN-001-SEC1: セキュリティ - XSS脆弱性チェック', async ({ page }) => {
  await page.goto('/');

  // 悪意のあるスクリプトを入力
  await page.fill('[data-testid="name"]', '<script>alert("XSS")</script>');
  await page.fill('[data-testid="birth-date"]', '1990-03-15');
  await page.fill('[data-testid="birth-time"]', '14:30');
  await page.click('[data-testid="gender-male"]');

  await page.click('[data-testid="calculate-button"]');

  // スクリプトが実行されないことを確認
  const alerts = [];
  page.on('dialog', dialog => {
    alerts.push(dialog.message());
    dialog.dismiss();
  });

  await page.waitForTimeout(1000);
  expect(alerts).toHaveLength(0);

  // 計算結果にスクリプトがエスケープされて表示されることを確認
  await expect(page.locator('[data-testid="saju-name"]')).toContainText('<script>alert("XSS")</script>');
});
```

### SQLインジェクション対策チェック

**目的**: 入力フィールドにSQLインジェクションコードを入力してもデータベースが保護されることを確認

```typescript
test('CHAIN-001-SEC2: セキュリティ - SQLインジェクション対策', async ({ page }) => {
  await page.goto('/');

  // SQLインジェクションを試みる
  await page.fill('[data-testid="name"]', "'; DROP TABLE saju; --");
  await page.fill('[data-testid="birth-date"]', '1990-03-15');
  await page.fill('[data-testid="birth-time"]', '14:30');
  await page.click('[data-testid="gender-male"]');

  await page.click('[data-testid="calculate-button"]');

  const calculateResponse = await page.waitForResponse(res =>
    res.url().includes('/api/saju/calculate') && res.status() === 200
  );

  // 正常に処理されることを確認（SQLインジェクションが実行されない）
  expect(calculateResponse.status()).toBe(200);

  // データベースが破壊されていないことを確認（保存が成功する）
  await page.click('[data-testid="save-button"]');
  const saveResponse = await page.waitForResponse(res =>
    res.url().includes('/api/saju/save') && res.status() === 201
  );
  expect(saveResponse.status()).toBe(201);
});
```

---

## 品質ゲート

CHAIN-001テストがすべて成功するための条件:

- ✅ すべての正常系テストケース（S1〜S4）が100%成功
- ✅ すべての異常系テストケース（S5〜S9）でエラーハンドリング確認
- ✅ パフォーマンス要件を満たす（計算API: 2秒以内、保存API: 1秒以内）
- ✅ セキュリティチェック全項目クリア（XSS、SQLインジェクション）
- ✅ UI検証（ローディングアニメーション、五行カラー、吉凶アイコン）
- ✅ ページ遷移が正常に動作（`/` → `/list`）

---

## 依存関係

### 外部ライブラリ

- **lunar-python**: 四柱推命計算エンジン
  - `EightChar` クラス使用
  - 干支計算、大運計算

### データベース

- **210年節気DB**: `solar_terms_1900_2109_JIEQI_ONLY.json`
  - 1900年〜2109年の節気データ
  - 節入日の正確な計算に使用

- **ドンサゴンマトリックス**: `docs/DONSAGONG_MASTER_DATABASE.md`
  - 天干100マトリックス（10×10）
  - 地支144マトリックス（12×12）
  - 調候用神表

### バックエンドサービス

- PostgreSQL（ログインモード）または LocalStorage（ゲストモード）

---

## トラブルシューティング

### 計算結果が不正確な場合

1. 210年節気DBが正しく読み込まれているか確認
2. lunar-pythonのバージョン確認
3. タイムゾーンが KST (UTC+9) に統一されているか確認
4. 性別パラメータが正しく渡されているか確認

### 保存が失敗する場合

1. PostgreSQL接続確認（ログインモード）
2. LocalStorage容量確認（ゲストモード）
3. JWT トークンの有効性確認（ログインモード）

### パフォーマンスが遅い場合

1. Redisキャッシュが有効になっているか確認
2. データベースクエリの最適化
3. ネットワーク遅延の確認

---

**作成日**: 2025年11月2日
**バージョン**: 1.0
**テストツール**: Playwright
**ステータス**: 未実装
**対応API仕様書**: `docs/api-specs/saju-calculation-api.md`
