# ゴールデン四柱推命アプリケーション - E2Eテストプラン

## テスト戦略の概要

このドキュメントは、ゴールデン四柱推命アプリケーションの統合テスト・E2Eテスト戦略を定義します。バックエンド実装完了後、実際のユーザーフローに基づいた包括的なテストを実施し、品質を保証します。

| 項目 | 内容 |
|-----|------|
| プロジェクト名 | ゴールデン四柱推命アプリケーション |
| テスト種別 | E2Eテスト（エンドツーエンドテスト） |
| テストツール | Playwright |
| テスト環境 | ローカル開発環境、ステージング環境、本番環境 |
| 作成日 | 2025年11月2日 |
| バージョン | 1.0 |

## テストツール選定

### Playwright採用理由

1. **クロスブラウザ対応**: Chromium、Firefox、WebKitを同時にテスト可能
2. **自動待機機能**: 要素が表示されるまで自動的に待機
3. **強力なセレクター**: data-testid、text、role等の多様なセレクター
4. **並列実行**: 複数テストケースを並列実行可能
5. **API検証**: ネットワークリクエスト/レスポンスを検証可能
6. **スクリーンショット**: 失敗時の画面キャプチャ自動保存
7. **TypeScript完全対応**: 型安全なテストコード

### インストール

```bash
cd frontend
npm install -D @playwright/test
npx playwright install
```

### 設定ファイル

`frontend/playwright.config.ts`:

```typescript
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  timeout: 30000,
  retries: 2,
  workers: 4,
  use: {
    baseURL: 'http://localhost:3247',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { browserName: 'chromium' },
    },
    {
      name: 'firefox',
      use: { browserName: 'firefox' },
    },
    {
      name: 'webkit',
      use: { browserName: 'webkit' },
    },
  ],
  webServer: {
    command: 'npm run dev',
    port: 3247,
    reuseExistingServer: !process.env.CI,
  },
});
```

## テスト環境設定

### 環境別設定

| 環境 | フロントエンド | バックエンド | データベース | 用途 |
|------|--------------|-------------|-------------|------|
| ローカル | http://localhost:3247 | http://localhost:8432 | PostgreSQL (ローカル) | 開発・デバッグ |
| ステージング | https://staging.goldensaju.app | https://api-staging.goldensaju.app | PostgreSQL (Neon - staging) | 統合テスト |
| 本番 | https://goldensaju.app | https://api.goldensaju.app | PostgreSQL (Neon - prod) | 受入テスト |

### 環境変数

`.env.test`:

```bash
# テスト環境設定
VITE_API_URL=http://localhost:8432/api
TEST_USER_EMAIL=test@goldensaju.local
TEST_USER_PASSWORD=TestGoldenSaju2025!
TEST_BIRTH_DATA_1_DATE=1990-03-15
TEST_BIRTH_DATA_1_TIME=14:30:00
TEST_BIRTH_DATA_1_GENDER=male
TEST_BIRTH_DATA_1_NAME=テスト太郎
TEST_BIRTH_DATA_2_DATE=1995-06-20
TEST_BIRTH_DATA_2_TIME=10:15:00
TEST_BIRTH_DATA_2_GENDER=female
TEST_BIRTH_DATA_2_NAME=テスト花子
```

## テストデータ準備

### テストユーザー

| ID | メール | パスワード | 権限 | 用途 |
|----|--------|----------|------|------|
| 1 | test@goldensaju.local | TestGoldenSaju2025! | user | 基本テスト |
| 2 | admin@goldensaju.local | AdminGoldenSaju2025! | admin | 管理者機能テスト |

### テスト命式データ

| ID | 名前 | 生年月日 | 時刻 | 性別 | 期待される結果 |
|----|------|---------|------|------|--------------|
| 1 | テスト太郎 | 1990-03-15 | 14:30 | male | 年柱: 庚午、月柱: 己卯、大運数: 7個、順行 |
| 2 | テスト花子 | 1995-06-20 | 10:15 | female | 年柱: 乙亥、月柱: 壬午、大運数: 7個、逆行 |
| 3 | エッジケース | 1900-01-01 | 00:00 | male | 範囲最小値（1900年） |
| 4 | エッジケース | 2109-12-31 | 23:59 | female | 範囲最大値（2109年） |

### 210年節気DBテストデータ

- **データソース**: `solar_terms_1900_2109_JIEQI_ONLY.json`
- **範囲**: 1900年〜2109年
- **節気数**: 2,520個（年12節気 × 210年）
- **精度**: 秒レベル

## テスト分類

### 1. 連鎖テスト（API連鎖テスト）

複数のAPIエンドポイントを連鎖的に呼び出すユーザーフローをテストします。

