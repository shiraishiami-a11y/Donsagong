# CHAIN-003: インタラクティブ運勢選択 - E2Eテスト仕様書

## テスト概要

| 項目 | 内容 |
|-----|------|
| 連鎖テストID | CHAIN-003 |
| スライス名 | インタラクティブ運勢選択 |
| ユーザーストーリー | 大運クリックで年運表示、年クリックで月運表示、月クリックで日運表示 |
| エンドポイント連鎖 | 3.2 → 3.3 → 3.4 → 3.5 |
| 外部依存 | 吉凶判定ロジック、ドンサゴン分析エンジン |
| 実装優先度 | 高 |
| 対応ページ | P-003（命式詳細・グラフページ） |
| テストツール | Playwright |
| 作成日 | 2025年11月2日 |
| バージョン | 1.0 |

## エンドポイント連鎖詳細

| ステップ | エンドポイント | HTTPメソッド | 説明 |
|---------|--------------|-------------|------|
| 1 | `/api/saju/{id}/daeun` | GET | 大運リスト取得 |
| 2 | `/api/saju/{id}/year/{daeun_start_age}` | GET | 年運リスト取得（大運クリック時） |
| 3 | `/api/saju/{id}/month/{year}` | GET | 月運リスト取得（年運クリック時） |
| 4 | `/api/saju/{id}/day/{year}/{month}` | GET | 日運リスト取得（月運クリック時） |

## 前提条件

- 命式が既に計算・保存されている
- 命式詳細ページ (`/detail/:id`) にアクセス済み
- 大運リストが表示されている

## テストシナリオ

### シナリオ1: 正常系 - 大運クリックで年運表示

**目的**: 大運をクリックすると、その大運期間の年運が表示されることを確認

#### ステップ

1. 命式詳細ページにアクセス
2. 大運リスト表示確認
3. 特定の大運（例: 18-27歳）をクリック
4. 年運リストが表示されることを確認（10年分）
5. 年運の各カードに年齢・干支・吉凶レベルが表示されることを確認

#### 期待結果

**エンドポイント: GET /api/saju/{id}/year/{daeun_start_age}**
- HTTPステータス: `200 OK`
- レスポンス型: `YearFortuneListResponse`
- `daeunStartAge`: 18
- `daeunEndAge`: 27
- `years`: 配列長さ10個（18歳〜27歳）
- 各年運に以下が含まれる:
  - `year`: 西暦年
  - `age`: 年齢
  - `yearStem`: 年天干
  - `yearBranch`: 年地支
  - `fortuneLevel`: 吉凶レベル
  - `isCurrent`: 現在の年かどうか

**UI検証**:
- ✅ 年運スクロールコンテナが表示される
- ✅ 10個の年運カードが表示される
- ✅ 各カードに年齢・干支・吉凶アイコンが表示される
- ✅ 現在の年がハイライト表示される（`isCurrent: true`）
- ✅ 五行カラーが正しく適用される

#### Playwrightテストコード例

```typescript
import { test, expect } from '@playwright/test';

test('CHAIN-003-S1: 正常系 - 大運クリックで年運表示', async ({ page }) => {
  const sajuId = 'saju-1730505600000';

  await page.goto(`/detail/${sajuId}`);

  // 大運リスト表示確認
  await expect(page.locator('[data-testid="daeun-scroll-container"]')).toBeVisible();

  // 2番目の大運（18-27歳）をクリック
  await page.click('[data-testid="daeun-card-18"]');

  // 年運API呼び出し確認
  const yearResponse = await page.waitForResponse(res =>
    res.url().includes(`/api/saju/${sajuId}/year/18`) && res.status() === 200
  );
  const yearData = await yearResponse.json();

  // レスポンス検証
  expect(yearData.daeunStartAge).toBe(18);
  expect(yearData.daeunEndAge).toBe(27);
  expect(yearData.years).toHaveLength(10);

  // UI検証
  await expect(page.locator('[data-testid="year-scroll-container"]')).toBeVisible();
  const yearCards = page.locator('[data-testid="year-card"]');
  await expect(yearCards).toHaveCount(10);

  // 各カードに干支が表示されることを確認
  const firstYearCard = yearCards.first();
  await expect(firstYearCard.locator('[data-testid="year-stem"]')).toBeVisible();
  await expect(firstYearCard.locator('[data-testid="year-branch"]')).toBeVisible();
  await expect(firstYearCard.locator('[data-testid="fortune-icon"]')).toBeVisible();
});
```

