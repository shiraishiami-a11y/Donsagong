import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright設定ファイル
 * ゴールデン四柱推命アプリケーション E2Eテスト設定
 */
export default defineConfig({
  // テストディレクトリ
  testDir: './tests/e2e',

  // 各テストのタイムアウト（30秒）
  timeout: 30 * 1000,

  // テスト実行設定
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : 4,

  // レポーター設定
  reporter: [
    ['html', { outputFolder: 'playwright-report' }],
    ['list'],
  ],

  // 全テスト共通の設定
  use: {
    // ベースURL
    baseURL: 'http://localhost:3247',

    // トレース設定
    trace: 'on-first-retry',

    // スクリーンショット設定
    screenshot: 'only-on-failure',

    // ビデオ設定
    video: 'retain-on-failure',

    // ヘッドレスモード（デフォルト: true）
    headless: true,
  },

  // テストプロジェクト設定
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],

  // 開発サーバー設定（オプション）
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3247',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
});
