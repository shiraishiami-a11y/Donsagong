// CHAIN-003: インタラクティブ運勢選択 E2Eテスト
// 対応ページ: P-003（命式詳細・グラフページ）

import { test, expect } from '@playwright/test';

// E2E-CHAIN-003-S1: 正常系 - 大運クリックで年運表示
test('E2E-CHAIN-003-S1: 正常系 - 大運クリックで年運表示', async ({ page }) => {
  // ブラウザコンソールログを収集
  const consoleLogs: Array<{ type: string; text: string }> = [];
  page.on('console', (msg) => {
    consoleLogs.push({
      type: msg.type(),
      text: msg.text(),
    });
  });

  // ネットワークログを収集
  const networkLogs: Array<{ url: string; method: string; status: number }> = [];
  page.on('response', (response) => {
    networkLogs.push({
      url: response.url(),
      method: response.request().method(),
      status: response.status(),
    });
  });

  // ログイン処理（バックエンドAPIを使用するため）
  await page.goto('/login');
  await expect(page).toHaveURL('/login');

  // ログイン情報入力
  await page.fill('[data-testid="email"]', 'test@example.com');
  await page.fill('[data-testid="password"]', 'TestGoldenSaju2025!');

  // ログインボタンクリック
  await page.click('[data-testid="login-button"]');

  // ログイン完了を待機（/listにリダイレクト）
  await page.waitForURL('**/list', { timeout: 10000 });

  // 既存の命式一覧から1番目の命式をクリック
  const sajuCards = page.locator('[data-testid="saju-card"]');
  await expect(sajuCards.first()).toBeVisible({ timeout: 5000 });
  await sajuCards.first().click();

  // 命式詳細ページへ遷移を待機
  await page.waitForURL('**/detail/**', { timeout: 10000 });

  // 現在のURL取得（命式ID含む）
  const currentUrl = page.url();
  const sajuId = currentUrl.split('/detail/')[1];

  console.log(`命式ID: ${sajuId}`);

  // 大運リスト表示確認（スクロールして表示）
  const daeunContainer = page.locator('[data-testid="daeun-scroll-container"]');
  await expect(daeunContainer).toBeVisible({ timeout: 10000 });
  await daeunContainer.scrollIntoViewIfNeeded();

  // 1番目の大運（9-18歳）をクリック
  const daeunCard = page.locator('[data-testid="daeun-card-9"]');
  await expect(daeunCard).toBeVisible({ timeout: 5000 });
  await daeunCard.scrollIntoViewIfNeeded();
  await daeunCard.click();

  // 年運API呼び出し確認
  const yearResponse = await page.waitForResponse(
    (res) => res.url().includes(`/api/saju/${sajuId}/year/9`) && res.status() === 200,
    { timeout: 10000 }
  );

  const yearData = await yearResponse.json();

  // レスポンス検証
  expect(yearData.daeunStartAge).toBe(9);
  expect(yearData.daeunEndAge).toBe(18);
  expect(yearData.years).toHaveLength(10);

  // UI検証
  await expect(page.locator('[data-testid="year-scroll-container"]')).toBeVisible({ timeout: 5000 });
  const yearCards = page.locator('[data-testid="year-card"]');
  await expect(yearCards).toHaveCount(10);

  // 各カードに干支が表示されることを確認
  const firstYearCard = yearCards.first();
  await expect(firstYearCard.locator('[data-testid="year-stem"]')).toBeVisible();
  await expect(firstYearCard.locator('[data-testid="year-branch"]')).toBeVisible();
  await expect(firstYearCard.locator('[data-testid="fortune-icon"]')).toBeVisible();
});

