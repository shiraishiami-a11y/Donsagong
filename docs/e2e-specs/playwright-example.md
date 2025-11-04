# Playwright実装例 - ゴールデン四柱推命アプリケーション

## 概要

このドキュメントは、E2Eテスト実装時に参考にするPlaywrightのベストプラクティスと実装例をまとめたものです。

---

## プロジェクト構造

```
frontend/
├── playwright.config.ts        # Playwright設定
├── tests/
│   ├── fixtures/               # テストデータ
│   │   ├── auth-test-data.ts
│   │   ├── saju-test-data.ts
│   │   └── fortune-test-data.ts
│   ├── helpers/                # ヘルパー関数
│   │   ├── auth-helper.ts
│   │   └── api-helper.ts
│   └── e2e/                    # E2Eテスト
│       ├── chain/              # 連鎖テスト
│       │   ├── CHAIN-001.spec.ts
│       │   ├── CHAIN-002.spec.ts
│       │   ├── CHAIN-003.spec.ts
│       │   ├── CHAIN-004.spec.ts
│       │   └── CHAIN-005.spec.ts
│       └── unit/               # 単品テスト
│           ├── auth-endpoints.spec.ts
│           ├── saju-calculation.spec.ts
│           └── ...
└── package.json
```

---

## Playwright設定ファイル

`frontend/playwright.config.ts`:

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  // テストディレクトリ
  testDir: './tests/e2e',

  // タイムアウト設定
  timeout: 30000,        // 各テストケースのタイムアウト（30秒）
  expect: {
    timeout: 5000        // expect()のタイムアウト（5秒）
  },

  // リトライ設定
  retries: process.env.CI ? 2 : 0,  // CI環境では2回リトライ

  // 並列実行設定
  workers: process.env.CI ? 2 : 4,  // CI環境では2ワーカー、ローカルでは4ワーカー

  // レポート設定
  reporter: [
    ['html', { outputFolder: 'playwright-report' }],
    ['json', { outputFile: 'test-results/results.json' }],
    ['junit', { outputFile: 'test-results/results.xml' }]
  ],

  // 全テスト共通設定
  use: {
    // ベースURL
    baseURL: 'http://localhost:3247',

    // トレース設定（失敗時のみ記録）
    trace: 'on-first-retry',

    // スクリーンショット（失敗時のみ）
    screenshot: 'only-on-failure',

    // ビデオ録画（失敗時のみ保持）
    video: 'retain-on-failure',

    // ブラウザコンテキストのタイムアウト
    actionTimeout: 10000,
    navigationTimeout: 15000
  },

  // ブラウザ設定
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    // モバイルブラウザ
    {
      name: 'mobile-chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'mobile-safari',
      use: { ...devices['iPhone 12'] },
    },
  ],

  // 開発サーバー設定（テスト前に自動起動）
  webServer: {
    command: 'npm run dev',
    port: 3247,
    reuseExistingServer: !process.env.CI,  // CI以外では既存サーバーを再利用
    timeout: 120000  // 起動タイムアウト（120秒）
  },
});
```

---

## テストデータ定義

`tests/fixtures/saju-test-data.ts`:

```typescript
export const testBirthData = {
  // 男性データ（1990年生まれ）
  male1990: {
    birthDatetime: '1990-03-15T14:30:00+09:00',
    gender: 'male' as const,
    name: 'テスト太郎',
    expected: {
      yearStem: '庚',
      yearBranch: '午',
      monthStem: '己',
      monthBranch: '卯',
      isForward: true  // 男性 + 陽干(庚) → 順行
    }
  },

  // 女性データ（1995年生まれ）
  female1995: {
    birthDatetime: '1995-06-20T10:15:00+09:00',
    gender: 'female' as const,
    name: 'テスト花子',
    expected: {
      yearStem: '乙',
      yearBranch: '亥',
      monthStem: '壬',
      monthBranch: '午',
      isForward: false  // 女性 + 陰干(乙) → 逆行
    }
  },

  // エッジケース（範囲最小値）
  edge1900: {
    birthDatetime: '1900-01-01T00:00:00+09:00',
    gender: 'male' as const,
    name: 'エッジケース1900'
  },

  // エッジケース（範囲最大値）
  edge2109: {
    birthDatetime: '2109-12-31T23:59:00+09:00',
    gender: 'female' as const,
    name: 'エッジケース2109'
  }
};

export const testAuthData = {
  validUser: {
    email: 'test@goldensaju.local',
    password: 'TestGoldenSaju2025!'
  },
  newUser: {
    email: `test-${Date.now()}@goldensaju.local`,  // ユニークなメール
    password: 'NewUser123!'
  }
};
```

---

## ヘルパー関数

`tests/helpers/auth-helper.ts`:

```typescript
import { Page } from '@playwright/test';

/**
 * ログインヘルパー
 */
