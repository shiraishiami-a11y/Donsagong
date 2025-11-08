# CHAIN-006: スマホレスポンシブ対応強化 E2Eテスト仕様書

## 概要

**テストチェーンID**: CHAIN-006
**テーマ**: スマホレスポンシブ対応強化
**優先度**: High
**対象画面**: 全ページ（TopPage, ListPage, SajuDetailPage, LoginPage, RegisterPage, SettingsPage）
**デバイス**: iPhone SE (375px), iPhone 14 Pro (393px), iPad mini (768px)

**目的**:
- 横スクロールが正常に動作すること
- タップ領域が44px以上であること
- フォントサイズが14px以上で読みやすいこと
- レイアウト崩れがないこと
- PC表示に影響がないこと

---

## テスト項目一覧

### 正常系（必須）- 8項目

#### 1. 横スクロール動作確認（Critical）
- **E2E-CHAIN-006-S1**: 横スクロール - 人生グラフ（LifeGraphSection）
- **E2E-CHAIN-006-S2**: 横スクロール - 大運（DaeunScrollSection）
- **E2E-CHAIN-006-S3**: 横スクロール - 年運（YearScrollSection）
- **E2E-CHAIN-006-S4**: 横スクロール - 月運（MonthScrollSection）
- **E2E-CHAIN-006-S5**: 横スクロール - 日運（DayScrollSection）

#### 2. タップ領域確認（Critical）
- **E2E-CHAIN-006-S6**: タップ領域 - ヘッダーボタン（閉じるボタン）
- **E2E-CHAIN-006-S7**: タップ領域 - ListPageアイコンボタン
- **E2E-CHAIN-006-S8**: タップ領域 - 性別選択ボタン

### UI/UX（推奨）- 7項目

#### 3. フォントサイズ確認
- **E2E-CHAIN-006-U1**: フォントサイズ - 四柱の天干地支
- **E2E-CHAIN-006-U2**: フォントサイズ - 大運カードの天干地支
- **E2E-CHAIN-006-U3**: フォントサイズ - エラーメッセージ

#### 4. レイアウト崩れ確認
- **E2E-CHAIN-006-U4**: レイアウト - TopPage（性別ボタン配置）
- **E2E-CHAIN-006-U5**: レイアウト - ListPage（空アイコン表示）
- **E2E-CHAIN-006-U6**: レイアウト - SajuCard（四柱ミニ表示）
- **E2E-CHAIN-006-U7**: レイアウト - LoginPage（パスワード忘れたリンク）

### パフォーマンス - 2項目

#### 5. スクロール性能確認
- **E2E-CHAIN-006-P1**: スクロール速度 - 大運カード（10個）のスクロール所要時間
- **E2E-CHAIN-006-P2**: スクロール速度 - 月運カード（12個）のスクロール所要時間

### クロスデバイス - 3項目

#### 6. デバイス別表示確認
- **E2E-CHAIN-006-D1**: デバイス別 - iPhone SE (375px)
- **E2E-CHAIN-006-D2**: デバイス別 - iPhone 14 Pro (393px)
- **E2E-CHAIN-006-D3**: デバイス別 - iPad mini (768px)

---

## 詳細テストケース

---

### E2E-CHAIN-006-S1: 横スクロール - 人生グラフ（LifeGraphSection）

**目的**: 人生グラフが横にスクロールできることを確認

**前提条件**:
- 命式データが1件保存済み（テスト太郎、1990年3月15日14:30、男性）
- ビューポート: iPhone SE (375px)

**テスト手順**:
1. TopPageで命式を計算
2. SajuDetailPageに遷移
3. LifeGraphSectionを確認
4. グラフを左から右にスクロール
5. スクロール可能であることを確認

**期待結果**:
- ✅ グラフ幅が800pxで表示される
- ✅ 画面幅375pxでもグラフがはみ出さずにスクロール可能
- ✅ スクロールが滑らかに動作する（-webkit-overflow-scrolling: touch）
- ✅ グラフが途切れずに全体が表示される