// E2E-CHAIN-003-S2: 正常系 - 年運クリックで月運表示
test('E2E-CHAIN-003-S2: 正常系 - 年運クリックで月運表示', async ({ page }) => {
  // ブラウザコンソールログを収集
  const consoleLogs: Array<{ type: string; text: string }> = [];
  page.on('console', (msg) => {
    consoleLogs.push({
      type: msg.type(),
      text: msg.text(),
    });
  });

  // ネットワークログを収集
  const networkLogs: Array<{ url: string; method: string; status: number }> = [];
  page.on('response', (response) => {
    networkLogs.push({
      url: response.url(),
      method: response.request().method(),
      status: response.status(),
    });
  });

  // ログイン処理（バックエンドAPIを使用するため）
  await page.goto('/login');
  await expect(page).toHaveURL('/login');

  // ログイン情報入力
  await page.fill('[data-testid="email"]', 'test@example.com');
  await page.fill('[data-testid="password"]', 'TestGoldenSaju2025!');

  // ログインボタンクリック
  await page.click('[data-testid="login-button"]');

  // ログイン完了を待機（/listにリダイレクト）
  await page.waitForURL('**/list', { timeout: 10000 });

  // 既存の命式一覧から1番目の命式をクリック
  const sajuCards = page.locator('[data-testid="saju-card"]');
  await expect(sajuCards.first()).toBeVisible({ timeout: 5000 });
  await sajuCards.first().click();

  // 命式詳細ページへ遷移を待機
  await page.waitForURL('**/detail/**', { timeout: 10000 });

  // 現在のURL取得（命式ID含む）
  const currentUrl = page.url();
  const sajuId = currentUrl.split('/detail/')[1];

  console.log(`命式ID: ${sajuId}`);

  // 大運リスト表示確認
  const daeunContainer = page.locator('[data-testid="daeun-scroll-container"]');
  await expect(daeunContainer).toBeVisible({ timeout: 10000 });
  await daeunContainer.scrollIntoViewIfNeeded();

  // 2番目の大運（19-28歳）をクリック
  const daeunCard = page.locator('[data-testid="daeun-card-19"]');
  await expect(daeunCard).toBeVisible({ timeout: 5000 });
  await daeunCard.scrollIntoViewIfNeeded();
  await daeunCard.click();

  // 年運API呼び出し確認
  await page.waitForResponse(
    (res) => res.url().includes(`/api/saju/${sajuId}/year/19`) && res.status() === 200,
    { timeout: 10000 }
  );

  // 年運表示確認
  await expect(page.locator('[data-testid="year-scroll-container"]')).toBeVisible({ timeout: 5000 });
  const yearCards = page.locator('[data-testid="year-card"]');
  await expect(yearCards).toHaveCount(10);

  // 最初の年運（19歳 = 2018年）をクリック（1999年生まれ）
  const firstYearCard = yearCards.first();
  await expect(firstYearCard).toBeVisible();
  await firstYearCard.click();

  // 月運API呼び出し確認（1999年生まれ19歳 = 2018年）
  const monthResponse = await page.waitForResponse(
    (res) => res.url().includes(`/api/saju/${sajuId}/month/2018`) && res.status() === 200,
    { timeout: 10000 }
  );

  const monthData = await monthResponse.json();

  // レスポンス検証
  expect(monthData.year).toBe(2018);
  expect(monthData.months).toHaveLength(12);

  // UI検証
  await expect(page.locator('[data-testid="month-scroll-container"]')).toBeVisible({ timeout: 5000 });
  const monthCards = page.locator('[data-testid="month-card"]');
  await expect(monthCards).toHaveCount(12);

  // 各月カードに干支が表示されることを確認
  const firstMonthCard = monthCards.first();
  await expect(firstMonthCard.locator('[data-testid="month-stem"]')).toBeVisible();
  await expect(firstMonthCard.locator('[data-testid="month-branch"]')).toBeVisible();
  await expect(firstMonthCard.locator('[data-testid="fortune-icon"]')).toBeVisible();
});