export async function login(page: Page, email: string, password: string) {
  await page.goto('/login');
  await page.fill('[data-testid="email"]', email);
  await page.fill('[data-testid="password"]', password);
  await page.click('[data-testid="login-button"]');

  // ログイン完了待機
  const response = await page.waitForResponse(res =>
    res.url().includes('/api/auth/login') && res.status() === 200
  );
  const data = await response.json();
  return data.accessToken;
}

/**
 * ログアウトヘルパー
 */
export async function logout(page: Page) {
  await page.click('[data-testid="logout-button"]');
  await page.waitForResponse(res =>
    res.url().includes('/api/auth/logout') && res.status() === 200
  );
}

/**
 * 新規登録ヘルパー
 */
export async function register(page: Page, email: string, password: string, migrateGuestData = false) {
  await page.goto('/register');
  await page.fill('[data-testid="email"]', email);
  await page.fill('[data-testid="password"]', password);
  await page.fill('[data-testid="password-confirm"]', password);

  if (migrateGuestData) {
    await page.check('[data-testid="migrate-guest-data"]');
  }

  await page.click('[data-testid="register-button"]');

  const response = await page.waitForResponse(res =>
    res.url().includes('/api/auth/register') && res.status() === 201
  );
  const data = await response.json();
  return data.accessToken;
}
```

`tests/helpers/api-helper.ts`:

```typescript
import { APIRequestContext } from '@playwright/test';

/**
 * 命式計算APIヘルパー
 */
export async function calculateSaju(request: APIRequestContext, birthData: any) {
  const response = await request.post('/api/saju/calculate', {
    data: birthData
  });

  if (response.status() !== 200) {
    throw new Error(`命式計算APIエラー: ${response.status()}`);
  }

  return await response.json();
}

/**
 * 命式保存APIヘルパー
 */
