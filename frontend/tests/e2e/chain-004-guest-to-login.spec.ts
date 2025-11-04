import { test, expect } from '@playwright/test';

// CHAIN-004: ゲスト→ログイン移行 - E2Eテスト

/**
 * テストID: E2E-CHAIN-004-S1
 * テスト項目: 正常系 - ゲストデータ移行成功
 * 対象ページ: /register
 */
test('E2E-CHAIN-004-S1: 正常系 - ゲストデータ移行成功', async ({ page }) => {
  console.log('[CHAIN-004-S1] テスト開始: ゲストデータ移行成功');

  // デバッグ: リクエスト/レスポンスをキャプチャ
  page.on('request', request => {
    if (request.url().includes('/api/auth/register')) {
      console.log('[NETWORK] Request to /api/auth/register');
      console.log('[NETWORK] Method:', request.method());
      console.log('[NETWORK] Headers:', request.headers());
      console.log('[NETWORK] PostData:', request.postData());
    }
  });

  page.on('response', async response => {
    if (response.url().includes('/api/auth/register')) {
      console.log('[NETWORK] Response from /api/auth/register');
      console.log('[NETWORK] Status:', response.status());
      console.log('[NETWORK] Headers:', response.headers());
      try {
        const body = await response.text();
        console.log('[NETWORK] Response Body:', body);
      } catch (e) {
        console.log('[NETWORK] Could not read response body');
      }
    }
  });

  page.on('console', msg => {
    console.log('[BROWSER]', msg.text());
  });

  // 1. LocalStorageにテストデータを保存
  await page.goto('http://localhost:3247/');
  await page.evaluate(() => {
    const testSajuData = [
      {
        id: 'guest-saju-001',
        name: 'ゲストテスト太郎',
        birthDatetime: '1990-03-15T14:30:00+09:00',
        gender: 'male',
        yearStem: '庚',
        yearBranch: '午',
        monthStem: '己',
        monthBranch: '卯',
        dayStem: '甲',
        dayBranch: '子',
        hourStem: '辛',
        hourBranch: '未',
        fortuneLevel: '吉',
        daeunList: [],
        createdAt: new Date().toISOString(),
      },
      {
        id: 'guest-saju-002',
        name: 'ゲストテスト花子',
        birthDatetime: '1995-06-20T10:15:00+09:00',
        gender: 'female',
        yearStem: '乙',
        yearBranch: '亥',
        monthStem: '壬',
        monthBranch: '午',
        dayStem: '丙',
        dayBranch: '寅',
        hourStem: '癸',
        hourBranch: '巳',
        fortuneLevel: '平',
        daeunList: [],
        createdAt: new Date().toISOString(),
      },
    ];
    localStorage.setItem('saju_data', JSON.stringify(testSajuData));
  });
  console.log('[CHAIN-004-S1] LocalStorageにゲストデータ保存完了（2件）');

  // 2. 新規登録ページにアクセス
  await page.goto('http://localhost:3247/register');
  console.log('[CHAIN-004-S1] 新規登録ページアクセス');

  // 3. フォーム入力
  const testEmail = `test-migrate-${Date.now()}@example.com`;
  await page.fill('[data-testid="register-email"]', testEmail);
  await page.fill('[data-testid="register-password"]', 'TestGoldenSaju2025!');
  await page.fill('[data-testid="register-password-confirm"]', 'TestGoldenSaju2025!');
  console.log('[CHAIN-004-S1] フォーム入力完了');

  // 4. 「ゲストデータを移行する」チェックボックスがONであることを確認
  const migrateCheckbox = page.locator('[data-testid="migrate-guest-data"]');
  await expect(migrateCheckbox).toBeChecked();
  console.log('[CHAIN-004-S1] データ移行チェックボックスON確認');

  // 5. 新規登録ボタンクリック
  await page.click('[data-testid="register-button"]');
  console.log('[CHAIN-004-S1] 新規登録ボタンクリック');

  // 6. 登録API呼び出し確認
  const registerResponse = await page.waitForResponse(
    res => res.url().includes('/api/auth/register') && res.status() === 201,
    { timeout: 10000 }
  );
  const authData = await registerResponse.json();
  console.log('[CHAIN-004-S1] 登録API成功:', { email: testEmail });

  // レスポンス検証
  expect(authData.accessToken).toBeTruthy();
  expect(authData.refreshToken).toBeTruthy();
  expect(authData.user.email).toBe(testEmail);
  expect(authData.user.role).toBe('user');

  // 7. データ移行API呼び出し確認
  const migrateResponse = await page.waitForResponse(
    res => res.url().includes('/api/saju/migrate') && res.status() === 201,
    { timeout: 10000 }
  );
  const migrateData = await migrateResponse.json();
  console.log('[CHAIN-004-S1] データ移行API成功:', migrateData);

  // データ移行レスポンス検証
  expect(migrateData.success).toBe(true);
  expect(migrateData.migratedCount).toBe(2);
  expect(migrateData.message).toContain('2件');

  // 8. LocalStorageがクリアされていることを確認
  const localStorageData = await page.evaluate(() => {
    return localStorage.getItem('saju_data');
  });
  expect(localStorageData).toBeNull();
  console.log('[CHAIN-004-S1] LocalStorageクリア確認 OK');

  // 9. リダイレクト確認（/list ページ）
  await expect(page).toHaveURL('http://localhost:3247/list', { timeout: 10000 });
  console.log('[CHAIN-004-S1] /listページにリダイレクト成功');

  // 10. 移行されたデータが一覧に表示されることを確認
  await page.waitForTimeout(2000); // データ読み込み待機

  const listItems = page.locator('[data-testid="saju-list-item"]');
  const itemCount = await listItems.count();
  expect(itemCount).toBeGreaterThanOrEqual(2); // 少なくとも移行した2件が表示される
  console.log(`[CHAIN-004-S1] 命式一覧に${itemCount}件表示確認 OK（移行した2件を含む）`);

  // 11. 移行されたデータ名を確認（一覧内に含まれるか）
  const allNames: string[] = [];
  for (let i = 0; i < itemCount; i++) {
    const name = await listItems.nth(i).locator('[data-testid="saju-name"]').textContent();
    if (name) allNames.push(name);
  }

  expect(allNames).toContain('ゲストテスト太郎');
  expect(allNames).toContain('ゲストテスト花子');
  console.log('[CHAIN-004-S1] 移行データ名確認 OK:', allNames.filter(n => n.includes('ゲストテスト')));

  console.log('[CHAIN-004-S1] テスト完了: すべての検証項目OK');
});