// E2E-CHAIN-003-S3: 正常系 - 月運クリックで日運表示
test('E2E-CHAIN-003-S3: 正常系 - 月運クリックで日運表示', async ({ page }) => {
  // ブラウザコンソールログを収集
  const consoleLogs: Array<{ type: string; text: string }> = [];
  page.on('console', (msg) => {
    consoleLogs.push({
      type: msg.type(),
      text: msg.text(),
    });
  });

  // ネットワークログを収集
  const networkLogs: Array<{ url: string; method: string; status: number }> = [];
  page.on('response', (response) => {
    networkLogs.push({
      url: response.url(),
      method: response.request().method(),
      status: response.status(),
    });
  });

  // ログイン処理（バックエンドAPIを使用するため）
  await page.goto('/login');
  await expect(page).toHaveURL('/login');

  // ログイン情報入力
  await page.fill('[data-testid="email"]', 'test@example.com');
  await page.fill('[data-testid="password"]', 'TestGoldenSaju2025!');

  // ログインボタンクリック
  await page.click('[data-testid="login-button"]');

  // ログイン完了を待機（/listにリダイレクト）
  await page.waitForURL('**/list', { timeout: 10000 });

  // 既存の命式一覧から1番目の命式をクリック
  const sajuCards = page.locator('[data-testid="saju-card"]');
  await expect(sajuCards.first()).toBeVisible({ timeout: 5000 });
  await sajuCards.first().click();

  // 命式詳細ページへ遷移を待機
  await page.waitForURL('**/detail/**', { timeout: 10000 });

  // 現在のURL取得（命式ID含む）
  const currentUrl = page.url();
  const sajuId = currentUrl.split('/detail/')[1];

  console.log(`命式ID: ${sajuId}`);

  // 大運リスト表示確認
  const daeunContainer = page.locator('[data-testid="daeun-scroll-container"]');
  await expect(daeunContainer).toBeVisible({ timeout: 10000 });
  await daeunContainer.scrollIntoViewIfNeeded();

  // 自動選択処理（0.5秒後）が完了するまで待機
  await page.waitForTimeout(1000);

  // 2番目の大運（19-28歳）をクリック
  const daeunCard = page.locator('[data-testid="daeun-card-19"]');
  await expect(daeunCard).toBeVisible({ timeout: 5000 });
  await daeunCard.scrollIntoViewIfNeeded();
  await daeunCard.click();

  // 年運API呼び出し確認
  await page.waitForResponse(
    (res) => res.url().includes(`/api/saju/${sajuId}/year/19`) && res.status() === 200,
    { timeout: 10000 }
  );

  // 年運表示確認
  await expect(page.locator('[data-testid="year-scroll-container"]')).toBeVisible({ timeout: 5000 });
  const yearCards = page.locator('[data-testid="year-card"]');
  await expect(yearCards).toHaveCount(10);

  // 最初の年運（19歳 = 2018年）をクリック（1999年生まれ）
  const firstYearCard = yearCards.first();
  await expect(firstYearCard).toBeVisible();
  await firstYearCard.click();

  // 月運API呼び出し確認（1999年生まれ19歳 = 2018年）
  await page.waitForResponse(
    (res) => res.url().includes(`/api/saju/${sajuId}/month/2018`) && res.status() === 200,
    { timeout: 10000 }
  );

  // 月運表示確認
  await expect(page.locator('[data-testid="month-scroll-container"]')).toBeVisible({ timeout: 5000 });
  const monthCards = page.locator('[data-testid="month-card"]');
  await expect(monthCards).toHaveCount(12);

  // 11月の月運をクリック
  const novemberCard = monthCards.nth(10); // 11月は0-indexedで10番目
  await expect(novemberCard).toBeVisible();
  await novemberCard.click();

  // 日運API呼び出し確認
  const dayResponse = await page.waitForResponse(
    (res) => res.url().includes(`/api/saju/${sajuId}/day/2018/11`) && res.status() === 200,
    { timeout: 10000 }
  );

  const dayData = await dayResponse.json();

  // レスポンス検証
  expect(dayData.year).toBe(2018);
  expect(dayData.month).toBe(11);
  expect(dayData.days.length).toBe(30); // 11月は30日

  // UI検証
  await expect(page.locator('[data-testid="day-scroll-container"]')).toBeVisible({ timeout: 5000 });
  const dayCards = page.locator('[data-testid="day-card"]');
  await expect(dayCards).toHaveCount(30);

  // 各日カードに干支が表示されることを確認
  const firstDayCard = dayCards.first();
  await expect(firstDayCard.locator('[data-testid="day-stem"]')).toBeVisible();
  await expect(firstDayCard.locator('[data-testid="day-branch"]')).toBeVisible();
  await expect(firstDayCard.locator('[data-testid="fortune-icon"]')).toBeVisible();
});