**Playwright実装例**:
```typescript
test('E2E-CHAIN-006-S1: 横スクロール - 人生グラフ', async ({ page }) => {
  // ビューポート設定（iPhone SE）
  await page.setViewportSize({ width: 375, height: 667 });

  // 命式計算
  await page.goto('http://localhost:3247');
  await page.fill('input[name="name"]', 'テスト太郎');
  await page.fill('input[name="birthDate"]', '1990-03-15');
  await page.fill('input[name="birthTime"]', '14:30');
  await page.click('button:has-text("男性")');
  await page.click('button:has-text("計算する")');

  // SajuDetailPageに遷移
  await page.waitForURL('**/detail/**');

  // LifeGraphSectionを確認
  const graphSection = page.locator('[data-testid="life-graph-section"]');
  await expect(graphSection).toBeVisible();

  // グラフコンテナの幅を確認（800px）
  const graphContainer = graphSection.locator('.recharts-wrapper');
  const width = await graphContainer.evaluate(el => el.clientWidth);
  expect(width).toBe(800);

  // スクロール可能性を確認
  const scrollContainer = graphSection.locator('> div').first();
  const isScrollable = await scrollContainer.evaluate(el => {
    return el.scrollWidth > el.clientWidth;
  });
  expect(isScrollable).toBeTruthy();

  // スクロール実行
  await scrollContainer.evaluate(el => {
    el.scrollLeft = 200;
  });

  // スクロール位置確認
  const scrollLeft = await scrollContainer.evaluate(el => el.scrollLeft);
  expect(scrollLeft).toBeGreaterThan(0);
});
```

---

### E2E-CHAIN-006-S2: 横スクロール - 大運（DaeunScrollSection）

**目的**: 大運カードが横にスクロールできることを確認

**前提条件**:
- 命式データが1件保存済み（テスト太郎、1990年3月15日14:30、男性）
- ビューポート: iPhone SE (375px)

**テスト手順**:
1. TopPageで命式を計算
2. SajuDetailPageに遷移
3. DaeunScrollSectionを確認
4. 大運カードを左から右にスクロール
5. スクロール可能であることを確認

**期待結果**:
- ✅ 大運カード9個が横に並ぶ
- ✅ カード最小幅が120pxで表示される
- ✅ スクロールが滑らかに動作する
- ✅ 現在の大運がハイライト表示される

**Playwright実装例**:
```typescript
test('E2E-CHAIN-006-S2: 横スクロール - 大運', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });

  // 命式計算・遷移（省略）

  // DaeunScrollSectionを確認
  const daeunSection = page.locator('[data-testid="daeun-scroll-section"]');
  await expect(daeunSection).toBeVisible();

  // 大運カードの数を確認
  const daeunCards = daeunSection.locator('[data-testid^="daeun-card-"]');
  await expect(daeunCards).toHaveCount(9);

  // カード最小幅を確認（120px）
  const firstCard = daeunCards.first();
  const cardWidth = await firstCard.evaluate(el => el.clientWidth);
  expect(cardWidth).toBeGreaterThanOrEqual(120);

  // スクロール実行
  const scrollContainer = daeunSection.locator('> div').first();
  await scrollContainer.evaluate(el => {
    el.scrollLeft = 300;
  });

  // スクロール位置確認
  const scrollLeft = await scrollContainer.evaluate(el => el.scrollLeft);
  expect(scrollLeft).toBeGreaterThan(0);
});
```

---

### E2E-CHAIN-006-S3: 横スクロール - 年運（YearScrollSection）

**目的**: 年運カードが横にスクロールできることを確認

**前提条件**:
- 命式データが1件保存済み（テスト太郎、1990年3月15日14:30、男性）
- 大運を選択済み（例: 18-27歳）
- ビューポート: iPhone SE (375px)

**テスト手順**:
1. TopPageで命式を計算
2. SajuDetailPageに遷移
3. 大運カードをクリック（18-27歳）
4. YearScrollSectionを確認
5. 年運カードを左から右にスクロール
6. スクロール可能であることを確認

**期待結果**:
- ✅ 年運カード10個が横に並ぶ
- ✅ スクロールが滑らかに動作する（-webkit-overflow-scrolling: touch）
- ✅ 現在の年運がハイライト表示される