/**
 * テストID: E2E-CHAIN-004-S2
 * テスト項目: 正常系 - ゲストデータなしで新規登録
 * 対象ページ: /register
 */
test('E2E-CHAIN-004-S2: 正常系 - ゲストデータなしで新規登録', async ({ page }) => {
  console.log('[CHAIN-004-S2] テスト開始: ゲストデータなしで新規登録');

  // コンソールログを全てキャプチャ
  page.on('console', msg => {
    console.log(`[BROWSER CONSOLE - ${msg.type()}]`, msg.text());
  });

  // ページエラーをキャプチャ
  page.on('pageerror', error => {
    console.error('[PAGE ERROR]', error.message);
  });

  // ネットワークリクエストを全てキャプチャ
  page.on('request', request => {
    console.log('[REQUEST]', request.method(), request.url());
  });

  page.on('response', async response => {
    console.log('[RESPONSE]', response.status(), response.url());
    if (!response.ok()) {
      try {
        const text = await response.text();
        console.log('[RESPONSE ERROR BODY]', text);
      } catch (e) {
        // ignore
      }
    }
  });

  // 1. LocalStorageをクリア（ゲストデータなし状態）
  await page.goto('http://localhost:3247/');
  await page.evaluate(() => localStorage.clear());
  console.log('[CHAIN-004-S2] LocalStorageクリア完了');

  // 2. 新規登録ページにアクセス
  await page.goto('http://localhost:3247/register');
  console.log('[CHAIN-004-S2] 新規登録ページアクセス');

  // 3. フォーム入力
  const testEmail = `test-${Date.now()}@example.com`;
  await page.fill('[data-testid="register-email"]', testEmail);
  await page.fill('[data-testid="register-password"]', 'TestGoldenSaju2025!');
  await page.fill('[data-testid="register-password-confirm"]', 'TestGoldenSaju2025!');
  console.log('[CHAIN-004-S2] フォーム入力完了');

  // 4. 「ゲストデータを移行する」チェックボックスは初期状態でON
  // （ただしゲストデータがないため移行は実行されない）

  // 5. 新規登録ボタンクリック
  await page.click('[data-testid="register-button"]');
  console.log('[CHAIN-004-S2] 新規登録ボタンクリック');

  // 6. 登録API呼び出し確認
  const registerResponse = await page.waitForResponse(
    res => res.url().includes('/api/auth/register') && res.status() === 201,
    { timeout: 10000 }
  );
  const authData = await registerResponse.json();
  console.log('[CHAIN-004-S2] 登録API成功:', { email: testEmail });

  // レスポンス検証
  expect(authData.accessToken).toBeTruthy();
  expect(authData.refreshToken).toBeTruthy();
  expect(authData.user.email).toBe(testEmail);
  expect(authData.user.role).toBe('user');

  // 7. データ移行APIが呼び出されないことを確認
  let migrateApiCalled = false;
  page.on('response', res => {
    if (res.url().includes('/api/saju/migrate')) {
      migrateApiCalled = true;
    }
  });

  await page.waitForTimeout(2000); // 2秒待機
  expect(migrateApiCalled).toBe(false);
  console.log('[CHAIN-004-S2] データ移行APIは呼び出されていない（期待通り）');

  // 8. リダイレクト確認（/list ページ）
  await expect(page).toHaveURL('http://localhost:3247/list');
  console.log('[CHAIN-004-S2] /listページにリダイレクト成功');

  // 9. 空の一覧が表示されることを確認
  // （新規登録直後はデータなし）
  const emptyListMessage = page.locator('[data-testid="empty-list-message"]');
  const hasEmptyMessage = await emptyListMessage.count();

  if (hasEmptyMessage > 0) {
    await expect(emptyListMessage).toBeVisible();
    console.log('[CHAIN-004-S2] 空の一覧メッセージ表示確認 OK');
  } else {
    // または一覧が空であることを確認
    const listItems = page.locator('[data-testid="saju-list-item"]');
    await expect(listItems).toHaveCount(0);
    console.log('[CHAIN-004-S2] 命式一覧が空であることを確認 OK');
  }

  console.log('[CHAIN-004-S2] テスト完了: すべての検証項目OK');
});

