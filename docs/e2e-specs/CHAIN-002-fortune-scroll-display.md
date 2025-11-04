# CHAIN-002: 水平スクロール運勢表示 - E2Eテスト仕様書

## テスト概要

| 項目 | 内容 |
|-----|------|
| 連鎖テストID | CHAIN-002 |
| スライス名 | 水平スクロール運勢表示 |
| ユーザーストーリー | 命式詳細ページで大運→年運→月運→日運を水平スクロールで階層的に表示する |
| エンドポイント連鎖 | 1.1 → 3.1 → 3.2 → 3.3 → 3.4 → 3.5 |
| 外部依存 | lunar-python, 天干・地支マトリックス, ドンサゴン分析エンジン |
| 実装優先度 | 最高 |
| 対応ページ | P-003（命式詳細・グラフページ） |
| テストツール | Playwright |
| 作成日 | 2025年11月2日 |
| バージョン | 1.0 |

## エンドポイント連鎖詳細

| ステップ | エンドポイント | HTTPメソッド | 説明 |
|---------|--------------|-------------|------|
| 1 | `/api/saju/calculate` | POST | 命式計算 |
| 2 | `/api/saju/{id}` | GET | 命式詳細取得 |
| 3 | `/api/saju/{id}/daeun` | GET | 大運リスト取得 |
| 4 | `/api/saju/{id}/year/{daeun_start_age}` | GET | 年運リスト取得（大運期間の10年分） |
| 5 | `/api/saju/{id}/month/{year}` | GET | 月運リスト取得（指定年の12ヶ月） |
| 6 | `/api/saju/{id}/day/{year}/{month}` | GET | 日運リスト取得（指定月の日数分） |

## 前提条件

- 命式が既に計算・保存されている
- 命式ID（`sajuId`）が判明している
- 命式詳細ページ (`/detail/:id`) にアクセス可能

## テストシナリオ

### シナリオ1: 正常系 - 階層的運勢表示（大運→年運→月運→日運）

**目的**: 水平スクロールで4階層の運勢が正しく表示されることを確認

#### ステップ

1. 命式計算（CHAIN-001を実行済み）
2. 命式詳細ページ (`/detail/:id`) にアクセス
3. 大運水平スクロールが表示されることを確認
4. 大運の1つをクリック
5. 年運水平スクロールが表示されることを確認（10年分）
6. 年運の1つをクリック
7. 月運水平スクロールが表示されることを確認（12ヶ月分）
8. 月運の1つをクリック
9. 日運水平スクロールが表示されることを確認（その月の日数分）

#### 期待結果

**ステップ2: GET /api/saju/{id}**
- HTTPステータス: `200 OK`
- レスポンス型: `SajuDetailResponse`
- 四柱データが表示される

**ステップ3: GET /api/saju/{id}/daeun**
- HTTPステータス: `200 OK`
- レスポンス型: `DaeunAnalysisResponse`
- `daeunList` 配列が10個前後
- 各大運に `startAge`, `endAge`, `daeunStem`, `daeunBranch`, `fortuneLevel` が存在

**ステップ5: GET /api/saju/{id}/year/{daeun_start_age}**
- HTTPステータス: `200 OK`
- レスポンス型: `YearFortuneListResponse`
- `years` 配列が10個（大運期間の10年分）
- 各年運に `year`, `age`, `yearStem`, `yearBranch`, `fortuneLevel` が存在

**ステップ7: GET /api/saju/{id}/month/{year}**
- HTTPステータス: `200 OK`
- レスポンス型: `MonthFortuneListResponse`
- `months` 配列が12個（1年の12ヶ月分）
- 各月運に `month`, `monthStem`, `monthBranch`, `fortuneLevel` が存在

**ステップ9: GET /api/saju/{id}/day/{year}/{month}**
- HTTPステータス: `200 OK`
- レスポンス型: `DayFortuneListResponse`
- `days` 配列がその月の日数分（28〜31個）
- 各日運に `day`, `dayStem`, `dayBranch`, `fortuneLevel` が存在

**UI検証**:
- ✅ 大運水平スクロールが表示される
- ✅ 各大運カードに干支・吉凶レベル・年齢範囲が表示される
- ✅ 大運クリック後、年運水平スクロールが表示される
- ✅ 年運クリック後、月運水平スクロールが表示される
- ✅ 月運クリック後、日運水平スクロールが表示される
- ✅ 各運勢カードに五行カラーが適用される
- ✅ 各運勢カードに吉凶アイコンが表示される
- ✅ 現在の大運・年運・月運・日運がハイライト表示される

#### Playwrightテストコード例