| 連鎖テストID | スライス名 | エンドポイント連鎖 | 優先度 |
|------------|---------|------------------|--------|
| CHAIN-001 | 命式計算全体フロー | 1.1→1.2 | 最高 |
| CHAIN-002 | 水平スクロール運勢表示 | 1.1→3.1→3.2→3.3→3.4→3.5 | 最高 |
| CHAIN-003 | インタラクティブ運勢選択 | 3.2→3.3→3.4→3.5 | 高 |
| CHAIN-004 | ゲスト→ログイン移行 | 5.2→5.3→2.1 | 高 |
| CHAIN-005 | データ管理統合 | 2.1→2.2→4.2 | 中 |

### 2. 単品エンドポイントテスト

個別のAPIエンドポイントの動作を検証します。

| テスト種別 | 対象エンドポイント数 | 説明 |
|----------|------------------|------|
| 認証API | 4 | login, register, logout, me |
| 命式計算・保存API | 2 | calculate, save |
| 命式リスト・削除API | 2 | list, delete |
| 命式詳細API | 3 | detail, daeun, current |
| 年月日運API | 3 | year, month, day |
| 設定・データ管理API | 4 | password, export, import, settings |
| データ移行API | 1 | migrate |

### 3. UI/UXテスト

- ローディングアニメーション（golden-peppa）表示
- 五行カラーシステム適用
- 吉凶アイコン表示
- レスポンシブデザイン（モバイル/タブレット/PC）
- アクセシビリティ（ARIA属性、キーボードナビゲーション）

### 4. パフォーマンステスト

- 命式計算API応答時間: 2秒以内
- 命式保存API応答時間: 1秒以内
- ページロード時間: 3秒以内
- 水平スクロールのフレームレート: 60fps

## テストシナリオ構成

### 正常系テスト

- 標準的な入力値での動作確認
- 期待される結果との一致確認
- 画面遷移の正確性確認

### 異常系テスト

- 範囲外の日付入力（1899年、2110年）
- 未入力フィールド
- 不正な形式のデータ
- ネットワークエラー時の挙動
- 認証エラー時の挙動

### エッジケーステスト

- 境界値テスト（1900-01-01、2109-12-31）
- 最大・最小値テスト
- 特殊文字入力
- 長文入力

## CI/CD統合方針

### GitHub Actions統合

`.github/workflows/e2e-tests.yml`:

```yaml
name: E2E Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: |
          cd frontend
          npm ci

      - name: Install Playwright browsers
        run: |
          cd frontend
          npx playwright install --with-deps

      - name: Start backend (Docker)
        run: docker-compose up -d

      - name: Wait for backend
        run: |
          timeout 60 bash -c 'until curl -f http://localhost:8432/health; do sleep 2; done'

      - name: Run E2E tests
        run: |
          cd frontend
          npx playwright test

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: frontend/playwright-report/

      - name: Stop backend
        if: always()
        run: docker-compose down
```

### テスト実行トリガー

- **Pull Request**: すべての連鎖テスト実行
- **Merge to main**: すべての連鎖テスト + 単品テスト実行
- **Nightly Build**: すべてのテスト + パフォーマンステスト実行

## 品質ゲート基準

### テスト成功率

| テスト種別 | 必須成功率 | 目標成功率 |
|----------|----------|----------|
| 連鎖テスト（最高優先度） | 100% | 100% |
| 連鎖テスト（高優先度） | 95% | 100% |
| 連鎖テスト（中優先度） | 90% | 100% |
| 単品エンドポイントテスト | 95% | 100% |
| UI/UXテスト | 90% | 100% |
| パフォーマンステスト | 80% | 100% |

### カバレッジ基準

| カテゴリ | 最低カバレッジ | 目標カバレッジ |
|---------|-------------|-------------|
| APIエンドポイント | 95% | 100% |
| ユーザーストーリー | 100% | 100% |
| 正常系シナリオ | 100% | 100% |
| 異常系シナリオ | 80% | 100% |

### パフォーマンス基準

| 指標 | 閾値 | 理想値 |
|------|-----|-------|
| 命式計算API応答時間 | 2秒 | 1秒 |
| 命式保存API応答時間 | 1秒 | 500ms |
| ページロード時間 | 3秒 | 2秒 |
| First Contentful Paint | 1.5秒 | 1秒 |
| Time to Interactive | 3秒 | 2秒 |

## テスト実行計画

### Phase 1: 基本機能テスト（最高優先度）

**期間**: バックエンド実装完了後 1週間

- CHAIN-001: 命式計算全体フロー
- CHAIN-002: 水平スクロール運勢表示
- 命式計算・保存API単品テスト

**成功基準**: すべてのテストケースが100%成功

### Phase 2: 統合機能テスト（高優先度）

**期間**: Phase 1完了後 1週間

- CHAIN-003: インタラクティブ運勢選択
- CHAIN-004: ゲスト→ログイン移行
- 認証API単品テスト
- 命式詳細API単品テスト

**成功基準**: すべてのテストケースが95%以上成功