/**
 * テストID: E2E-CHAIN-004-S3
 * テスト項目: 正常系 - データ移行チェックボックスOFFで新規登録
 * 対象ページ: /register
 */
test('E2E-CHAIN-004-S3: 正常系 - データ移行チェックボックスOFFで新規登録', async ({ page }) => {
  console.log('[CHAIN-004-S3] テスト開始: データ移行チェックボックスOFF');

  // 1. LocalStorageにテストデータを保存
  await page.goto('http://localhost:3247/');
  await page.evaluate(() => {
    const testSajuData = [
      {
        id: 'guest-saju-001',
        name: 'ゲストテスト太郎',
        birthDatetime: '1990-03-15T14:30:00+09:00',
        gender: 'male',
        yearStem: '庚',
        yearBranch: '午',
        monthStem: '己',
        monthBranch: '卯',
        dayStem: '甲',
        dayBranch: '子',
        hourStem: '辛',
        hourBranch: '未',
        fortuneLevel: '吉',
        daeunList: [],
        createdAt: new Date().toISOString(),
      },
      {
        id: 'guest-saju-002',
        name: 'ゲストテスト花子',
        birthDatetime: '1995-06-20T10:15:00+09:00',
        gender: 'female',
        yearStem: '乙',
        yearBranch: '亥',
        monthStem: '壬',
        monthBranch: '午',
        dayStem: '丙',
        dayBranch: '寅',
        hourStem: '癸',
        hourBranch: '巳',
        fortuneLevel: '平',
        daeunList: [],
        createdAt: new Date().toISOString(),
      },
    ];
    localStorage.setItem('saju_data', JSON.stringify(testSajuData));
  });
  console.log('[CHAIN-004-S3] LocalStorageにゲストデータ保存完了（2件）');

  // 2. 新規登録ページにアクセス
  await page.goto('http://localhost:3247/register');
  console.log('[CHAIN-004-S3] 新規登録ページアクセス');

  // 3. フォーム入力
  const testEmail = `test-nodata-${Date.now()}@example.com`;
  await page.fill('[data-testid="register-email"]', testEmail);
  await page.fill('[data-testid="register-password"]', 'TestGoldenSaju2025!');
  await page.fill('[data-testid="register-password-confirm"]', 'TestGoldenSaju2025!');
  console.log('[CHAIN-004-S3] フォーム入力完了');

  // 4. 「ゲストデータを移行する」チェックボックスをOFF
  const migrateCheckbox = page.locator('[data-testid="migrate-guest-data"]');
  await migrateCheckbox.uncheck();
  console.log('[CHAIN-004-S3] データ移行チェックボックスOFF');

  // チェックが外れたことを確認
  await expect(migrateCheckbox).not.toBeChecked();

  // 5. 新規登録ボタンクリック
  await page.click('[data-testid="register-button"]');
  console.log('[CHAIN-004-S3] 新規登録ボタンクリック');

  // 6. 登録API呼び出し確認
  const registerResponse = await page.waitForResponse(
    res => res.url().includes('/api/auth/register') && res.status() === 201,
    { timeout: 10000 }
  );
  const authData = await registerResponse.json();
  console.log('[CHAIN-004-S3] 登録API成功:', { email: testEmail });

  // レスポンス検証
  expect(authData.accessToken).toBeTruthy();
  expect(authData.refreshToken).toBeTruthy();
  expect(authData.user.email).toBe(testEmail);

  // 7. データ移行APIが呼び出されないことを確認
  let migrateApiCalled = false;
  page.on('response', res => {
    if (res.url().includes('/api/saju/migrate')) {
      migrateApiCalled = true;
    }
  });

  await page.waitForTimeout(2000); // 2秒待機
  expect(migrateApiCalled).toBe(false);
  console.log('[CHAIN-004-S3] データ移行APIは呼び出されていない（期待通り）');

  // 8. LocalStorageがクリアされていないことを確認（データ保護）
  const localStorageData = await page.evaluate(() => {
    return localStorage.getItem('saju_data');
  });
  expect(localStorageData).not.toBeNull();
  const sajuData = JSON.parse(localStorageData!);
  expect(sajuData).toHaveLength(2);
  console.log('[CHAIN-004-S3] LocalStorageデータは保護されている（2件残存）');

  // 9. リダイレクト確認
  await expect(page).toHaveURL('http://localhost:3247/list');
  console.log('[CHAIN-004-S3] /listページにリダイレクト成功');

  console.log('[CHAIN-004-S3] テスト完了: すべての検証項目OK');
});

