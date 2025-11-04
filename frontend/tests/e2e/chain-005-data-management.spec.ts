import { test, expect } from '@playwright/test';

// CHAIN-005: データ管理統合 - E2Eテスト

/**
 * テストID: E2E-CHAIN-005-S1
 * テスト項目: 正常系 - 命式一覧取得と表示
 * 対象ページ: /list
 */
test('E2E-CHAIN-005-S1: 正常系 - 命式一覧取得と表示', async ({ page }) => {
  // ブラウザコンソールログを収集
  const consoleLogs: Array<{type: string, text: string}> = [];
  page.on('console', (msg) => {
    consoleLogs.push({
      type: msg.type(),
      text: msg.text()
    });
  });

  // ネットワークログを収集
  const networkLogs: Array<{url: string, method: string, status: number}> = [];
  page.on('response', (res) => {
    networkLogs.push({
      url: res.url(),
      method: res.request().method(),
      status: res.status()
    });
  });

  // 前提: ログイン済み
  await page.goto('http://localhost:3247/login');
  await page.fill('[data-testid="email"]', 'test@example.com');
  await page.fill('[data-testid="password"]', 'TestGoldenSaju2025!');

  // ログインAPIレスポンスを待機（クリック前にPromise設定）
  const loginResponsePromise = page.waitForResponse(res =>
    res.url().includes('/api/auth/login') && res.status() === 200
  , { timeout: 10000 });

  await page.click('[data-testid="login-button"]');

  // ログインAPIの成功を待機
  await loginResponsePromise;

  // ログイン後に/listページに自動遷移するまで待機
  await page.waitForURL('**/list', { timeout: 10000 });

  // 2. 命式一覧API呼び出し確認
  const listResponse = await page.waitForResponse(res =>
    res.url().includes('/api/saju/list') && res.status() === 200
  );
  const listData = await listResponse.json();

  // レスポンス検証（ページネーション形式）
  expect(listData).toHaveProperty('items');
  expect(listData).toHaveProperty('total');
  expect(listData).toHaveProperty('page');
  expect(listData).toHaveProperty('limit');
  expect(listData.items).toBeInstanceOf(Array);
  expect(listData.items.length).toBeGreaterThan(0);
  expect(listData.items[0]).toHaveProperty('id');
  expect(listData.items[0]).toHaveProperty('name');
  expect(listData.items[0]).toHaveProperty('birthDatetime');
  expect(listData.items[0]).toHaveProperty('fortuneLevel');
  expect(listData.items[0]).toHaveProperty('yearStem');
  expect(listData.items[0]).toHaveProperty('yearBranch');
  expect(listData.items[0]).toHaveProperty('monthStem');
  expect(listData.items[0]).toHaveProperty('monthBranch');
  expect(listData.items[0]).toHaveProperty('dayStem');
  expect(listData.items[0]).toHaveProperty('dayBranch');
  expect(listData.items[0]).toHaveProperty('hourStem');
  expect(listData.items[0]).toHaveProperty('hourBranch');

  // 3. UI検証: 一覧表示
  await expect(page.locator('[data-testid="saju-list-container"]')).toBeVisible();
  const sajuCards = page.locator('[data-testid="saju-list-item"]');
  await expect(sajuCards).toHaveCount(listData.items.length);

  // 4. 各カード内容確認
  const firstCard = sajuCards.first();
  await expect(firstCard.locator('[data-testid="saju-name"]')).toBeVisible();
  await expect(firstCard.locator('[data-testid="birth-datetime"]')).toBeVisible();
  await expect(firstCard.locator('[data-testid="fortune-icon"]')).toBeVisible();
  await expect(firstCard.locator('[data-testid="year-stem"]')).toContainText(listData.items[0].yearStem);

  // 5. カードクリックで詳細ページ遷移
  await firstCard.click();
  await expect(page).toHaveURL(new RegExp(`/detail/${listData.items[0].id}`));
});

/**
 * テストID: E2E-CHAIN-005-S2
 * テスト項目: 正常系 - 命式削除
 */
