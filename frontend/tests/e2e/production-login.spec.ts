import { test, expect } from '@playwright/test';

const PRODUCTION_URL = 'https://frontend-7h8s12mf9-amis-projects-474dde3c.vercel.app';
const TEST_EMAIL = 'test@example.com';
const TEST_PASSWORD = 'TestGoldenSaju2025!';

test.describe('本番環境ログインテスト', () => {
  test('フロントエンドにアクセス可能', async ({ page }) => {
    await page.goto(PRODUCTION_URL);

    // ページタイトルを確認
    await expect(page).toHaveTitle(/Golden Saju|ゴールデン四柱推命/);

    // スクリーンショット保存
    await page.screenshot({ path: 'test-results/production-home.png' });

    console.log('✅ フロントエンドアクセス成功');
  });

  test('ログインページにアクセス可能', async ({ page }) => {
    await page.goto(`${PRODUCTION_URL}/login`);

    // ログインフォームが表示されることを確認
    await expect(page.locator('input[type="email"]')).toBeVisible();
    await expect(page.locator('input[type="password"]')).toBeVisible();

    await page.screenshot({ path: 'test-results/production-login-page.png' });

    console.log('✅ ログインページアクセス成功');
  });

  test('ログイン成功テスト', async ({ page }) => {
    // エラーログを収集
    const errors: string[] = [];
    page.on('console', msg => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
        console.log('コンソールエラー:', msg.text());
      }
    });

    page.on('pageerror', error => {
      errors.push(error.message);
      console.log('ページエラー:', error.message);
    });

    page.on('requestfailed', request => {
      console.log('リクエスト失敗:', request.url());
    });

    // ログインページへ
    await page.goto(`${PRODUCTION_URL}/login`);
    await page.screenshot({ path: 'test-results/step1-login-page.png' });

    // メール入力
    await page.fill('input[type="email"]', TEST_EMAIL);
    await page.screenshot({ path: 'test-results/step2-email-filled.png' });

    // パスワード入力
    await page.fill('input[type="password"]', TEST_PASSWORD);
    await page.screenshot({ path: 'test-results/step3-password-filled.png' });

    // ログインボタンクリック
    const loginButton = page.locator('[data-testid="login-button"]');
    await expect(loginButton).toBeVisible();
    await loginButton.click();

    console.log('ログインボタンをクリックしました...');
    await page.screenshot({ path: 'test-results/step4-after-click.png' });

    // ナビゲーション待機（最大10秒）
    try {
      await page.waitForURL((url) => !url.pathname.includes('/login'), {
        timeout: 10000
      });

      console.log('✅ ログイン後のページへ遷移しました');
      await page.screenshot({ path: 'test-results/step5-after-login.png' });

      // 現在のURL確認
      const currentUrl = page.url();
      console.log('現在のURL:', currentUrl);

      // ログイン成功を確認
      expect(currentUrl).not.toContain('/login');

      console.log('✅ ログイン成功！');

    } catch (error) {
      console.error('❌ ログイン失敗:', error);
      await page.screenshot({ path: 'test-results/step5-login-failed.png' });

      // エラー情報を出力
      if (errors.length > 0) {
        console.error('収集されたエラー:', errors);
      }

      throw error;
    }
  });

  test('バックエンドAPI疎通確認', async ({ request }) => {
    const backendUrl = 'https://golden-saju-api-235426778039.asia-northeast1.run.app';

    // ルートエンドポイント確認
    const response = await request.get(backendUrl);
    expect(response.ok()).toBeTruthy();

    const data = await response.json();
    console.log('API応答:', data);
    expect(data).toHaveProperty('message');

    console.log('✅ バックエンドAPI疎通成功');
  });
});
