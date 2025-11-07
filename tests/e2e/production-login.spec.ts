import { test, expect } from '@playwright/test';

const PRODUCTION_URL = 'https://frontend-q4ifdudam-amis-projects-474dde3c.vercel.app';
const TEST_EMAIL = 'test@goldensaju.local';
const TEST_PASSWORD = 'TestGoldenSaju2025!';

test.describe('本番環境ログインテスト', () => {
  test('フロントエンドにアクセスできる', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/ゴールデン四柱推命|Golden/);
    await page.screenshot({ path: 'tests/screenshots/home.png' });
  });

  test('ログインページにアクセスできる', async ({ page }) => {
    await page.goto('/login');
    await expect(page.getByText('ログイン')).toBeVisible();
    await page.screenshot({ path: 'tests/screenshots/login-page.png' });
  });

  test('ログインフォームが正しく表示される', async ({ page }) => {
    await page.goto('/login');
    
    // メールアドレス入力フィールド
    const emailInput = page.getByTestId('email');
    await expect(emailInput).toBeVisible();
    
    // パスワード入力フィールド
    const passwordInput = page.getByTestId('password');
    await expect(passwordInput).toBeVisible();
    
    // ログインボタン
    const loginButton = page.getByTestId('login-button');
    await expect(loginButton).toBeVisible();
  });

  test('本番環境でログインする', async ({ page }) => {
    await page.goto('/login');

    // メールアドレス入力
    await page.getByTestId('email').fill(TEST_EMAIL);
    
    // パスワード入力
    await page.getByTestId('password').fill(TEST_PASSWORD);
    
    // ログインボタンをクリック
    await page.getByTestId('login-button').click();

    // ログイン後のページ遷移を待つ（最大10秒）
    await page.waitForURL((url) => !url.pathname.includes('/login'), { timeout: 10000 });
    
    // ログイン成功のスクリーンショット
    await page.screenshot({ path: 'tests/screenshots/login-success.png' });
    
    // URLがログインページ以外になっているか確認
    const currentUrl = page.url();
    expect(currentUrl).not.toContain('/login');
    
    console.log('ログイン成功！現在のURL:', currentUrl);
  });
});