test('E2E-CHAIN-005-S2: 正常系 - 命式削除', async ({ page }) => {
  // 前提: ログイン済み
  await page.goto('http://localhost:3247/login');
  await page.fill('[data-testid="email"]', 'test@example.com');
  await page.fill('[data-testid="password"]', 'TestGoldenSaju2025!');

  const loginResponsePromise = page.waitForResponse(res =>
    res.url().includes('/api/auth/login') && res.status() === 200
  , { timeout: 10000 });

  await page.click('[data-testid="login-button"]');
  await loginResponsePromise;
  await page.waitForURL('**/list', { timeout: 10000 });

  // 1. 削除前の一覧取得
  const listResponseBefore = await page.waitForResponse(res =>
    res.url().includes('/api/saju/list') && res.status() === 200
  );
  const listDataBefore = await listResponseBefore.json();
  const initialTotal = listDataBefore.total;
  const initialItemsCount = listDataBefore.items.length;
  expect(initialTotal).toBeGreaterThan(0);

  // 2. 最初の命式カードを取得
  const sajuCards = page.locator('[data-testid="saju-list-item"]');
  const firstCard = sajuCards.first();
  const targetId = listDataBefore.items[0].id;

  // 3. 一覧APIレスポンスを記録（削除後のみを取得するため）
  let listResponseAfterCapture: any = null;
  page.on('response', async (res) => {
    if (res.url().includes('/api/saju/list') && res.request().method() === 'GET' && res.status() === 200) {
      // 削除後の一覧APIのみを記録
      const timestamp = Date.now();
      console.log(`[TEST] 一覧API検出: ${timestamp}`);
      listResponseAfterCapture = await res.json();
    }
  });

  // 4. 削除ボタンをクリック
  await firstCard.locator('[data-testid="delete-button"]').click();

  // 5. 確認ダイアログで「削除」をクリック
  const deleteResponsePromise = page.waitForResponse(res =>
    res.url().includes(`/api/saju/${targetId}`) &&
    res.request().method() === 'DELETE' &&
    res.status() === 200
  );

  await page.locator('[data-testid="confirm-delete-button"]').click();
  const deleteResponse = await deleteResponsePromise;

  // 6. 一覧APIの再呼び出しを待機（最大5秒）
  await page.waitForTimeout(1000);
  expect(listResponseAfterCapture).not.toBeNull();

  // 7. 削除後の一覧データを検証
  const listDataAfter = listResponseAfterCapture;

  // ページネーションにより表示件数は変わらない可能性があるため、total値で検証
  expect(listDataAfter.total).toBe(initialTotal - 1);

  // 削除したIDが一覧に含まれていないことを確認
  const deletedItemExists = listDataAfter.items.some((item: any) => item.id === targetId);
  expect(deletedItemExists).toBe(false);
});

/**
 * テストID: E2E-CHAIN-005-S3
 * テスト項目: 正常系 - データエクスポート
 */