---

### シナリオ2: 正常系 - 年運クリックで月運表示

**目的**: 年運をクリックすると、その年の月運が表示されることを確認

#### ステップ

1. 大運をクリックして年運表示（シナリオ1継続）
2. 特定の年運（例: 2025年）をクリック
3. 月運リストが表示されることを確認（12ヶ月分）
4. 月運の各カードに月・干支・吉凶レベルが表示されることを確認

#### 期待結果

**エンドポイント: GET /api/saju/{id}/month/{year}**
- HTTPステータス: `200 OK`
- レスポンス型: `MonthFortuneListResponse`
- `year`: 2025
- `months`: 配列長さ12個（1月〜12月）
- 各月運に以下が含まれる:
  - `month`: 月（1-12）
  - `monthStem`: 月天干
  - `monthBranch`: 月地支
  - `fortuneLevel`: 吉凶レベル
  - `isCurrent`: 現在の月かどうか

**UI検証**:
- ✅ 月運スクロールコンテナが表示される
- ✅ 12個の月運カードが表示される
- ✅ 各カードに月名・干支・吉凶アイコンが表示される
- ✅ 現在の月がハイライト表示される

#### Playwrightテストコード例

```typescript
test('CHAIN-003-S2: 正常系 - 年運クリックで月運表示', async ({ page }) => {
  const sajuId = 'saju-1730505600000';
  const targetYear = 2025;

  await page.goto(`/detail/${sajuId}`);

  // 大運クリック（前提）
  await page.click('[data-testid="daeun-card-18"]');
  await page.waitForResponse(res =>
    res.url().includes(`/api/saju/${sajuId}/year/18`) && res.status() === 200
  );

  // 年運クリック
  await page.click(`[data-testid="year-card-${targetYear}"]`);

  // 月運API呼び出し確認
  const monthResponse = await page.waitForResponse(res =>
    res.url().includes(`/api/saju/${sajuId}/month/${targetYear}`) && res.status() === 200
  );
  const monthData = await monthResponse.json();

  // レスポンス検証
  expect(monthData.year).toBe(targetYear);
  expect(monthData.months).toHaveLength(12);

  // UI検証
  await expect(page.locator('[data-testid="month-scroll-container"]')).toBeVisible();
  const monthCards = page.locator('[data-testid="month-card"]');
  await expect(monthCards).toHaveCount(12);

  // 各カードに干支が表示されることを確認
  const firstMonthCard = monthCards.first();
  await expect(firstMonthCard.locator('[data-testid="month-stem"]')).toBeVisible();
  await expect(firstMonthCard.locator('[data-testid="month-branch"]')).toBeVisible();
});
```

---

### シナリオ3: 正常系 - 月運クリックで日運表示

**目的**: 月運をクリックすると、その月の日運が表示されることを確認

#### ステップ

1. 年運クリックして月運表示（シナリオ2継続）
2. 特定の月運（例: 11月）をクリック
3. 日運リストが表示されることを確認（その月の日数分: 28〜31日）
4. 日運の各カードに日・干支・吉凶レベルが表示されることを確認

#### 期待結果

**エンドポイント: GET /api/saju/{id}/day/{year}/{month}**
- HTTPステータス: `200 OK`
- レスポンス型: `DayFortuneListResponse`
- `year`: 2025
- `month`: 11
- `days`: 配列長さ30個（11月は30日）
- 各日運に以下が含まれる:
  - `day`: 日（1-31）
  - `dayStem`: 日天干
  - `dayBranch`: 日地支
  - `fortuneLevel`: 吉凶レベル
  - `isToday`: 今日かどうか

**UI検証**:
- ✅ 日運スクロールコンテナが表示される
- ✅ 30個の日運カードが表示される
- ✅ 各カードに日付・干支・吉凶アイコンが表示される
- ✅ 今日がハイライト表示される（`isToday: true`）

#### Playwrightテストコード例

