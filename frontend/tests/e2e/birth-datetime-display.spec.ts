/**
 * E2Eテスト：生年月日時の表示確認
 *
 * 目的：入力した生年月日時が、詳細ページとリストページで正しく表示されることを確認
 *
 * テストケース：
 * 1. トップページで生年月日時を入力（1986年5月26日 05:00）
 * 2. 性別を選択
 * 3. 計算ボタンをクリック
 * 4. 詳細ページで「1986年5月26日 5:00」と表示されることを確認
 * 5. リストページに遷移
 * 6. カードに「1986年5月26日 5:00」と表示されることを確認
 */

import { test, expect } from '@playwright/test';

test.describe('生年月日時の表示確認', () => {
  test.beforeEach(async ({ page }) => {
    // テスト開始前にLocalStorageをクリア
    await page.goto('http://localhost:3248');
    await page.evaluate(() => localStorage.clear());
  });

  test('入力した生年月日時が詳細ページとリストページで正しく表示される', async ({ page }) => {
    // Step 1: トップページにアクセス
    await page.goto('http://localhost:3248');
    await page.waitForLoadState('networkidle');

    // Step 2: 生年月日時を入力（1986年5月26日 05:00）
    // 名前を入力
    await page.fill('input[name="name"]', 'テスト太郎');

    // 生年月日を入力
    const dateInput = page.locator('input[placeholder="生年月日を選択"]');
    await dateInput.click();
    // MUI DatePickerのカレンダーから日付を選択
    // まず年を選択（1986年）
    await page.click('text=1986年');
    await page.click('text=1986');

    // 月を選択（5月）
    await page.click('button[aria-label="5月を選択"]');

    // 日を選択（26日）
    await page.click('button[aria-label="5月 26, 1986"]');

    // 時刻を入力（05:00）
    const timeInput = page.locator('input[placeholder="時刻を選択"]');
    await timeInput.click();
    await page.keyboard.type('0500');

    // 性別を選択（男性）
    await page.click('input[value="male"]');

    // Step 3: 計算ボタンをクリック
    await page.click('button:has-text("命式を計算")');

    // ローディングが終わるまで待機
    await page.waitForLoadState('networkidle');
    await page.waitForSelector('[data-testid="basic-info-section"]', { timeout: 10000 });

    // Step 4: 詳細ページで生年月日時を確認
    const birthDatetimeText = await page.locator('[data-testid="basic-info-section"]').textContent();

    // 「1986年5月26日 5:00」または「1986年5月26日 05:00」のいずれかが表示されることを確認
    const isCorrectDate = birthDatetimeText?.includes('1986年5月26日 5:00') ||
                          birthDatetimeText?.includes('1986年5月26日 05:00');
    expect(isCorrectDate).toBeTruthy();

    // デバッグ用：実際の表示内容をログ出力
    console.log('[詳細ページ] 基本情報欄のテキスト:', birthDatetimeText);

    // Step 5: リストページに遷移
    await page.click('[data-testid="header-list-button"]');
    await page.waitForLoadState('networkidle');

    // Step 6: リストページで生年月日時を確認
    const cardDatetimeText = await page.locator('[data-testid="birth-datetime"]').first().textContent();

    // 「1986年5月26日 5:00」または「1986年5月26日 05:00」のいずれかが表示されることを確認
    const isCorrectCardDate = cardDatetimeText?.includes('1986年5月26日 5:00') ||
                              cardDatetimeText?.includes('1986年5月26日 05:00');
    expect(isCorrectCardDate).toBeTruthy();

    // デバッグ用：実際の表示内容をログ出力
    console.log('[リストページ] カードのテキスト:', cardDatetimeText);

    // スクリーンショット保存（証拠として）
    await page.screenshot({ path: 'tests/screenshots/birth-datetime-list-page.png' });
  });

  test.afterEach(async ({ page }) => {
    // テスト終了後にLocalStorageをクリア
    await page.evaluate(() => localStorage.clear());
  });
});