test('E2E-CHAIN-005-S3: 正常系 - データエクスポート', async ({ page }) => {
  // コンソールログ収集
  page.on('console', msg => console.log('Browser console:', msg.text()));

  // 前提: ログイン済み
  await page.goto('http://localhost:3247/login');
  await page.fill('[data-testid="email"]', 'test@example.com');
  await page.fill('[data-testid="password"]', 'TestGoldenSaju2025!');

  const loginResponsePromise = page.waitForResponse(res =>
    res.url().includes('/api/auth/login') && res.status() === 200
  , { timeout: 10000 });

  await page.click('[data-testid="login-button"]');
  await loginResponsePromise;

  // ログイン後に/settingsページに遷移
  console.log('Navigating to /settings...');
  await page.goto('http://localhost:3247/settings');

  // エクスポートボタンが表示されるまで待機
  console.log('Waiting for export button...');
  const exportButton = await page.waitForSelector('[data-testid="export-button"]', { timeout: 10000 });
  console.log('Export button found:', !!exportButton);

  // ボタンのテキストを確認
  const buttonText = await exportButton?.textContent();
  console.log('Button text:', buttonText);

  // 1. エクスポートボタンをクリック（Promise設定後）
  console.log('Clicking export button...');
  const [exportResponse, download] = await Promise.all([
    page.waitForResponse(res => {
      console.log('Response:', res.url(), res.status());
      return res.url().includes('/api/saju/export') && res.status() === 200;
    }, { timeout: 30000 }),
    page.waitForEvent('download', { timeout: 30000 }),
    page.locator('[data-testid="export-button"]').click()
  ]);

  // 2. レスポンス検証（新しいレスポンス形式）
  const exportData = await exportResponse.json();
  expect(exportData).toHaveProperty('exported_at');
  expect(exportData).toHaveProperty('user_id');
  expect(exportData).toHaveProperty('count');
  expect(exportData).toHaveProperty('data');
  expect(exportData.count).toBeGreaterThan(0);
  expect(exportData.data).toBeInstanceOf(Array);
  expect(exportData.data.length).toBeGreaterThan(0);
  expect(exportData.data[0]).toHaveProperty('id');
  expect(exportData.data[0]).toHaveProperty('name');
  expect(exportData.data[0]).toHaveProperty('birth_datetime');
  expect(exportData.data[0]).toHaveProperty('gender');
  expect(exportData.data[0]).toHaveProperty('saju');
  expect(exportData.data[0]).toHaveProperty('created_at');

  // 3. ファイルダウンロード確認
  expect(download.suggestedFilename()).toMatch(/golden-saju-export-.*\.json/);
});

/**
 * テストID: E2E-CHAIN-005-S4
 * テスト項目: 正常系 - 連鎖テスト（一覧→削除→エクスポート）
 */
test('E2E-CHAIN-005-S4: 正常系 - 連鎖テスト（一覧→削除→エクスポート）', async ({ page }) => {
  // 前提: ログイン済み
  await page.goto('http://localhost:3247/login');
  await page.fill('[data-testid="email"]', 'test@example.com');
  await page.fill('[data-testid="password"]', 'TestGoldenSaju2025!');

  const loginResponsePromise = page.waitForResponse(res =>
    res.url().includes('/api/auth/login') && res.status() === 200
  , { timeout: 10000 });

  await page.click('[data-testid="login-button"]');
  await loginResponsePromise;

  // STEP 1: 一覧取得
  await page.waitForURL('**/list', { timeout: 10000 });
  const listResponse1 = await page.waitForResponse(res =>
    res.url().includes('/api/saju/list') && res.status() === 200
  );
  const listData1 = await listResponse1.json();
  const initialTotal = listData1.total;
  const targetId = listData1.items[0].id;

  // STEP 2: 削除
  const sajuCards = page.locator('[data-testid="saju-list-item"]');
  const firstCard = sajuCards.first();

  // 一覧APIレスポンスを記録（削除後のみを取得するため）
  let listResponseAfterCapture: any = null;
  page.on('response', async (res) => {
    if (res.url().includes('/api/saju/list') && res.request().method() === 'GET' && res.status() === 200) {
      // 削除後の一覧APIのみを記録
      const timestamp = Date.now();
      console.log(`[TEST S4] 一覧API検出: ${timestamp}`);
      listResponseAfterCapture = await res.json();
    }
  });

  // 削除ボタンをクリック
  await firstCard.locator('[data-testid="delete-button"]').click();

  // 確認ダイアログで「削除」をクリック
  const deleteResponsePromise = page.waitForResponse(res =>
    res.url().includes(`/api/saju/${targetId}`) &&
    res.request().method() === 'DELETE' &&
    res.status() === 200
  );

  await page.locator('[data-testid="confirm-delete-button"]').click();
  const deleteResponse = await deleteResponsePromise;

  // 一覧APIの再呼び出しを待機（最大5秒）
  await page.waitForTimeout(1000);
  expect(listResponseAfterCapture).not.toBeNull();

  // STEP 3: 削除後の一覧確認
  const listData2 = listResponseAfterCapture;
  expect(listData2.total).toBe(initialTotal - 1);

  // STEP 4: エクスポート
  await page.goto('http://localhost:3247/settings');
  await page.locator('[data-testid="export-button"]').click();
  const exportResponse = await page.waitForResponse(res =>
    res.url().includes('/api/saju/export') && res.status() === 200
  );
  const exportData = await exportResponse.json();
  expect(exportData.count).toBe(initialTotal - 1);
  expect(exportData.data.length).toBe(initialTotal - 1);
});

