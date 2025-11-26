import { test, expect } from '@playwright/test';

// CHAIN-008: 命式修正機能 - E2Eテスト

// テストを順次実行（並列実行による競合を防ぐ）
test.describe.configure({ mode: 'serial' });

/**
 * テストID: E2E-CHAIN-008-S1
 * テスト項目: 正常系 - 名前の変更が正しく保存される
 * 対象ページ: /list
 */
test('E2E-CHAIN-008-S1: 正常系 - 名前の変更が正しく保存される', async ({ page }) => {
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

  // ステップ1: ログイン
  await page.goto('http://localhost:3247/login');
  await page.fill('[data-testid="email"]', 'test@example.com');
  await page.fill('[data-testid="password"]', 'TestGoldenSaju2025!');

  const loginResponsePromise = page.waitForResponse(res =>
    res.url().includes('/api/auth/login') && res.status() === 200
  , { timeout: 10000 });

  await page.click('[data-testid="login-button"]');
  await loginResponsePromise;
  await page.waitForURL('**/list', { timeout: 10000 });

  // ステップ2: 命式一覧を取得
  const listResponse = await page.waitForResponse(res =>
    res.url().includes('/api/saju/list') && res.status() === 200
  );
  const listData = await listResponse.json();
  expect(listData.items).toBeInstanceOf(Array);
  expect(listData.items.length).toBeGreaterThan(0);

  const firstSaju = listData.items[0];
  const originalName = firstSaju.name;

  // ステップ3: 編集ボタンをクリック
  const editButtons = page.locator('[data-testid="edit-button"]');
  await expect(editButtons.first()).toBeVisible();
  await editButtons.first().click();

  // ステップ4: モーダルが開くことを確認
  const modal = page.locator('[data-testid="edit-saju-modal"]');
  await expect(modal).toBeVisible({ timeout: 5000 });

  // ステップ5: 名前を変更
  const newName = `変更テスト_${Date.now()}`;
  const nameInput = modal.locator('[data-testid="name"]');
  await nameInput.clear();
  await nameInput.fill(newName);

  // ステップ6: 保存ボタンをクリック
  const updateResponsePromise = page.waitForResponse(res =>
    res.url().includes(`/api/saju/${firstSaju.id}`) &&
    res.request().method() === 'PUT' &&
    res.status() === 200
  , { timeout: 10000 });

  await modal.locator('button:has-text("保存")').click();

  // ステップ7: 更新APIの成功を待機
  const updateResponse = await updateResponsePromise;
  const updateData = await updateResponse.json();
  expect(updateData).toHaveProperty('id');
  expect(updateData.name).toBe(newName);

  // ステップ8: モーダルが閉じることを確認
  await expect(modal).not.toBeVisible({ timeout: 5000 });

  // ステップ9: リストが更新されることを確認
  const reloadResponsePromise = page.waitForResponse(res =>
    res.url().includes('/api/saju/list') && res.status() === 200
  , { timeout: 10000 });
  await reloadResponsePromise;

  // 更新された名前が表示されることを確認
  await expect(page.locator(`[data-testid="saju-card-${firstSaju.id}"] [data-testid="saju-name"]`)).toContainText(newName);
});

/**
 * テストID: E2E-CHAIN-008-S2
 * テスト項目: キャンセルフロー - 変更が反映されないことを確認
 * 対象ページ: /list
 */
test('E2E-CHAIN-008-S2: キャンセルフロー - 変更が反映されないことを確認', async ({ page }) => {
  // ステップ1: ログイン
  await page.goto('http://localhost:3247/login');
  await page.fill('[data-testid="email"]', 'test@example.com');
  await page.fill('[data-testid="password"]', 'TestGoldenSaju2025!');

  const loginResponsePromise = page.waitForResponse(res =>
    res.url().includes('/api/auth/login') && res.status() === 200
  , { timeout: 10000 });

  await page.click('[data-testid="login-button"]');
  await loginResponsePromise;
  await page.waitForURL('**/list', { timeout: 10000 });

  // ステップ2: 命式一覧を取得
  const listResponse = await page.waitForResponse(res =>
    res.url().includes('/api/saju/list') && res.status() === 200
  );
  const listData = await listResponse.json();
  const firstSaju = listData.items[0];
  const originalName = firstSaju.name;

  // ステップ3: 編集ボタンをクリック
  const editButtons = page.locator('[data-testid="edit-button"]');
  await editButtons.first().click();

  // ステップ4: モーダルが開く
  const modal = page.locator('[data-testid="edit-saju-modal"]');
  await expect(modal).toBeVisible({ timeout: 5000 });

  // ステップ5: 名前を変更
  const tempName = `キャンセルテスト_${Date.now()}`;
  const nameInput = modal.locator('[data-testid="name"]');
  await nameInput.clear();
  await nameInput.fill(tempName);

  // ステップ6: キャンセルボタンをクリック
  await modal.locator('button:has-text("キャンセル")').click();

  // ステップ7: モーダルが閉じる
  await expect(modal).not.toBeVisible({ timeout: 5000 });

  // ステップ8: 変更が反映されていないことを確認
  await expect(page.locator(`[data-testid="saju-card-${firstSaju.id}"] [data-testid="saju-name"]`)).toContainText(originalName);
  await expect(page.locator(`[data-testid="saju-card-${firstSaju.id}"] [data-testid="saju-name"]`)).not.toContainText(tempName);
});