```typescript
import { test, expect } from '@playwright/test';

test('CHAIN-002-S1: 正常系 - 階層的運勢表示', async ({ page }) => {
  // 前提: 命式が既に保存されている
  const sajuId = 'saju-1730505600000'; // テストデータのID

  // 1. 命式詳細ページにアクセス
  await page.goto(`/detail/${sajuId}`);

  // 2. 命式詳細API呼び出し確認
  const detailResponse = await page.waitForResponse(res =>
    res.url().includes(`/api/saju/${sajuId}`) && res.status() === 200
  );
  const detailData = await detailResponse.json();
  expect(detailData.id).toBe(sajuId);

  // 3. 大運リストAPI呼び出し確認
  const daeunResponse = await page.waitForResponse(res =>
    res.url().includes(`/api/saju/${sajuId}/daeun`) && res.status() === 200
  );
  const daeunData = await daeunResponse.json();
  expect(daeunData.daeunList).toBeInstanceOf(Array);
  expect(daeunData.daeunList.length).toBeGreaterThan(0);

  // 大運水平スクロール表示確認
  await expect(page.locator('[data-testid="daeun-scroll-container"]')).toBeVisible();
  await expect(page.locator('[data-testid="daeun-card"]').first()).toBeVisible();

  // 4. 大運の1つをクリック
  const firstDaeun = daeunData.daeunList[0];
  await page.click(`[data-testid="daeun-card-${firstDaeun.startAge}"]`);

  // 5. 年運リストAPI呼び出し確認
  const yearResponse = await page.waitForResponse(res =>
    res.url().includes(`/api/saju/${sajuId}/year/${firstDaeun.startAge}`) && res.status() === 200
  );
  const yearData = await yearResponse.json();
  expect(yearData.years).toBeInstanceOf(Array);
  expect(yearData.years.length).toBe(10); // 10年分

  // 年運水平スクロール表示確認
  await expect(page.locator('[data-testid="year-scroll-container"]')).toBeVisible();
  await expect(page.locator('[data-testid="year-card"]').first()).toBeVisible();

  // 6. 年運の1つをクリック
  const firstYear = yearData.years[0];
  await page.click(`[data-testid="year-card-${firstYear.year}"]`);

  // 7. 月運リストAPI呼び出し確認
  const monthResponse = await page.waitForResponse(res =>
    res.url().includes(`/api/saju/${sajuId}/month/${firstYear.year}`) && res.status() === 200
  );
  const monthData = await monthResponse.json();
  expect(monthData.months).toBeInstanceOf(Array);
  expect(monthData.months.length).toBe(12); // 12ヶ月分

  // 月運水平スクロール表示確認
  await expect(page.locator('[data-testid="month-scroll-container"]')).toBeVisible();
  await expect(page.locator('[data-testid="month-card"]').first()).toBeVisible();

  // 8. 月運の1つをクリック
  const firstMonth = monthData.months[0];
  await page.click(`[data-testid="month-card-${firstMonth.month}"]`);

  // 9. 日運リストAPI呼び出し確認
  const dayResponse = await page.waitForResponse(res =>
    res.url().includes(`/api/saju/${sajuId}/day/${firstYear.year}/${firstMonth.month}`) && res.status() === 200
  );
  const dayData = await dayResponse.json();
  expect(dayData.days).toBeInstanceOf(Array);
  expect(dayData.days.length).toBeGreaterThanOrEqual(28); // 28〜31日

  // 日運水平スクロール表示確認
  await expect(page.locator('[data-testid="day-scroll-container"]')).toBeVisible();
  await expect(page.locator('[data-testid="day-card"]').first()).toBeVisible();

  // UI検証: 五行カラー適用
  const firstDayCard = page.locator('[data-testid="day-card"]').first();
  const stemElement = firstDayCard.locator('[data-testid="day-stem"]');
  await expect(stemElement).toHaveCSS('color', /.+/); // 何らかの色が適用されている

  // UI検証: 吉凶アイコン表示
  await expect(firstDayCard.locator('[data-testid="fortune-icon"]')).toBeVisible();
});
```

---

### シナリオ2: 正常系 - 現在の運勢ハイライト表示

**目的**: 現在の大運・年運・月運・日運が自動的にハイライト表示されることを確認

#### ステップ

1. 命式詳細ページにアクセス
2. 大運スクロールで `isCurrent: true` の大運が自動的にスクロールされて表示される
3. 年運スクロールで現在年が自動的にスクロールされて表示される
4. 月運スクロールで現在月が自動的にスクロールされて表示される
5. 日運スクロールで今日が自動的にスクロールされて表示される

#### 期待結果

- ✅ 現在の大運が `isCurrent: true` としてレスポンスに含まれる
- ✅ 現在の大運カードがハイライト表示される（背景色: ゴールド #D4AF37）
- ✅ 現在の年運カードがハイライト表示される
- ✅ 現在の月運カードがハイライト表示される
- ✅ 今日の日運カードがハイライト表示される（`isToday: true`）