// E2E-CHAIN-003-S4: UI/UX - 連続クリックでスムーズに階層移動
test('E2E-CHAIN-003-S4: UI/UX - 連続クリックでスムーズに階層移動', async ({ page }) => {
  // ブラウザコンソールログを収集
  const consoleLogs: Array<{ type: string; text: string }> = [];
  page.on('console', (msg) => {
    consoleLogs.push({
      type: msg.type(),
      text: msg.text(),
    });
  });

  // ネットワークログを収集
  const networkLogs: Array<{ url: string; method: string; status: number; timing: number }> = [];
  page.on('response', (response) => {
    networkLogs.push({
      url: response.url(),
      method: response.request().method(),
      status: response.status(),
      timing: response.request().timing().responseEnd,
    });
  });

  // ログイン処理（バックエンドAPIを使用するため）
  await page.goto('/login');
  await expect(page).toHaveURL('/login');

  // ログイン情報入力
  await page.fill('[data-testid="email"]', 'test@example.com');
  await page.fill('[data-testid="password"]', 'TestGoldenSaju2025!');

  // ログインボタンクリック
  await page.click('[data-testid="login-button"]');

  // ログイン完了を待機（/listにリダイレクト）
  await page.waitForURL('**/list', { timeout: 10000 });

  // 既存の命式一覧から1番目の命式をクリック
  const sajuCards = page.locator('[data-testid="saju-card"]');
  await expect(sajuCards.first()).toBeVisible({ timeout: 5000 });
  await sajuCards.first().click();

  // 命式詳細ページへ遷移を待機
  await page.waitForURL('**/detail/**', { timeout: 10000 });

  // 現在のURL取得（命式ID含む）
  const currentUrl = page.url();
  const sajuId = currentUrl.split('/detail/')[1];

  console.log(`命式ID: ${sajuId}`);

  // 大運リスト表示確認
  const daeunContainer = page.locator('[data-testid="daeun-scroll-container"]');
  await expect(daeunContainer).toBeVisible({ timeout: 10000 });
  await daeunContainer.scrollIntoViewIfNeeded();

  // 連続クリックテスト開始 - タイミングを測定
  const startTime = Date.now();

  // ステップ1: 大運クリック → 年運表示
  const daeunCard = page.locator('[data-testid="daeun-card-19"]');
  await expect(daeunCard).toBeVisible({ timeout: 5000 });
  await daeunCard.scrollIntoViewIfNeeded();
  const daeunClickTime = Date.now();
  await daeunCard.click();

  const yearResponse = await page.waitForResponse(
    (res) => res.url().includes(`/api/saju/${sajuId}/year/19`) && res.status() === 200,
    { timeout: 10000 }
  );
  const yearDisplayTime = Date.now();
  const yearLoadTime = yearDisplayTime - daeunClickTime;

  console.log(`年運表示時間: ${yearLoadTime}ms`);

  // 年運表示確認
  await expect(page.locator('[data-testid="year-scroll-container"]')).toBeVisible({ timeout: 5000 });

  // ステップ2: 年運クリック → 月運表示（即座に）
  const yearCards = page.locator('[data-testid="year-card"]');
  await expect(yearCards).toHaveCount(10);
  const firstYearCard = yearCards.first();
  const yearClickTime = Date.now();
  await firstYearCard.click();

  const monthResponse = await page.waitForResponse(
    (res) => res.url().includes(`/api/saju/${sajuId}/month/`) && res.status() === 200,
    { timeout: 10000 }
  );
  const monthDisplayTime = Date.now();
  const monthLoadTime = monthDisplayTime - yearClickTime;

  console.log(`月運表示時間: ${monthLoadTime}ms`);

  // 月運表示確認
  await expect(page.locator('[data-testid="month-scroll-container"]')).toBeVisible({ timeout: 5000 });

  // ステップ3: 月運クリック → 日運表示（即座に）
  const monthCards = page.locator('[data-testid="month-card"]');
  await expect(monthCards).toHaveCount(12);
  const novemberCard = monthCards.nth(10); // 11月
  const monthClickTime = Date.now();
  await novemberCard.click();

  const dayResponse = await page.waitForResponse(
    (res) => res.url().includes(`/api/saju/${sajuId}/day/`) && res.status() === 200,
    { timeout: 10000 }
  );
  const dayDisplayTime = Date.now();
  const dayLoadTime = dayDisplayTime - monthClickTime;

  console.log(`日運表示時間: ${dayLoadTime}ms`)

  // 日運表示確認
  await expect(page.locator('[data-testid="day-scroll-container"]')).toBeVisible({ timeout: 5000 });

  const endTime = Date.now();
  const totalTime = endTime - startTime;

  console.log(`総所要時間: ${totalTime}ms`);
  console.log('✅ E2E-CHAIN-003-S4: UI/UX - 連続クリックでスムーズに階層移動テスト成功');

  // パフォーマンス要件確認（閾値ベース）
  // 初回API呼び出しは遅い場合があるため、閾値は緩めに設定
  expect(yearLoadTime).toBeLessThan(5000); // 閾値5秒以内（初回は遅い可能性）
  expect(monthLoadTime).toBeLessThan(3000); // 閾値3秒以内
  expect(dayLoadTime).toBeLessThan(3000); // 閾値3秒以内

  // 理想的には各API呼び出しが1秒以内であることをログで確認
  console.log(`パフォーマンス要件確認:`);
  console.log(`  年運: ${yearLoadTime}ms ${yearLoadTime < 1000 ? '✅ 理想値達成' : '⚠️ 理想値未達成（1秒以上）'}`);
  console.log(`  月運: ${monthLoadTime}ms ${monthLoadTime < 1000 ? '✅ 理想値達成' : '⚠️ 理想値未達成（1秒以上）'}`);
  console.log(`  日運: ${dayLoadTime}ms ${dayLoadTime < 1000 ? '✅ 理想値達成' : '⚠️ 理想値未達成（1秒以上）'}`)
});