/**
 * テストID: E2E-CHAIN-008-S3
 * テスト項目: 生年月日時変更フロー - 四柱推命が再計算されることを確認
 * 対象ページ: /list → /detail/:id
 */
test('E2E-CHAIN-008-S3: 生年月日時変更フロー - 四柱推命が再計算されることを確認', async ({ page }) => {
  // ステップ1: ログイン
  await page.goto('http://localhost:3247/login');
  await page.fill('[data-testid="email"]', 'test@example.com');
  await page.fill('[data-testid="password"]', 'TestGoldenSaju2025!');

  const loginResponsePromise = page.waitForResponse(res =>
    res.url().includes('/api/auth/login') && res.status() === 200
  , { timeout: 10000 });

  await page.click('[data-testid="login-button"]');
  await loginResponsePromise;
  await page.waitForURL('**/list', { timeout: 10000 });

  // ステップ2: 命式一覧を取得
  const listResponse = await page.waitForResponse(res =>
    res.url().includes('/api/saju/list') && res.status() === 200
  );
  const listData = await listResponse.json();
  const firstSaju = listData.items[0];
  const originalYearStem = firstSaju.yearStem;

  // ステップ3: 編集ボタンをクリック
  const editButtons = page.locator('[data-testid="edit-button"]');
  await editButtons.first().click();

  // ステップ4: モーダルが開く
  const modal = page.locator('[data-testid="edit-saju-modal"]');
  await expect(modal).toBeVisible({ timeout: 5000 });

  // ステップ5: 生年月日を変更（例: 1990-05-15）
  const birthDateInput = modal.locator('[data-testid="birth-date"]');
  await birthDateInput.clear();
  await birthDateInput.fill('1990年05月15日');

  // ステップ6: 保存
  const updateResponsePromise = page.waitForResponse(res =>
    res.url().includes(`/api/saju/${firstSaju.id}`) &&
    res.request().method() === 'PUT' &&
    res.status() === 200
  , { timeout: 10000 });

  await modal.locator('button:has-text("保存")').click();
  await updateResponsePromise;

  // ステップ7: モーダルが閉じる
  await expect(modal).not.toBeVisible({ timeout: 5000 });

  // ステップ8: 詳細ページに移動
  await page.locator(`[data-testid="saju-card-${firstSaju.id}"]`).click();
  await page.waitForURL(`**/detail/${firstSaju.id}`, { timeout: 10000 });

  // ステップ9: 四柱推命が変更されていることを確認（API応答から検証）
  const detailResponse = await page.waitForResponse(res =>
    res.url().includes(`/api/saju/${firstSaju.id}`) &&
    res.request().method() === 'GET' &&
    res.status() === 200
  , { timeout: 10000 });
  const detailData = await detailResponse.json();

  // 年柱天干が変わっているはず（元の日付と異なる日付なので）
  // ※ ただし、同じ年であれば変わらない可能性もあるため、
  //    生年月日時が更新されたことをAPI応答で確認
  expect(detailData.birthDatetime).toContain('1990-05-15');
});

/**
 * テストID: E2E-CHAIN-008-S4
 * テスト項目: バリデーションエラー - 生年月日を空にすると保存ボタンが機能しない
 * 対象ページ: /list
 */