**Playwright実装例**:
```typescript
test('E2E-CHAIN-006-S3: 横スクロール - 年運', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });

  // 命式計算・遷移（省略）

  // 大運をクリック
  await page.click('[data-testid="daeun-card-18"]');

  // YearScrollSectionを確認
  const yearSection = page.locator('[data-testid="year-scroll-section"]');
  await expect(yearSection).toBeVisible();

  // 年運カードの数を確認
  const yearCards = yearSection.locator('[data-testid^="year-card-"]');
  await expect(yearCards).toHaveCount(10);

  // スクロール実行
  const scrollContainer = yearSection.locator('> div').first();
  await scrollContainer.evaluate(el => {
    el.scrollLeft = 200;
  });

  // スクロール位置確認
  const scrollLeft = await scrollContainer.evaluate(el => el.scrollLeft);
  expect(scrollLeft).toBeGreaterThan(0);
});
```

---

### E2E-CHAIN-006-S4: 横スクロール - 月運（MonthScrollSection）

**目的**: 月運カードが横にスクロールできることを確認

**前提条件**:
- 命式データが1件保存済み（テスト太郎、1990年3月15日14:30、男性）
- 大運・年運を選択済み
- ビューポート: iPhone SE (375px)

**テスト手順**:
1. TopPageで命式を計算
2. SajuDetailPageに遷移
3. 大運カードをクリック（18-27歳）
4. 年運カードをクリック（2025年）
5. MonthScrollSectionを確認
6. 月運カードを左から右にスクロール
7. スクロール可能であることを確認

**期待結果**:
- ✅ 月運カード12個が横に並ぶ
- ✅ スクロールが滑らかに動作する（-webkit-overflow-scrolling: touch）
- ✅ 現在の月運がハイライト表示される

**Playwright実装例**:
```typescript
test('E2E-CHAIN-006-S4: 横スクロール - 月運', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });

  // 命式計算・遷移・大運選択・年運選択（省略）

  // MonthScrollSectionを確認
  const monthSection = page.locator('[data-testid="month-scroll-section"]');
  await expect(monthSection).toBeVisible();

  // 月運カードの数を確認
  const monthCards = monthSection.locator('[data-testid^="month-card-"]');
  await expect(monthCards).toHaveCount(12);

  // スクロール実行
  const scrollContainer = monthSection.locator('> div').first();
  await scrollContainer.evaluate(el => {
    el.scrollLeft = 200;
  });

  // スクロール位置確認
  const scrollLeft = await scrollContainer.evaluate(el => el.scrollLeft);
  expect(scrollLeft).toBeGreaterThan(0);
});
```

---

### E2E-CHAIN-006-S5: 横スクロール - 日運（DayScrollSection）

**目的**: 日運カードが横にスクロールできることを確認

**前提条件**:
- 命式データが1件保存済み（テスト太郎、1990年3月15日14:30、男性）
- 大運・年運・月運を選択済み
- ビューポート: iPhone SE (375px)

**テスト手順**:
1. TopPageで命式を計算
2. SajuDetailPageに遷移
3. 大運カードをクリック（18-27歳）
4. 年運カードをクリック（2025年）
5. 月運カードをクリック（11月）
6. DayScrollSectionを確認
7. 日運カードを左から右にスクロール
8. スクロール可能であることを確認

**期待結果**:
- ✅ 日運カード30個が横に並ぶ
- ✅ スクロールが滑らかに動作する（-webkit-overflow-scrolling: touch）
- ✅ 今日の日運がハイライト表示される

**Playwright実装例**:
```typescript
test('E2E-CHAIN-006-S5: 横スクロール - 日運', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });

  // 命式計算・遷移・大運選択・年運選択・月運選択（省略）

  // DayScrollSectionを確認
  const daySection = page.locator('[data-testid="day-scroll-section"]');
  await expect(daySection).toBeVisible();

  // 日運カードの数を確認
  const dayCards = daySection.locator('[data-testid^="day-card-"]');
  await expect(dayCards).toHaveCount(30);

  // スクロール実行
  const scrollContainer = daySection.locator('> div').first();
  await scrollContainer.evaluate(el => {
    el.scrollLeft = 300;
  });

  // スクロール位置確認
  const scrollLeft = await scrollContainer.evaluate(el => el.scrollLeft);
  expect(scrollLeft).toBeGreaterThan(0);
});
```