/**
 * テストID: E2E-CHAIN-004-S4
 * テスト項目: 異常系 - データ移行中にエラー発生
 * 対象ページ: /register
 */
test('E2E-CHAIN-004-S4: 異常系 - データ移行中にエラー発生', async ({ page }) => {
  console.log('[CHAIN-004-S4] テスト開始: データ移行中にエラー発生');

  // 1. LocalStorageにテストデータを保存
  await page.goto('http://localhost:3247/');
  await page.evaluate(() => {
    const testSajuData = [
      {
        id: 'guest-saju-001',
        name: 'ゲストテスト太郎',
        birthDatetime: '1990-03-15T14:30:00+09:00',
        gender: 'male',
        yearStem: '庚',
        yearBranch: '午',
        monthStem: '己',
        monthBranch: '卯',
        dayStem: '甲',
        dayBranch: '子',
        hourStem: '辛',
        hourBranch: '未',
        fortuneLevel: '平',
        daeunList: [],
        createdAt: new Date().toISOString(),
      },
    ];
    localStorage.setItem('saju_data', JSON.stringify(testSajuData));
  });
  console.log('[CHAIN-004-S4] LocalStorageにゲストデータ保存完了（1件）');

  // 2. データ移行APIを強制的にエラーにする
  await page.route('**/api/saju/migrate', route => {
    route.fulfill({
      status: 500,
      contentType: 'application/json',
      body: JSON.stringify({ error: 'データ移行中にエラーが発生しました' }),
    });
  });
  console.log('[CHAIN-004-S4] データ移行APIをモック（500エラー）');

  // 3. 新規登録ページにアクセス
  await page.goto('http://localhost:3247/register');

  // 4. フォーム入力
  const testEmail = `test-error-${Date.now()}@example.com`;
  await page.fill('[data-testid="register-email"]', testEmail);
  await page.fill('[data-testid="register-password"]', 'TestGoldenSaju2025!');
  await page.fill('[data-testid="register-password-confirm"]', 'TestGoldenSaju2025!');
  console.log('[CHAIN-004-S4] フォーム入力完了');

  // 5. データ移行チェックボックスがON
  const migrateCheckbox = page.locator('[data-testid="migrate-guest-data"]');
  await expect(migrateCheckbox).toBeChecked();

  // 6. 新規登録ボタンクリック
  await page.click('[data-testid="register-button"]');
  console.log('[CHAIN-004-S4] 新規登録ボタンクリック');

  // 7. 登録は成功する
  const registerResponse = await page.waitForResponse(
    res => res.url().includes('/api/auth/register') && res.status() === 201,
    { timeout: 10000 }
  );
  expect(registerResponse.status()).toBe(201);
  console.log('[CHAIN-004-S4] 登録API成功（アカウント作成OK）');

  // 8. 移行エラーが発生するが、登録自体は成功しているため/listにリダイレクトされる
  await expect(page).toHaveURL('http://localhost:3247/list', { timeout: 5000 });
  console.log('[CHAIN-004-S4] /listページにリダイレクト確認 OK');

  // 9. LocalStorageが残っていることを確認（データ保護）
  // 移行エラー時はLocalStorageをクリアしない仕様
  const localStorageData = await page.evaluate(() => {
    return localStorage.getItem('saju_data');
  });
  expect(localStorageData).not.toBeNull();
  console.log('[CHAIN-004-S4] LocalStorageデータは保護されている');

  console.log('[CHAIN-004-S4] テスト完了: すべての検証項目OK');
});