export async function saveSaju(request: APIRequestContext, sajuData: any, token?: string) {
  const headers: any = {
    'Content-Type': 'application/json'
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await request.post('/api/saju/save', {
    data: sajuData,
    headers
  });

  if (response.status() !== 201) {
    throw new Error(`命式保存APIエラー: ${response.status()}`);
  }

  return await response.json();
}
```

---

## 連鎖テスト実装例

`tests/e2e/chain/CHAIN-001.spec.ts`:

```typescript
import { test, expect } from '@playwright/test';
import { testBirthData } from '../../fixtures/saju-test-data';

test.describe('CHAIN-001: 命式計算全体フロー', () => {
  test('正常系 - 男性、1990年3月15日14時30分生まれ', async ({ page }) => {
    const birthData = testBirthData.male1990;

    // 1. トップページにアクセス
    await page.goto('/');
    await expect(page).toHaveURL('/');

    // 2-5. 入力フォーム入力
    await page.fill('[data-testid="birth-date"]', '1990-03-15');
    await page.fill('[data-testid="birth-time"]', '14:30');
    await page.click('[data-testid="gender-male"]');
    await page.fill('[data-testid="name"]', birthData.name);

    // 6. 計算ボタンクリック
    await page.click('[data-testid="calculate-button"]');

    // 7. ローディングアニメーション確認
    await expect(page.locator('[data-testid="loading-animation"]')).toBeVisible();

    // API呼び出し確認: POST /api/saju/calculate
    const calculateResponse = await page.waitForResponse(res =>
      res.url().includes('/api/saju/calculate') && res.status() === 200
    );
    const sajuData = await calculateResponse.json();

    // レスポンス検証
    expect(sajuData.id).toBeTruthy();
    expect(sajuData.name).toBe(birthData.name);
    expect(sajuData.birthDatetime).toBe(birthData.birthDatetime);
    expect(sajuData.gender).toBe(birthData.gender);
    expect(sajuData.yearStem).toBe(birthData.expected.yearStem);
    expect(sajuData.yearBranch).toBe(birthData.expected.yearBranch);
    expect(sajuData.monthStem).toBe(birthData.expected.monthStem);
    expect(sajuData.monthBranch).toBe(birthData.expected.monthBranch);
    expect(sajuData.isForward).toBe(birthData.expected.isForward);
    expect(sajuData.daeunList).toBeInstanceOf(Array);
    expect(sajuData.daeunList.length).toBeGreaterThan(0);
    expect(['大吉', '吉', '平', '凶', '大凶']).toContain(sajuData.fortuneLevel);

    // 8. ローディング終了後、計算結果が表示される
    await expect(page.locator('[data-testid="loading-animation"]')).not.toBeVisible();
    await expect(page.locator('[data-testid="saju-result-section"]')).toBeVisible();

    // UI検証: 四柱表示
    await expect(page.locator('[data-testid="year-stem"]')).toContainText(birthData.expected.yearStem);
    await expect(page.locator('[data-testid="year-branch"]')).toContainText(birthData.expected.yearBranch);

    // 9. 保存ボタンクリック
    await page.click('[data-testid="save-button"]');

    // API呼び出し確認: POST /api/saju/save
    const saveResponse = await page.waitForResponse(res =>
      res.url().includes('/api/saju/save') && res.status() === 201
    );
    const saveData = await saveResponse.json();

    // 保存レスポンス検証
    expect(saveData.success).toBe(true);
    expect(saveData.id).toBe(sajuData.id);
    expect(saveData.message).toContain('保存しました');

    // 10. 保存成功メッセージ確認
    await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
    await expect(page.locator('[data-testid="success-message"]')).toContainText('保存しました');

    // 11. リダイレクト確認
    await expect(page).toHaveURL('/list');
  });

  test('正常系 - 女性、1995年6月20日10時15分生まれ', async ({ page }) => {
    const birthData = testBirthData.female1995;

    await page.goto('/');

    await page.fill('[data-testid="birth-date"]', '1995-06-20');
    await page.fill('[data-testid="birth-time"]', '10:15');
    await page.click('[data-testid="gender-female"]');
    await page.fill('[data-testid="name"]', birthData.name);

    await page.click('[data-testid="calculate-button"]');

    const calculateResponse = await page.waitForResponse(res =>
      res.url().includes('/api/saju/calculate') && res.status() === 200
    );
    const sajuData = await calculateResponse.json();

    expect(sajuData.yearStem).toBe(birthData.expected.yearStem);
    expect(sajuData.yearBranch).toBe(birthData.expected.yearBranch);
    expect(sajuData.isForward).toBe(birthData.expected.isForward);  // 女性 + 陰干 → 逆行

    await page.click('[data-testid="save-button"]');
    await expect(page).toHaveURL('/list');
  });

  test('異常系 - 範囲外の日付（1899年）', async ({ page }) => {
    await page.goto('/');

    await page.fill('[data-testid="birth-date"]', '1899-12-31');
    await page.fill('[data-testid="birth-time"]', '12:00');
    await page.click('[data-testid="gender-male"]');

    await page.click('[data-testid="calculate-button"]');

    // クライアント側バリデーションチェック
    await expect(page.locator('[data-testid="error-message"]')).toBeVisible();
    await expect(page.locator('[data-testid="error-message"]')).toContainText('1900-2109年の範囲内で入力してください');

    // API呼び出しが行われないことを確認
    let apiCalled = false;
    page.on('response', res => {
      if (res.url().includes('/api/saju/calculate')) {
        apiCalled = true;
      }
    });

    await page.waitForTimeout(2000);
    expect(apiCalled).toBe(false);
  });
});
```

---

## 単品テスト実装例

`tests/e2e/unit/auth-endpoints.spec.ts`:

```typescript
import { test, expect } from '@playwright/test';
import { testAuthData } from '../../fixtures/saju-test-data';

test.describe('認証API - 単品テスト', () => {
  test('POST /api/auth/login - 正常系', async ({ request }) => {
    const response = await request.post('/api/auth/login', {
      data: {
        email: testAuthData.validUser.email,
        password: testAuthData.validUser.password,
        rememberMe: true
      }
    });

    expect(response.status()).toBe(200);
    const data = await response.json();
    expect(data.accessToken).toBeTruthy();
    expect(data.refreshToken).toBeTruthy();
    expect(data.user.email).toBe(testAuthData.validUser.email);
    expect(data.user.role).toBe('user');
  });

  test('POST /api/auth/login - 異常系（パスワード間違い）', async ({ request }) => {
    const response = await request.post('/api/auth/login', {
      data: {
        email: testAuthData.validUser.email,
        password: 'WrongPassword123!'
      }
    });

    expect(response.status()).toBe(401);
    const data = await response.json();
    expect(data.error).toContain('正しくありません');
  });

  test('POST /api/auth/register - 正常系', async ({ request }) => {
    const response = await request.post('/api/auth/register', {
      data: {
        email: testAuthData.newUser.email,
        password: testAuthData.newUser.password,
        migrateGuestData: false
      }
    });

    expect(response.status()).toBe(201);
    const data = await response.json();
    expect(data.accessToken).toBeTruthy();
    expect(data.user.role).toBe('user');
  });
});
```

---

## 実行コマンド

```bash
# すべてのテストを実行
npx playwright test

# 連鎖テストのみ実行
npx playwright test tests/e2e/chain/

# 単品テストのみ実行
npx playwright test tests/e2e/unit/

# 特定のテストファイルを実行
npx playwright test tests/e2e/chain/CHAIN-001.spec.ts

# UIモードで実行（デバッグ用）
npx playwright test --ui

# デバッグモードで実行
npx playwright test --debug

# ヘッドレスモードをOFFにして実行
npx playwright test --headed

# HTMLレポート生成
npx playwright test --reporter=html
npx playwright show-report
```

---

**作成日**: 2025年11月2日
**バージョン**: 1.0
**テストツール**: Playwright