---

### E2E-CHAIN-006-S6: タップ領域 - ヘッダーボタン（閉じるボタン）

**目的**: ヘッダーの閉じるボタンのタップ領域が44px以上であることを確認

**前提条件**:
- 命式データが1件保存済み
- ビューポート: iPhone SE (375px)

**テスト手順**:
1. SajuDetailPageに遷移
2. ヘッダーの閉じるボタンを確認
3. ボタンのサイズを測定

**期待結果**:
- ✅ 閉じるボタンの幅が48px以上
- ✅ 閉じるボタンの高さが48px以上
- ✅ ボタンがタップ可能

**Playwright実装例**:
```typescript
test('E2E-CHAIN-006-S6: タップ領域 - ヘッダーボタン', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });

  // SajuDetailPageに遷移（省略）

  // 閉じるボタンを確認
  const closeButton = page.locator('[data-testid="close-button"]');
  await expect(closeButton).toBeVisible();

  // ボタンサイズを測定
  const box = await closeButton.boundingBox();
  expect(box?.width).toBeGreaterThanOrEqual(48);
  expect(box?.height).toBeGreaterThanOrEqual(48);

  // ボタンをクリック
  await closeButton.click();

  // ListPageに遷移確認
  await page.waitForURL('**/list');
});
```

---

### E2E-CHAIN-006-S7: タップ領域 - ListPageアイコンボタン

**目的**: ListPageの削除ボタンのタップ領域が44px以上であることを確認

**前提条件**:
- 命式データが1件保存済み
- ビューポート: iPhone SE (375px)

**テスト手順**:
1. ListPageに遷移
2. 削除ボタンを確認
3. ボタンのサイズを測定

**期待結果**:
- ✅ 削除ボタンの幅が48px以上
- ✅ 削除ボタンの高さが48px以上
- ✅ ボタンがタップ可能

**Playwright実装例**:
```typescript
test('E2E-CHAIN-006-S7: タップ領域 - ListPageアイコンボタン', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });

  // ListPageに遷移（省略）

  // 削除ボタンを確認
  const deleteButton = page.locator('[data-testid="delete-button"]').first();
  await expect(deleteButton).toBeVisible();

  // ボタンサイズを測定
  const box = await deleteButton.boundingBox();
  expect(box?.width).toBeGreaterThanOrEqual(48);
  expect(box?.height).toBeGreaterThanOrEqual(48);
});
```

---

### E2E-CHAIN-006-S8: タップ領域 - 性別選択ボタン

**目的**: TopPageの性別選択ボタンのタップ領域が44px以上であることを確認

**前提条件**:
- ビューポート: iPhone SE (375px)

**テスト手順**:
1. TopPageに遷移
2. 性別選択ボタン（男性・女性）を確認
3. ボタンのサイズを測定

**期待結果**:
- ✅ 男性ボタンの高さが48px以上
- ✅ 女性ボタンの高さが48px以上
- ✅ ボタンがタップ可能

**Playwright実装例**:
```typescript
test('E2E-CHAIN-006-S8: タップ領域 - 性別選択ボタン', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });

  // TopPageに遷移
  await page.goto('http://localhost:3247');

  // 男性ボタンを確認
  const maleButton = page.locator('button:has-text("男性")');
  await expect(maleButton).toBeVisible();

  // ボタンサイズを測定
  const maleBox = await maleButton.boundingBox();
  expect(maleBox?.height).toBeGreaterThanOrEqual(48);

  // 女性ボタンを確認
  const femaleButton = page.locator('button:has-text("女性")');
  await expect(femaleButton).toBeVisible();

  // ボタンサイズを測定
  const femaleBox = await femaleButton.boundingBox();
  expect(femaleBox?.height).toBeGreaterThanOrEqual(48);
});
```

---

### E2E-CHAIN-006-U1: フォントサイズ - 四柱の天干地支

**目的**: 四柱の天干地支フォントサイズが14px以上で読みやすいことを確認

**前提条件**:
- 命式データが1件保存済み
- ビューポート: iPhone SE (375px)