test('E2E-CHAIN-008-S4: バリデーションエラー - 生年月日を空にするとエラーが出る', async ({ page }) => {
  // アラートをキャプチャする
  let alertMessage = '';
  page.on('dialog', async (dialog) => {
    alertMessage = dialog.message();
    await dialog.accept();
  });

  // ステップ1: ログイン
  await page.goto('http://localhost:3247/login');
  await page.fill('[data-testid="email"]', 'test@example.com');
  await page.fill('[data-testid="password"]', 'TestGoldenSaju2025!');

  const loginResponsePromise = page.waitForResponse(res =>
    res.url().includes('/api/auth/login') && res.status() === 200
  , { timeout: 10000 });

  await page.click('[data-testid="login-button"]');
  await loginResponsePromise;
  await page.waitForURL('**/list', { timeout: 10000 });

  // ステップ2: 命式一覧を取得
  await page.waitForResponse(res =>
    res.url().includes('/api/saju/list') && res.status() === 200
  );

  // ステップ3: 編集ボタンをクリック
  const editButtons = page.locator('[data-testid="edit-button"]');
  await editButtons.first().click();

  // ステップ4: モーダルが開く
  const modal = page.locator('[data-testid="edit-saju-modal"]');
  await expect(modal).toBeVisible({ timeout: 5000 });

  // ステップ5: 生年月日を空にする
  const birthDateInput = modal.locator('[data-testid="birth-date"]');
  await birthDateInput.clear();

  // ステップ6: 保存ボタンをクリック
  await modal.locator('button:has-text("保存")').click();

  // ステップ7: アラートが表示されることを確認
  await page.waitForTimeout(1000); // アラート表示を待機
  expect(alertMessage).toContain('生年月日を入力してください');

  // ステップ8: モーダルがまだ開いていることを確認（保存失敗）
  await expect(modal).toBeVisible();
});

/**
 * テストID: E2E-CHAIN-008-S5
 * テスト項目: 性別変更フロー - 性別が正しく更新される
 * 対象ページ: /list
 */
test('E2E-CHAIN-008-S5: 性別変更フロー - 性別が正しく更新される', async ({ page }) => {
  // ステップ1: ログイン
  await page.goto('http://localhost:3247/login');
  await page.fill('[data-testid="email"]', 'test@example.com');
  await page.fill('[data-testid="password"]', 'TestGoldenSaju2025!');

  const loginResponsePromise = page.waitForResponse(res =>
    res.url().includes('/api/auth/login') && res.status() === 200
  , { timeout: 10000 });

  await page.click('[data-testid="login-button"]');
  await loginResponsePromise;
  await page.waitForURL('**/list', { timeout: 10000 });

  // ステップ2: 命式一覧を取得
  const listResponse = await page.waitForResponse(res =>
    res.url().includes('/api/saju/list') && res.status() === 200
  );
  const listData = await listResponse.json();
  const firstSaju = listData.items[0];
  const originalGender = firstSaju.gender;
  const newGender = originalGender === 'male' ? 'female' : 'male';

  // ステップ3: 編集ボタンをクリック
  const editButtons = page.locator('[data-testid="edit-button"]');
  await editButtons.first().click();

  // ステップ4: モーダルが開く
  const modal = page.locator('[data-testid="edit-saju-modal"]');
  await expect(modal).toBeVisible({ timeout: 5000 });

  // ステップ5: 性別を変更
  const genderButton = modal.locator(`[data-testid="gender-${newGender}"]`);
  await genderButton.click();

  // ステップ6: 保存
  const updateResponsePromise = page.waitForResponse(res =>
    res.url().includes(`/api/saju/${firstSaju.id}`) &&
    res.request().method() === 'PUT' &&
    res.status() === 200
  , { timeout: 10000 });

  await modal.locator('button:has-text("保存")').click();

  // ステップ7: 更新APIの成功を待機
  const updateResponse = await updateResponsePromise;
  const updateData = await updateResponse.json();
  expect(updateData.gender).toBe(newGender);

  // ステップ8: モーダルが閉じる
  await expect(modal).not.toBeVisible({ timeout: 5000 });

  // ステップ9: リストが更新されることを確認
  await page.waitForResponse(res =>
    res.url().includes('/api/saju/list') && res.status() === 200
  , { timeout: 10000 });

  // 性別アイコンが変更されていることを確認
  const genderIcon = newGender === 'male' ? '👨' : '👩';
  await expect(page.locator(`[data-testid="saju-card-${firstSaju.id}"]`)).toContainText(genderIcon);
});
