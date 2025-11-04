import { test, expect } from '@playwright/test';

/**
 * サンプルテスト - Playwright動作確認用
 * 実際のE2Eテスト作成時には削除してください
 */
test.describe('Playwright動作確認', () => {
  test('基本動作テスト', async ({ page }) => {
    // Playwrightが正常に動作することを確認
    await page.goto('/');
    expect(page).toBeTruthy();
  });
});