**テスト手順**:
1. SajuDetailPageに遷移
2. PillarsSectionを確認
3. 天干地支のフォントサイズを測定

**期待結果**:
- ✅ 天干のフォントサイズが18px以上
- ✅ 地支のフォントサイズが18px以上
- ✅ 文字が読みやすい

**Playwright実装例**:
```typescript
test('E2E-CHAIN-006-U1: フォントサイズ - 四柱の天干地支', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });

  // SajuDetailPageに遷移（省略）

  // PillarsSectionを確認
  const pillarsSection = page.locator('[data-testid="pillars-section"]');
  await expect(pillarsSection).toBeVisible();

  // 天干のフォントサイズを測定
  const tianganElement = pillarsSection.locator('.tiangan').first();
  const tianganFontSize = await tianganElement.evaluate(el => {
    return window.getComputedStyle(el).fontSize;
  });
  expect(parseInt(tianganFontSize)).toBeGreaterThanOrEqual(18);

  // 地支のフォントサイズを測定
  const dizhiElement = pillarsSection.locator('.dizhi').first();
  const dizhiFontSize = await dizhiElement.evaluate(el => {
    return window.getComputedStyle(el).fontSize;
  });
  expect(parseInt(dizhiFontSize)).toBeGreaterThanOrEqual(18);
});
```

---

### E2E-CHAIN-006-U2: フォントサイズ - 大運カードの天干地支

**目的**: 大運カードの天干地支フォントサイズが14px以上で読みやすいことを確認

**前提条件**:
- 命式データが1件保存済み
- ビューポート: iPhone SE (375px)

**テスト手順**:
1. SajuDetailPageに遷移
2. DaeunScrollSectionを確認
3. 大運カードの天干地支のフォントサイズを測定

**期待結果**:
- ✅ 天干のフォントサイズが16px以上
- ✅ 地支のフォントサイズが16px以上
- ✅ 文字が読みやすい

**Playwright実装例**:
```typescript
test('E2E-CHAIN-006-U2: フォントサイズ - 大運カードの天干地支', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });

  // SajuDetailPageに遷移（省略）

  // 大運カードの天干を確認
  const daeunCard = page.locator('[data-testid="daeun-card-18"]');
  const tianganElement = daeunCard.locator('.tiangan');
  const tianganFontSize = await tianganElement.evaluate(el => {
    return window.getComputedStyle(el).fontSize;
  });
  expect(parseInt(tianganFontSize)).toBeGreaterThanOrEqual(16);

  // 大運カードの地支を確認
  const dizhiElement = daeunCard.locator('.dizhi');
  const dizhiFontSize = await dizhiElement.evaluate(el => {
    return window.getComputedStyle(el).fontSize;
  });
  expect(parseInt(dizhiFontSize)).toBeGreaterThanOrEqual(16);
});
```

---

### E2E-CHAIN-006-U3: フォントサイズ - エラーメッセージ

**目的**: エラーメッセージのフォントサイズが14px以上で読みやすいことを確認

**前提条件**:
- ビューポート: iPhone SE (375px)

**テスト手順**:
1. TopPageに遷移
2. 未入力で計算ボタンをクリック
3. エラーメッセージを確認
4. フォントサイズを測定

**期待結果**:
- ✅ エラーメッセージのフォントサイズが14px以上
- ✅ 文字が読みやすい

**Playwright実装例**:
```typescript
test('E2E-CHAIN-006-U3: フォントサイズ - エラーメッセージ', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });

  // TopPageに遷移
  await page.goto('http://localhost:3247');

  // 未入力で計算ボタンをクリック
  await page.click('button:has-text("計算する")');

  // エラーメッセージを確認
  const errorMessage = page.locator('[role="alert"]');
  await expect(errorMessage).toBeVisible();

  // フォントサイズを測定
  const fontSize = await errorMessage.evaluate(el => {
    return window.getComputedStyle(el).fontSize;
  });
  expect(parseInt(fontSize)).toBeGreaterThanOrEqual(14);
});
```

---

### E2E-CHAIN-006-U4: レイアウト - TopPage（性別ボタン配置）