/**
 * テストID: E2E-CHAIN-004-S5
 * テスト項目: UI/UX - 移行確認ダイアログの表示
 * 対象ページ: /register
 */
test('E2E-CHAIN-004-S5: UI/UX - 移行確認ダイアログの表示', async ({ page }) => {
  console.log('[CHAIN-004-S5] テスト開始: 移行確認ダイアログの表示');

  // 1. LocalStorageにテストデータを保存
  await page.goto('http://localhost:3247/');
  await page.evaluate(() => {
    const testSajuData = [
      {
        id: 'guest-saju-001',
        name: 'ゲストテスト太郎',
        birthDatetime: '1990-03-15T14:30:00+09:00',
        gender: 'male',
        yearStem: '庚',
        yearBranch: '午',
        monthStem: '己',
        monthBranch: '卯',
        dayStem: '甲',
        dayBranch: '子',
        hourStem: '辛',
        hourBranch: '未',
        fortuneLevel: '吉',
        daeunList: [],
        createdAt: new Date().toISOString(),
      },
      {
        id: 'guest-saju-002',
        name: 'ゲストテスト花子',
        birthDatetime: '1995-06-20T10:15:00+09:00',
        gender: 'female',
        yearStem: '乙',
        yearBranch: '亥',
        monthStem: '壬',
        monthBranch: '午',
        dayStem: '丙',
        dayBranch: '寅',
        hourStem: '癸',
        hourBranch: '巳',
        fortuneLevel: '平',
        daeunList: [],
        createdAt: new Date().toISOString(),
      },
    ];
    localStorage.setItem('saju_data', JSON.stringify(testSajuData));
  });
  console.log('[CHAIN-004-S5] LocalStorageにゲストデータ保存完了（2件）');

  // 2. 新規登録ページにアクセス
  await page.goto('http://localhost:3247/register');
  console.log('[CHAIN-004-S5] 新規登録ページアクセス');

  // 3. データ移行チェックボックスが表示され、初期状態でONであることを確認
  const migrateCheckbox = page.locator('[data-testid="migrate-guest-data"]');
  await expect(migrateCheckbox).toBeVisible();
  await expect(migrateCheckbox).toBeChecked();
  console.log('[CHAIN-004-S5] データ移行チェックボックス表示確認（初期状態ON）');

  // 4. チェックボックスのラベルテキスト確認
  // MUIのFormControlLabelはinput要素とlabel要素を含むラベル構造を生成
  // ページ内の「ゲストデータを移行する」テキストを確認
  const labelTextLocator = page.getByText('ゲストデータを移行する');
  await expect(labelTextLocator).toBeVisible();
  console.log('[CHAIN-004-S5] チェックボックスラベル表示確認');

  // 5. ヘルプテキストが表示されていることを確認
  const helpText = page.locator('[data-testid="migrate-help-text"]');
  if ((await helpText.count()) > 0) {
    await expect(helpText).toBeVisible();
    console.log('[CHAIN-004-S5] ヘルプテキスト表示確認');
  }

  // 6. チェックボックスのON/OFF切り替えが正常に動作することを確認
  await migrateCheckbox.uncheck();
  await expect(migrateCheckbox).not.toBeChecked();
  console.log('[CHAIN-004-S5] チェックボックスOFF切り替え成功');

  await migrateCheckbox.check();
  await expect(migrateCheckbox).toBeChecked();
  console.log('[CHAIN-004-S5] チェックボックスON切り替え成功');

  console.log('[CHAIN-004-S5] テスト完了: すべての検証項目OK');
});