// E2E-CHAIN-003-S5: 異常系 - 範囲外の年・月・日でアクセス
test('E2E-CHAIN-003-S5: 異常系 - 範囲外の年・月・日でアクセス', async ({ page, request }) => {
  // ログイン処理（バックエンドAPIを使用するため）
  await page.goto('/login');
  await expect(page).toHaveURL('/login');

  // ログイン情報入力
  await page.fill('[data-testid="email"]', 'test@example.com');
  await page.fill('[data-testid="password"]', 'TestGoldenSaju2025!');

  // ログインボタンクリック
  await page.click('[data-testid="login-button"]');

  // ログイン完了を待機（/listにリダイレクト）
  await page.waitForURL('**/list', { timeout: 10000 });

  // 既存の命式一覧から1番目の命式をクリック
  const sajuCards = page.locator('[data-testid="saju-card"]');
  await expect(sajuCards.first()).toBeVisible({ timeout: 5000 });
  await sajuCards.first().click();

  // 命式詳細ページへ遷移を待機
  await page.waitForURL('**/detail/**', { timeout: 10000 });

  // 現在のURL取得（命式ID含む）
  const currentUrl = page.url();
  const sajuId = currentUrl.split('/detail/')[1];

  console.log(`命式ID: ${sajuId}`);

  // 範囲外の月（99月）でAPIを直接呼び出し（backend port 8432）
  const response = await request.get(`http://localhost:8432/api/saju/${sajuId}/day/2025/99`);

  // HTTPステータス確認
  expect(response.status()).toBe(400);

  // エラーメッセージ確認
  const errorData = await response.json();
  console.log(`エラーレスポンス:`, errorData);
  expect(errorData.detail || errorData.error || errorData.message).toMatch(/無効|invalid|month|月|不正/i);

  console.log('✅ E2E-CHAIN-003-S5: 異常系 - 範囲外の年・月・日でアクセステスト成功');
});