**目的**: TopPageの性別ボタンが適切に配置されていることを確認

**前提条件**:
- ビューポート: iPhone SE (375px)

**テスト手順**:
1. TopPageに遷移
2. 性別ボタンの配置を確認

**期待結果**:
- ✅ 性別ボタンが横並びで表示される
- ✅ ボタン間の余白が適切
- ✅ レイアウト崩れなし

**Playwright実装例**:
```typescript
test('E2E-CHAIN-006-U4: レイアウト - TopPage（性別ボタン配置）', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });

  // TopPageに遷移
  await page.goto('http://localhost:3247');

  // 性別ボタンの配置を確認
  const genderButtons = page.locator('[data-testid="gender-buttons"]');
  await expect(genderButtons).toBeVisible();

  // ボタンが横並びであることを確認
  const box = await genderButtons.boundingBox();
  expect(box?.width).toBeLessThanOrEqual(375); // 画面幅以内
});
```

---

### E2E-CHAIN-006-U5: レイアウト - ListPage（空アイコン表示）

**目的**: ListPageの空アイコンが適切に表示されることを確認

**前提条件**:
- 命式データが0件
- ビューポート: iPhone SE (375px)

**テスト手順**:
1. ListPageに遷移（データなし）
2. 空アイコンの表示を確認

**期待結果**:
- ✅ 空アイコンが中央に表示される
- ✅ アイコンサイズが適切
- ✅ レイアウト崩れなし

**Playwright実装例**:
```typescript
test('E2E-CHAIN-006-U5: レイアウト - ListPage（空アイコン表示）', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });

  // ListPageに遷移（データなし）
  await page.goto('http://localhost:3247/list');

  // 空アイコンを確認
  const emptyIcon = page.locator('[data-testid="empty-icon"]');
  await expect(emptyIcon).toBeVisible();

  // アイコンが中央に表示されることを確認
  const box = await emptyIcon.boundingBox();
  expect(box?.x).toBeGreaterThan(100); // 左から100px以上
});
```

---

### E2E-CHAIN-006-U6: レイアウト - SajuCard（四柱ミニ表示）

**目的**: SajuCardの四柱ミニ表示が適切に表示されることを確認

**前提条件**:
- 命式データが1件保存済み
- ビューポート: iPhone SE (375px)

**テスト手順**:
1. ListPageに遷移
2. SajuCardを確認
3. 四柱ミニ表示を確認

**期待結果**:
- ✅ 四柱が横並びで表示される
- ✅ 天干地支のサイズが適切
- ✅ レイアウト崩れなし

**Playwright実装例**:
```typescript
test('E2E-CHAIN-006-U6: レイアウト - SajuCard（四柱ミニ表示）', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });

  // ListPageに遷移（省略）

  // SajuCardを確認
  const sajuCard = page.locator('[data-testid="saju-card"]').first();
  await expect(sajuCard).toBeVisible();

  // 四柱ミニ表示を確認
  const pillarsContainer = sajuCard.locator('[data-testid="pillars-mini"]');
  await expect(pillarsContainer).toBeVisible();

  // レイアウトが崩れていないことを確認
  const box = await pillarsContainer.boundingBox();
  expect(box?.width).toBeLessThanOrEqual(375);
});
```

---

### E2E-CHAIN-006-U7: レイアウト - LoginPage（パスワード忘れたリンク）

**目的**: LoginPageのパスワード忘れたリンクが適切に表示されることを確認

**前提条件**:
- ビューポート: iPhone SE (375px)

**テスト手順**:
1. LoginPageに遷移
2. パスワード忘れたリンクを確認

**期待結果**:
- ✅ リンクが適切に表示される
- ✅ フォントサイズが14px以上
- ✅ タップ可能

**Playwright実装例**:
```typescript
test('E2E-CHAIN-006-U7: レイアウト - LoginPage（パスワード忘れたリンク）', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });

  // LoginPageに遷移
  await page.goto('http://localhost:3247/login');

  // パスワード忘れたリンクを確認
  const forgotPasswordLink = page.locator('a:has-text("パスワードを忘れた")');
  await expect(forgotPasswordLink).toBeVisible();

  // フォントサイズを測定
  const fontSize = await forgotPasswordLink.evaluate(el => {
    return window.getComputedStyle(el).fontSize;
  });
  expect(parseInt(fontSize)).toBeGreaterThanOrEqual(14);
});
```