```typescript
test('CHAIN-003-S3: 正常系 - 月運クリックで日運表示', async ({ page }) => {
  const sajuId = 'saju-1730505600000';
  const targetYear = 2025;
  const targetMonth = 11;

  await page.goto(`/detail/${sajuId}`);

  // 大運→年運→月運クリック（前提）
  await page.click('[data-testid="daeun-card-18"]');
  await page.waitForResponse(res => res.url().includes('/year/18') && res.status() === 200);

  await page.click(`[data-testid="year-card-${targetYear}"]`);
  await page.waitForResponse(res => res.url().includes(`/month/${targetYear}`) && res.status() === 200);

  // 月運クリック
  await page.click(`[data-testid="month-card-${targetMonth}"]`);

  // 日運API呼び出し確認
  const dayResponse = await page.waitForResponse(res =>
    res.url().includes(`/api/saju/${sajuId}/day/${targetYear}/${targetMonth}`) && res.status() === 200
  );
  const dayData = await dayResponse.json();

  // レスポンス検証
  expect(dayData.year).toBe(targetYear);
  expect(dayData.month).toBe(targetMonth);
  expect(dayData.days.length).toBe(30); // 11月は30日

  // UI検証
  await expect(page.locator('[data-testid="day-scroll-container"]')).toBeVisible();
  const dayCards = page.locator('[data-testid="day-card"]');
  await expect(dayCards).toHaveCount(30);

  // 今日の日運がハイライトされることを確認（今日が11月の場合）
  const today = new Date();
  if (today.getFullYear() === targetYear && today.getMonth() + 1 === targetMonth) {
    const todayCard = page.locator(`[data-testid="day-card-${today.getDate()}"]`);
    await expect(todayCard).toHaveCSS('background-color', /rgba?\(212, 175, 55/); // ゴールド
  }
});
```

---

### シナリオ4: UI/UX - 連続クリックでスムーズに階層移動

**目的**: 大運→年運→月運→日運と連続してクリックした際にスムーズに表示されることを確認

#### ステップ

1. 命式詳細ページにアクセス
2. 大運クリック → 年運表示
3. 即座に年運クリック → 月運表示
4. 即座に月運クリック → 日運表示
5. 各遷移が1秒以内に完了することを確認

#### 期待結果

- ✅ 各API呼び出しが500ms以内に応答
- ✅ UIトランジションがスムーズ（フェードイン/スライドイン）
- ✅ 連続クリックでもエラーが発生しない

---

### シナリオ5: 異常系 - 範囲外の年・月・日でアクセス

**目的**: 存在しない年・月・日でAPIを呼び出した場合のエラーハンドリング確認

#### ステップ

1. APIを直接呼び出し（例: `/api/saju/{id}/day/2099/99`）

#### 期待結果

- HTTPステータス: `400 Bad Request`
- エラーメッセージ: "無効な月です（1-12の範囲で指定してください）"

#### Playwrightテストコード例

```typescript
test('CHAIN-003-S5: 異常系 - 範囲外の月', async ({ page }) => {
  const sajuId = 'saju-1730505600000';

  // 直接APIを呼び出し
  const response = await page.request.get(`/api/saju/${sajuId}/day/2025/99`);

  expect(response.status()).toBe(400);
  const errorData = await response.json();
  expect(errorData.error).toContain('無効な月');
});
```

---

## パフォーマンス要件

| 指標 | 閾値 | 理想値 |
|------|-----|-------|
| 年運取得API応答時間 | 500ms以内 | 300ms以内 |
| 月運取得API応答時間 | 500ms以内 | 300ms以内 |
| 日運取得API応答時間 | 1秒以内 | 500ms以内 |
| クリック後の表示遅延 | 200ms以内 | 100ms以内 |

---

## 品質ゲート

CHAIN-003テストがすべて成功するための条件:

- ✅ エンドポイント連鎖（3.2 → 3.3 → 3.4 → 3.5）がすべて成功
- ✅ 大運→年運→月運→日運の階層移動が正常に動作
- ✅ 各運勢カードに干支・吉凶レベルが正しく表示される
- ✅ 現在の運勢がハイライト表示される
- ✅ 連続クリックでもエラーが発生しない
- ✅ パフォーマンス要件を満たす

---

**作成日**: 2025年11月2日
**バージョン**: 1.0
**テストツール**: Playwright
**ステータス**: 未実装
**対応API仕様書**: `docs/api-specs/saju-fortune-api.md`