/**
 * テストID: E2E-CHAIN-005-S5
 * テスト項目: 異常系 - 存在しない命式の削除
 */
test('E2E-CHAIN-005-S5: 異常系 - 存在しない命式の削除', async ({ page }) => {
  // 前提: ログイン済み
  await page.goto('http://localhost:3247/login');
  await page.fill('[data-testid="email"]', 'test@example.com');
  await page.fill('[data-testid="password"]', 'TestGoldenSaju2025!');

  const loginResponsePromise = page.waitForResponse(res =>
    res.url().includes('/api/auth/login') && res.status() === 200
  , { timeout: 10000 });

  await page.click('[data-testid="login-button"]');
  const loginResponse = await loginResponsePromise;
  const loginData = await loginResponse.json();
  const token = loginData.accessToken;

  // 存在しないIDで削除API直接呼び出し（Authorizationヘッダー付き）
  const nonExistentId = 99999999;
  const response = await page.request.delete(
    `http://localhost:8432/api/saju/${nonExistentId}`,
    {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }
  );

  // 404エラーを期待
  expect(response.status()).toBe(404);
  const errorData = await response.json();
  expect(errorData).toHaveProperty('detail');
  expect(errorData.detail).toContain('見つかりません');
});

/**
 * テストID: E2E-CHAIN-005-S6
 * テスト項目: 異常系 - 空の一覧表示
 */
test('E2E-CHAIN-005-S6: 異常系 - 空の一覧表示', async ({ page }) => {
  // 前提: 全データを削除済みの新規ユーザーでログイン
  // 新規ユーザー作成
  const uniqueEmail = `test-empty-${Date.now()}@example.com`;
  await page.goto('http://localhost:3247/register');
  await page.fill('[data-testid="register-email"]', uniqueEmail);
  await page.fill('[data-testid="register-password"]', 'TestGoldenSaju2025!');
  await page.fill('[data-testid="register-password-confirm"]', 'TestGoldenSaju2025!');

  const registerResponsePromise = page.waitForResponse(res =>
    res.url().includes('/api/auth/register') && res.status() === 201
  , { timeout: 10000 });

  await page.click('[data-testid="register-button"]');
  await registerResponsePromise;

  // 登録後、自動的に/listページに遷移
  await page.waitForURL('**/list', { timeout: 10000 });

  // 一覧取得
  const listResponse = await page.waitForResponse(res =>
    res.url().includes('/api/saju/list') && res.status() === 200
  );
  const listData = await listResponse.json();
  expect(listData).toHaveProperty('items');
  expect(listData).toHaveProperty('total');
  expect(listData.items).toBeInstanceOf(Array);
  expect(listData.items.length).toBe(0);
  expect(listData.total).toBe(0);

  // UI検証: 空状態メッセージが表示されること
  await expect(page.locator('[data-testid="empty-state-message"]')).toBeVisible();
  await expect(page.locator('[data-testid="empty-state-message"]')).toContainText('命式がありません');
});

/**
 * テストID: E2E-CHAIN-005-SEC1
 * テスト項目: セキュリティ - 未ログイン状態で一覧取得
 */
test('E2E-CHAIN-005-SEC1: セキュリティ - 未ログイン状態で一覧取得', async ({ page }) => {
  // API直接呼び出しで401 or 403エラーを確認
  const response = await page.request.get('http://localhost:8432/api/saju/list');
  expect([401, 403]).toContain(response.status());
});