---

### E2E-CHAIN-006-P1: スクロール速度 - 大運カード（10個）のスクロール所要時間

**目的**: 大運カードのスクロールが滑らかに動作することを確認

**前提条件**:
- 命式データが1件保存済み
- ビューポート: iPhone SE (375px)

**テスト手順**:
1. SajuDetailPageに遷移
2. 大運カードを左から右にスクロール
3. スクロール所要時間を測定

**期待結果**:
- ✅ スクロール所要時間が1秒以内
- ✅ スクロールが滑らか

**Playwright実装例**:
```typescript
test('E2E-CHAIN-006-P1: スクロール速度 - 大運カード', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });

  // SajuDetailPageに遷移（省略）

  // スクロール開始時刻
  const startTime = Date.now();

  // スクロール実行
  const scrollContainer = page.locator('[data-testid="daeun-scroll-section"] > div').first();
  await scrollContainer.evaluate(el => {
    el.scrollLeft = 500;
  });

  // スクロール完了まで待機
  await page.waitForTimeout(100);

  // スクロール所要時間を測定
  const duration = Date.now() - startTime;
  expect(duration).toBeLessThan(1000); // 1秒以内
});
```

---

### E2E-CHAIN-006-P2: スクロール速度 - 月運カード（12個）のスクロール所要時間

**目的**: 月運カードのスクロールが滑らかに動作することを確認

**前提条件**:
- 命式データが1件保存済み
- 大運・年運を選択済み
- ビューポート: iPhone SE (375px)

**テスト手順**:
1. SajuDetailPageに遷移
2. 大運・年運を選択
3. 月運カードを左から右にスクロール
4. スクロール所要時間を測定

**期待結果**:
- ✅ スクロール所要時間が1秒以内
- ✅ スクロールが滑らか

**Playwright実装例**:
```typescript
test('E2E-CHAIN-006-P2: スクロール速度 - 月運カード', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });

  // SajuDetailPageに遷移・大運・年運選択（省略）

  // スクロール開始時刻
  const startTime = Date.now();

  // スクロール実行
  const scrollContainer = page.locator('[data-testid="month-scroll-section"] > div').first();
  await scrollContainer.evaluate(el => {
    el.scrollLeft = 400;
  });

  // スクロール完了まで待機
  await page.waitForTimeout(100);

  // スクロール所要時間を測定
  const duration = Date.now() - startTime;
  expect(duration).toBeLessThan(1000); // 1秒以内
});
```

---

### E2E-CHAIN-006-D1: デバイス別 - iPhone SE (375px)

**目的**: iPhone SE (375px)で全機能が正常に動作することを確認

**前提条件**:
- ビューポート: iPhone SE (375px × 667px)

**テスト手順**:
1. 全ページを順次確認
2. 横スクロール動作確認
3. タップ領域確認
4. レイアウト崩れ確認

**期待結果**:
- ✅ 全ページが正常に表示される
- ✅ 横スクロールが動作する
- ✅ タップ領域が44px以上
- ✅ レイアウト崩れなし

**Playwright実装例**:
```typescript
test('E2E-CHAIN-006-D1: デバイス別 - iPhone SE', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });

  // TopPage確認
  await page.goto('http://localhost:3247');
  await expect(page).toHaveTitle(/Golden Saju/);

  // ListPage確認
  await page.goto('http://localhost:3247/list');
  const listContent = page.locator('main');
  await expect(listContent).toBeVisible();

  // LoginPage確認
  await page.goto('http://localhost:3247/login');
  const loginForm = page.locator('form');
  await expect(loginForm).toBeVisible();

  // 横スクロール確認（SajuDetailPage）
  // （省略、他のテストケースと同様）
});
```

---

### E2E-CHAIN-006-D2: デバイス別 - iPhone 14 Pro (393px)

**目的**: iPhone 14 Pro (393px)で全機能が正常に動作することを確認

**前提条件**:
- ビューポート: iPhone 14 Pro (393px × 852px)

