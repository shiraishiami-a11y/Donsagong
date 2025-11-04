# CHAIN-004: ゲスト→ログイン移行 - E2Eテスト仕様書

## テスト概要

| 項目 | 内容 |
|-----|------|
| 連鎖テストID | CHAIN-004 |
| スライス名 | ゲスト→ログイン移行 |
| ユーザーストーリー | ゲストモードで保存したデータをログイン時にクラウドに移行する |
| エンドポイント連鎖 | 5.2 → 5.3 → 2.1 |
| 外部依存 | PostgreSQL、JWT認証 |
| 実装優先度 | 高 |
| 対応ページ | P-AUTH-2（新規登録ページ） |
| テストツール | Playwright |
| 作成日 | 2025年11月2日 |
| バージョン | 1.0 |

## エンドポイント連鎖詳細

| ステップ | エンドポイント | HTTPメソッド | 説明 |
|---------|--------------|-------------|------|
| 1 | `/api/auth/register` | POST | 新規登録（アカウント作成） |
| 2 | `/api/saju/migrate` | POST | ゲストデータ移行（LocalStorage → PostgreSQL） |
| 3 | `/api/saju/list` | GET | 移行後の命式一覧取得（確認） |

## 前提条件

- ゲストモードで複数の命式が LocalStorage に保存されている
- ユーザーが新規登録ページ (`/register`) にアクセス
- PostgreSQL データベースが稼働している

## テストシナリオ

### シナリオ1: 正常系 - ゲストデータ移行成功

**目的**: ゲストモードで保存した命式データがログイン時にクラウドに移行されることを確認

#### 事前準備

```typescript
// LocalStorageにテストデータを保存
const testSajuData = [
  {
    id: 'guest-saju-001',
    name: 'ゲストテスト太郎',
    birthDatetime: '1990-03-15T14:30:00+09:00',
    gender: 'male',
    // ... その他のフィールド
  },
  {
    id: 'guest-saju-002',
    name: 'ゲストテスト花子',
    birthDatetime: '1995-06-20T10:15:00+09:00',
    gender: 'female',
    // ... その他のフィールド
  }
];
localStorage.setItem('saju_data', JSON.stringify(testSajuData));
```

#### ステップ

1. 新規登録ページ (`/register`) にアクセス
2. メールアドレス入力: `test@example.com`
3. パスワード入力: `TestPassword123!`
4. パスワード確認入力: `TestPassword123!`
5. 「ゲストデータを移行する」チェックボックスにチェック
6. 「新規登録」ボタンをクリック
7. 登録成功メッセージ確認
8. データ移行中のローディングアニメーション確認
9. データ移行成功メッセージ確認
10. 命式リストページ (`/list`) にリダイレクト
11. 移行されたデータが表示されることを確認

#### 期待結果

**ステップ6: POST /api/auth/register**
- HTTPステータス: `201 Created`
- レスポンス型: `AuthResponse`
- 検証項目:
  - ✅ `accessToken`: JWT形式の文字列
  - ✅ `refreshToken`: JWT形式の文字列
  - ✅ `user.id`: UUID形式
  - ✅ `user.email`: "test@example.com"
  - ✅ `user.role`: "user"

**ステップ8: POST /api/saju/migrate**
- HTTPステータス: `201 Created`
- レスポンス型: `MigrateResponse`
- 検証項目:
  - ✅ `success`: `true`
  - ✅ `migratedCount`: 2（LocalStorageに2件保存されていた場合）
  - ✅ `message`: "2件の命式データを移行しました"

**ステップ10: GET /api/saju/list**
- HTTPステータス: `200 OK`
- レスポンス型: `Array<SajuSummary>`
- 検証項目:
  - ✅ 配列長さ: 2
  - ✅ 各要素が移行前のデータと一致
  - ✅ `id` は新しいUUIDに変換されている（`guest-saju-001` → `saju-xxxxxxxx`）

**UI検証**:
- ✅ 登録成功メッセージ表示: "アカウント作成が完了しました"
- ✅ データ移行中のローディングアニメーション表示
- ✅ データ移行成功メッセージ表示: "2件の命式データを移行しました"
- ✅ `/list` ページにリダイレクト
- ✅ 移行されたデータが一覧に表示される
- ✅ LocalStorage が空になっている（`localStorage.getItem('saju_data') === null`）

#### Playwrightテストコード例