### Phase 3: 全機能テスト（中優先度）

**期間**: Phase 2完了後 1週間

- CHAIN-005: データ管理統合
- 設定・データ管理API単品テスト
- UI/UXテスト
- パフォーマンステスト

**成功基準**: すべてのテストケースが90%以上成功

## テスト実装ガイドライン

### data-testid命名規則

```typescript
// ボタン: [機能名]-button
<button data-testid="calculate-button">計算する</button>

// 入力フィールド: [フィールド名]
<input data-testid="birth-date" />

// 表示エリア: [エリア名]-section
<div data-testid="saju-result-section">...</div>

// リスト項目: [リスト名]-item-[id]
<div data-testid="saju-list-item-123">...</div>

// ローディング: loading-animation
<div data-testid="loading-animation">...</div>
```

### APIモック戦略

**開発環境**: モックサービスを使用

```typescript
// frontend/src/services/mockSajuService.ts
export const mockCalculate = async (data: BirthDataRequest): Promise<SajuResponse> => {
  // モックデータを返す
};
```

**E2Eテスト環境**: 実際のAPIを使用

```typescript
// tests/e2e/CHAIN-001.spec.ts
test('CHAIN-001: 命式計算全体フロー', async ({ page }) => {
  // 実際のAPIエンドポイントにリクエスト
  const response = await page.waitForResponse(res =>
    res.url().includes('/api/saju/calculate') && res.status() === 200
  );
});
```

### エラーハンドリングテスト

```typescript
test('異常系 - ネットワークエラー', async ({ page }) => {
  // ネットワークをオフラインにする
  await page.route('**/api/**', route => route.abort('failed'));

  await page.goto('/');
  await page.fill('[data-testid="birth-date"]', '1990-03-15');
  await page.click('[data-testid="calculate-button"]');

  // エラーメッセージが表示されることを確認
  await expect(page.locator('[data-testid="error-message"]')).toBeVisible();
  await expect(page.locator('[data-testid="error-message"]')).toContainText('ネットワークエラー');
});
```

## セキュリティテスト

### XSS脆弱性テスト

```typescript
test('セキュリティ - XSS脆弱性チェック', async ({ page }) => {
  await page.goto('/');

  // 悪意のあるスクリプトを入力
  await page.fill('[data-testid="name"]', '<script>alert("XSS")</script>');
  await page.click('[data-testid="calculate-button"]');

  // スクリプトが実行されないことを確認
  const alerts = [];
  page.on('dialog', dialog => {
    alerts.push(dialog.message());
    dialog.dismiss();
  });

  await page.waitForTimeout(1000);
  expect(alerts).toHaveLength(0);
});
```

### SQLインジェクション対策テスト

```typescript
test('セキュリティ - SQLインジェクション対策', async ({ page }) => {
  await page.goto('/login');

  // SQLインジェクションを試みる
  await page.fill('[data-testid="email"]', "admin' OR '1'='1");
  await page.fill('[data-testid="password"]', "password' OR '1'='1");
  await page.click('[data-testid="login-button"]');

  // ログイン失敗することを確認
  await expect(page.locator('[data-testid="error-message"]')).toBeVisible();
});
```

### CSRF対策テスト

```typescript
test('セキュリティ - CSRF対策', async ({ page }) => {
  // ログイン状態でトークンなしリクエストを送信
  const response = await page.request.post('/api/saju/save', {
    data: { /* ... */ },
    headers: {
      // CSRFトークンを含めない
    }
  });

  // 403 Forbiddenが返されることを確認
  expect(response.status()).toBe(403);
});
```

## レポーティング

### テスト結果レポート

Playwrightは自動的にHTML形式のレポートを生成します。

```bash
npx playwright show-report
```

**レポート内容**:
- テストケース実行結果（成功/失敗）
- 実行時間
- スクリーンショット（失敗時）
- ビデオ録画（失敗時）
- ネットワークログ
- コンソールログ

### CI/CD統合レポート

GitHub Actionsでテスト結果をコメントとして表示：

```yaml
- name: Comment PR with test results
  uses: daun/playwright-report-comment@v3
  with:
    report-path: frontend/playwright-report/
```

## テストメンテナンス

### 定期レビュー

- **週次**: テスト失敗原因の分析
- **月次**: テストカバレッジレビュー
- **四半期**: テスト戦略見直し

### テストデータ更新

- 新機能追加時: テストケース追加
- バグ修正時: リグレッションテスト追加
- API変更時: テストケース更新

## 次のステップ

1. 各連鎖テストのE2E仕様書確認
2. 単品エンドポイントテスト仕様書確認
3. Playwright実装例確認
4. バックエンド実装開始
5. E2Eテスト実装開始

---

**作成日**: 2025年11月2日
**バージョン**: 1.0
**プロジェクト**: ゴールデン四柱推命アプリケーション
**テストツール**: Playwright
**ステータス**: 策定完了