**テスト手順**:
1. 全ページを順次確認
2. 横スクロール動作確認
3. タップ領域確認
4. レイアウト崩れ確認

**期待結果**:
- ✅ 全ページが正常に表示される
- ✅ 横スクロールが動作する
- ✅ タップ領域が44px以上
- ✅ レイアウト崩れなし

**Playwright実装例**:
```typescript
test('E2E-CHAIN-006-D2: デバイス別 - iPhone 14 Pro', async ({ page }) => {
  await page.setViewportSize({ width: 393, height: 852 });

  // iPhone SEと同様のテスト（省略）
});
```

---

### E2E-CHAIN-006-D3: デバイス別 - iPad mini (768px)

**目的**: iPad mini (768px)で全機能が正常に動作することを確認

**前提条件**:
- ビューポート: iPad mini (768px × 1024px)

**テスト手順**:
1. 全ページを順次確認
2. 横スクロール動作確認
3. レイアウトが適切に拡大されることを確認

**期待結果**:
- ✅ 全ページが正常に表示される
- ✅ 横スクロールが動作する
- ✅ レイアウトがタブレットサイズに最適化される

**Playwright実装例**:
```typescript
test('E2E-CHAIN-006-D3: デバイス別 - iPad mini', async ({ page }) => {
  await page.setViewportSize({ width: 768, height: 1024 });

  // iPhone SEと同様のテスト（省略）
});
```

---

## テスト実行順序

### Phase 1: 横スクロール確認（Critical）
1. E2E-CHAIN-006-S1: 人生グラフ
2. E2E-CHAIN-006-S2: 大運
3. E2E-CHAIN-006-S3: 年運
4. E2E-CHAIN-006-S4: 月運
5. E2E-CHAIN-006-S5: 日運

### Phase 2: タップ領域確認（Critical）
6. E2E-CHAIN-006-S6: ヘッダーボタン
7. E2E-CHAIN-006-S7: ListPageアイコンボタン
8. E2E-CHAIN-006-S8: 性別選択ボタン

### Phase 3: UI/UX確認（推奨）
9. E2E-CHAIN-006-U1: 四柱の天干地支フォント
10. E2E-CHAIN-006-U2: 大運カードの天干地支フォント
11. E2E-CHAIN-006-U3: エラーメッセージフォント
12. E2E-CHAIN-006-U4: TopPageレイアウト
13. E2E-CHAIN-006-U5: ListPageレイアウト
14. E2E-CHAIN-006-U6: SajuCardレイアウト
15. E2E-CHAIN-006-U7: LoginPageレイアウト

### Phase 4: パフォーマンス確認
16. E2E-CHAIN-006-P1: 大運カードスクロール速度
17. E2E-CHAIN-006-P2: 月運カードスクロール速度

### Phase 5: クロスデバイス確認
18. E2E-CHAIN-006-D1: iPhone SE
19. E2E-CHAIN-006-D2: iPhone 14 Pro
20. E2E-CHAIN-006-D3: iPad mini

---

## 実装チェックリスト

### コード修正
- [ ] SajuDetailPage/index.tsx: maxWidth修正
- [ ] LifeGraphSection.tsx: グラフ幅800px化
- [ ] SajuDetailPage/index.tsx: ヘッダーボタン48px化
- [ ] ListPage/index.tsx: アイコンボタン48px化
- [ ] SettingsPage.tsx: レスポンシブ対応追加
- [ ] HomePage.tsx: ファイル削除
- [ ] YearScrollSection.tsx: webkit-overflow追加
- [ ] MonthScrollSection.tsx: webkit-overflow追加
- [ ] DayScrollSection.tsx: webkit-overflow追加

### テスト実装
- [ ] chain-006-responsive-mobile.spec.ts作成
- [ ] 20項目のテストケース実装
- [ ] Playwrightビューポート設定

### 検証
- [ ] 全20項目Pass
- [ ] 実機テスト（iPhone SE, 14 Pro）
- [ ] 横スクロール動作確認（5箇所全て）
- [ ] PC表示に影響なし

---

**作成日**: 2025-11-07
**最終更新**: 2025-11-07
**総テスト項目数**: 20項目