#### Playwrightテストコード例

```typescript
test('CHAIN-002-S2: 正常系 - 現在の運勢ハイライト表示', async ({ page }) => {
  const sajuId = 'saju-1730505600000';

  await page.goto(`/detail/${sajuId}`);

  // 大運リスト取得
  const daeunResponse = await page.waitForResponse(res =>
    res.url().includes(`/api/saju/${sajuId}/daeun`) && res.status() === 200
  );
  const daeunData = await daeunResponse.json();

  // 現在の大運を特定
  const currentDaeun = daeunData.daeunList.find(d => d.isCurrent);
  expect(currentDaeun).toBeTruthy();

  // 現在の大運カードがハイライト表示されることを確認
  const currentDaeunCard = page.locator(`[data-testid="daeun-card-${currentDaeun.startAge}"]`);
  await expect(currentDaeunCard).toHaveCSS('background-color', /rgba?\(212, 175, 55/); // #D4AF37

  // 現在の大運をクリック
  await currentDaeunCard.click();

  // 年運リスト取得
  const yearResponse = await page.waitForResponse(res =>
    res.url().includes(`/api/saju/${sajuId}/year/${currentDaeun.startAge}`) && res.status() === 200
  );
  const yearData = await yearResponse.json();

  // 現在の年運を特定
  const currentYear = yearData.years.find(y => y.isCurrent);
  expect(currentYear).toBeTruthy();

  // 現在の年運カードがハイライト表示されることを確認
  const currentYearCard = page.locator(`[data-testid="year-card-${currentYear.year}"]`);
  await expect(currentYearCard).toHaveCSS('background-color', /rgba?\(212, 175, 55/);
});
```

---

### シナリオ3: UI/UX - 水平スクロールのスムーズ動作

**目的**: 水平スクロールが60fpsでスムーズに動作することを確認

#### ステップ

1. 命式詳細ページにアクセス
2. 大運スクロールを左右にドラッグ
3. フレームレートを測定

#### 期待結果

- ✅ フレームレート: 60fps以上
- ✅ スクロールが途切れずにスムーズ
- ✅ オーバースクロール時のバウンス効果（オプション）

---

### シナリオ4: 異常系 - 存在しない命式IDでアクセス

**目的**: 存在しない命式IDでアクセスした場合のエラーハンドリング確認

#### ステップ

1. 存在しない命式ID (`/detail/invalid-id`) にアクセス

#### 期待結果

- HTTPステータス: `404 Not Found`
- エラーメッセージ表示: "命式が見つかりません"
- トップページへのリダイレクトリンク表示

#### Playwrightテストコード例

```typescript
test('CHAIN-002-S4: 異常系 - 存在しない命式ID', async ({ page }) => {
  await page.goto('/detail/invalid-id');

  const response = await page.waitForResponse(res =>
    res.url().includes('/api/saju/invalid-id') && res.status() === 404
  );
  expect(response.status()).toBe(404);

  // エラーメッセージ表示確認
  await expect(page.locator('[data-testid="error-message"]')).toBeVisible();
  await expect(page.locator('[data-testid="error-message"]')).toContainText('命式が見つかりません');

  // トップページへのリンク確認
  await expect(page.locator('[data-testid="back-to-home"]')).toBeVisible();
});
```

---

## パフォーマンス要件

| 指標 | 閾値 | 理想値 |
|------|-----|-------|
| 大運リスト取得API応答時間 | 500ms以内 | 300ms以内 |
| 年運リスト取得API応答時間 | 500ms以内 | 300ms以内 |
| 月運リスト取得API応答時間 | 500ms以内 | 300ms以内 |
| 日運リスト取得API応答時間 | 1秒以内 | 500ms以内 |
| 水平スクロールフレームレート | 60fps | 60fps |

---

## 品質ゲート

CHAIN-002テストがすべて成功するための条件:

- ✅ エンドポイント連鎖（1.1 → 3.1 → 3.2 → 3.3 → 3.4 → 3.5）がすべて成功
- ✅ 階層的運勢表示が正しく動作（大運→年運→月運→日運）
- ✅ 現在の運勢が自動的にハイライト表示される
- ✅ 水平スクロールが60fpsでスムーズに動作
- ✅ 五行カラー・吉凶アイコンが正しく表示される
- ✅ 異常系でエラーハンドリングが正しく動作

---

**作成日**: 2025年11月2日
**バージョン**: 1.0
**テストツール**: Playwright
**ステータス**: 未実装
**対応API仕様書**:
- `docs/api-specs/saju-detail-api.md`
- `docs/api-specs/saju-fortune-api.md`