```typescript
import { test, expect } from '@playwright/test';

test('CHAIN-004-S1: 正常系 - ゲストデータ移行成功', async ({ page }) => {
  // 事前準備: LocalStorageにテストデータを保存
  await page.goto('/');
  await page.evaluate(() => {
    const testSajuData = [
      {
        id: 'guest-saju-001',
        name: 'ゲストテスト太郎',
        birthDatetime: '1990-03-15T14:30:00+09:00',
        gender: 'male',
        yearStem: '庚',
        yearBranch: '午',
        // ... 省略
      },
      {
        id: 'guest-saju-002',
        name: 'ゲストテスト花子',
        birthDatetime: '1995-06-20T10:15:00+09:00',
        gender: 'female',
        yearStem: '乙',
        yearBranch: '亥',
        // ... 省略
      }
    ];
    localStorage.setItem('saju_data', JSON.stringify(testSajuData));
  });

  // 1. 新規登録ページにアクセス
  await page.goto('/register');

  // 2-5. 入力フォーム
  await page.fill('[data-testid="email"]', 'test@example.com');
  await page.fill('[data-testid="password"]', 'TestPassword123!');
  await page.fill('[data-testid="password-confirm"]', 'TestPassword123!');
  await page.check('[data-testid="migrate-guest-data"]');

  // 6. 新規登録ボタンクリック
  await page.click('[data-testid="register-button"]');

  // 7. 登録API呼び出し確認
  const registerResponse = await page.waitForResponse(res =>
    res.url().includes('/api/auth/register') && res.status() === 201
  );
  const authData = await registerResponse.json();

  // レスポンス検証
  expect(authData.accessToken).toBeTruthy();
  expect(authData.refreshToken).toBeTruthy();
  expect(authData.user.email).toBe('test@example.com');
  expect(authData.user.role).toBe('user');

  // 8. データ移行中のローディング確認
  await expect(page.locator('[data-testid="migration-loading"]')).toBeVisible();

  // 9. データ移行API呼び出し確認
  const migrateResponse = await page.waitForResponse(res =>
    res.url().includes('/api/saju/migrate') && res.status() === 201
  );
  const migrateData = await migrateResponse.json();

  // レスポンス検証
  expect(migrateData.success).toBe(true);
  expect(migrateData.migratedCount).toBe(2);
  expect(migrateData.message).toContain('2件');

  // 10. データ移行成功メッセージ確認
  await expect(page.locator('[data-testid="migration-success-message"]')).toBeVisible();
  await expect(page.locator('[data-testid="migration-success-message"]')).toContainText('2件の命式データを移行しました');

  // 11. リダイレクト確認
  await expect(page).toHaveURL('/list');

  // 12. 命式一覧API呼び出し確認
  const listResponse = await page.waitForResponse(res =>
    res.url().includes('/api/saju/list') && res.status() === 200
  );
  const listData = await listResponse.json();

  // レスポンス検証
  expect(listData).toHaveLength(2);
  expect(listData[0].name).toBe('ゲストテスト太郎');
  expect(listData[1].name).toBe('ゲストテスト花子');

  // 13. LocalStorageが空になっていることを確認
  const localStorageData = await page.evaluate(() => {
    return localStorage.getItem('saju_data');
  });
  expect(localStorageData).toBeNull();

  // 14. UI検証: 一覧に表示されることを確認
  await expect(page.locator('[data-testid="saju-list-item"]')).toHaveCount(2);
});
```

---

### シナリオ2: 正常系 - ゲストデータなしで新規登録

**目的**: ゲストデータがない場合でも正常に新規登録できることを確認

#### ステップ

1. LocalStorageをクリア
2. 新規登録ページにアクセス
3. メールアドレス・パスワード入力
4. 「新規登録」ボタンをクリック
5. データ移行が実行されないことを確認
6. 命式リストページに移動
7. 空の一覧が表示されることを確認

#### 期待結果

- ✅ 登録成功（`201 Created`）
- ✅ データ移行APIは呼び出されない
- ✅ `/list` ページにリダイレクト
- ✅ 空の一覧が表示される

#### Playwrightテストコード例

```typescript
test('CHAIN-004-S2: 正常系 - ゲストデータなしで新規登録', async ({ page }) => {
  // LocalStorageをクリア
  await page.goto('/');
  await page.evaluate(() => localStorage.clear());

  await page.goto('/register');

  await page.fill('[data-testid="email"]', 'newuser@example.com');
  await page.fill('[data-testid="password"]', 'NewPassword123!');
  await page.fill('[data-testid="password-confirm"]', 'NewPassword123!');

  await page.click('[data-testid="register-button"]');

  // 登録API呼び出し確認
  const registerResponse = await page.waitForResponse(res =>
    res.url().includes('/api/auth/register') && res.status() === 201
  );
  expect(registerResponse.status()).toBe(201);

  // データ移行APIが呼び出されないことを確認
  let migrateApiCalled = false;
  page.on('response', res => {
    if (res.url().includes('/api/saju/migrate')) {
      migrateApiCalled = true;
    }
  });

  await page.waitForTimeout(2000); // 2秒待機
  expect(migrateApiCalled).toBe(false);

  // リダイレクト確認
  await expect(page).toHaveURL('/list');

  // 空の一覧表示確認
  await expect(page.locator('[data-testid="empty-list-message"]')).toBeVisible();
});
```

---

### シナリオ3: 正常系 - データ移行チェックボックスOFFで新規登録

**目的**: ゲストデータがあっても、チェックボックスOFFなら移行しないことを確認

#### ステップ

1. LocalStorageにテストデータを保存
2. 新規登録ページにアクセス
3. メールアドレス・パスワード入力
4. 「ゲストデータを移行する」チェックボックスをOFF
5. 「新規登録」ボタンをクリック
6. データ移行が実行されないことを確認
7. LocalStorageがクリアされないことを確認

#### 期待結果

- ✅ 登録成功
- ✅ データ移行APIは呼び出されない
- ✅ LocalStorageはそのまま残る

---

### シナリオ4: 異常系 - データ移行中にエラー発生

**目的**: データ移行APIがエラーを返した場合のエラーハンドリング確認

#### ステップ

1. LocalStorageにテストデータを保存
2. 新規登録ページにアクセス
3. メールアドレス・パスワード入力
4. 「ゲストデータを移行する」チェックボックスにチェック
5. データ移行APIを強制的にエラーにする（モック）
6. 「新規登録」ボタンをクリック
7. エラーメッセージが表示されることを確認
8. LocalStorageはそのまま残ることを確認

#### 期待結果

- ✅ 登録成功（アカウントは作成される）
- ✅ データ移行失敗のエラーメッセージ表示
- ✅ LocalStorageはクリアされない（データ保護）
- ✅ ユーザーは後で再度移行を試みることができる

#### Playwrightテストコード例

```typescript
test('CHAIN-004-S4: 異常系 - データ移行中にエラー発生', async ({ page }) => {
  // LocalStorageにテストデータを保存
  await page.goto('/');
  await page.evaluate(() => {
    const testSajuData = [{ id: 'guest-saju-001', name: 'テスト' }];
    localStorage.setItem('saju_data', JSON.stringify(testSajuData));
  });

  // データ移行APIを強制的にエラーにする
  await page.route('**/api/saju/migrate', route => {
    route.fulfill({
      status: 500,
      contentType: 'application/json',
      body: JSON.stringify({ error: 'データ移行中にエラーが発生しました' })
    });
  });

  await page.goto('/register');

  await page.fill('[data-testid="email"]', 'error-test@example.com');
  await page.fill('[data-testid="password"]', 'ErrorTest123!');
  await page.fill('[data-testid="password-confirm"]', 'ErrorTest123!');
  await page.check('[data-testid="migrate-guest-data"]');

  await page.click('[data-testid="register-button"]');

  // 登録は成功する
  await page.waitForResponse(res =>
    res.url().includes('/api/auth/register') && res.status() === 201
  );

  // エラーメッセージ表示確認
  await expect(page.locator('[data-testid="migration-error-message"]')).toBeVisible();
  await expect(page.locator('[data-testid="migration-error-message"]')).toContainText('データ移行中にエラーが発生しました');

  // LocalStorageが残っていることを確認
  const localStorageData = await page.evaluate(() => {
    return localStorage.getItem('saju_data');
  });
  expect(localStorageData).not.toBeNull();
});
```

---

### シナリオ5: 異常系 - 重複メールアドレスで登録

**目的**: 既に登録済みのメールアドレスで登録しようとした場合のエラーハンドリング確認

#### ステップ

1. 既に登録済みのメールアドレスで新規登録を試みる

#### 期待結果

- HTTPステータス: `400 Bad Request`
- エラーメッセージ: "このメールアドレスは既に登録されています"
- データ移行は実行されない

---

## トランザクション管理

**重要**: データ移行は全成功または全失敗（All or Nothing）

- すべてのゲストデータが正常に移行される
- または、1件でもエラーがあれば全体がロールバックされる
- 部分的な移行は許可されない

---

## パフォーマンス要件

| 指標 | 閾値 | 理想値 |
|------|-----|-------|
| 新規登録API応答時間 | 1秒以内 | 500ms以内 |
| データ移行API応答時間（10件） | 3秒以内 | 2秒以内 |
| データ移行API応答時間（100件） | 10秒以内 | 5秒以内 |

---

## 品質ゲート

CHAIN-004テストがすべて成功するための条件:

- ✅ エンドポイント連鎖（5.2 → 5.3 → 2.1）がすべて成功
- ✅ ゲストデータが正常に移行される
- ✅ 移行後に LocalStorage がクリアされる
- ✅ 移行後の命式一覧が正しく表示される
- ✅ エラー発生時に LocalStorage が保護される
- ✅ トランザクション管理が正常に動作（All or Nothing）

---

**作成日**: 2025年11月2日
**バージョン**: 1.0
**テストツール**: Playwright
**ステータス**: 未実装
**対応API仕様書**:
- `docs/api-specs/auth-api.md`
- `docs/api-specs/data-migration-api.md`
