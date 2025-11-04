# CHAIN-005: データ管理統合 - E2Eテスト仕様書

## テスト概要

| 項目 | 内容 |
|-----|------|
| 連鎖テストID | CHAIN-005 |
| スライス名 | データ管理統合 |
| ユーザーストーリー | 命式一覧・削除・エクスポートを統合的に管理する |
| エンドポイント連鎖 | 2.1 → 2.2 → 4.2 |
| 外部依存 | PostgreSQL、ファイルシステム |
| 実装優先度 | 中 |
| 対応ページ | P-002（命式リストページ）、P-004（設定ページ） |
| テストツール | Playwright |
| 作成日 | 2025年11月2日 |
| バージョン | 1.0 |

## エンドポイント連鎖詳細

| ステップ | エンドポイント | HTTPメソッド | 説明 |
|---------|--------------|-------------|------|
| 1 | `/api/saju/list` | GET | 命式一覧取得 |
| 2 | `/api/saju/{id}` | DELETE | 命式削除 |
| 3 | `/api/saju/export` | GET | データエクスポート（JSON形式） |

## 前提条件

- ユーザーがログインしている
- 複数の命式データが保存されている
- 命式リストページ (`/list`) にアクセス可能

## テストシナリオ

### シナリオ1: 正常系 - 命式一覧取得と表示

**目的**: 保存された命式一覧が正しく表示されることを確認

#### ステップ

1. ログイン済みユーザーで命式リストページ (`/list`) にアクセス
2. 命式一覧APIが呼び出されることを確認
3. 一覧に複数の命式が表示されることを確認
4. 各命式カードに以下が表示されることを確認:
   - 名前
   - 生年月日
   - 四柱プレビュー（年柱・月柱・日柱・時柱）
   - 吉凶レベル（アイコン・カラー）
   - 作成日時

#### 期待結果

**エンドポイント: GET /api/saju/list**
- HTTPステータス: `200 OK`
- レスポンス型: `Array<SajuSummary>`
- 検証項目:
  - ✅ 配列が返される
  - ✅ 各要素に `id`, `name`, `birthDatetime`, `gender`, `fortuneLevel`, `createdAt` が含まれる
  - ✅ 四柱データ（`yearStem`, `yearBranch`, `monthStem`, `monthBranch`, `dayStem`, `dayBranch`, `hourStem`, `hourBranch`）が含まれる

**UI検証**:
- ✅ 命式一覧が表示される
- ✅ 各カードに五行カラーが適用される
- ✅ 各カードに吉凶アイコンが表示される
- ✅ カードをクリックすると詳細ページ (`/detail/:id`) に遷移する

#### Playwrightテストコード例

```typescript
import { test, expect } from '@playwright/test';

test('CHAIN-005-S1: 正常系 - 命式一覧取得と表示', async ({ page }) => {
  // 前提: ログイン済み
  await page.goto('/login');
  await page.fill('[data-testid="email"]', 'test@goldensaju.local');
  await page.fill('[data-testid="password"]', 'TestGoldenSaju2025!');
  await page.click('[data-testid="login-button"]');
  await page.waitForResponse(res => res.url().includes('/api/auth/login') && res.status() === 200);

  // 1. 命式リストページにアクセス
  await page.goto('/list');

  // 2. 命式一覧API呼び出し確認
  const listResponse = await page.waitForResponse(res =>
    res.url().includes('/api/saju/list') && res.status() === 200
  );
  const listData = await listResponse.json();

  // レスポンス検証
  expect(listData).toBeInstanceOf(Array);
  expect(listData.length).toBeGreaterThan(0);
  expect(listData[0]).toHaveProperty('id');
  expect(listData[0]).toHaveProperty('name');
  expect(listData[0]).toHaveProperty('birthDatetime');
  expect(listData[0]).toHaveProperty('fortuneLevel');
  expect(listData[0]).toHaveProperty('yearStem');

  // 3. UI検証: 一覧表示
  await expect(page.locator('[data-testid="saju-list-container"]')).toBeVisible();
  const sajuCards = page.locator('[data-testid="saju-list-item"]');
  await expect(sajuCards).toHaveCount(listData.length);

  // 4. 各カード内容確認
  const firstCard = sajuCards.first();
  await expect(firstCard.locator('[data-testid="saju-name"]')).toBeVisible();
  await expect(firstCard.locator('[data-testid="birth-datetime"]')).toBeVisible();
  await expect(firstCard.locator('[data-testid="fortune-icon"]')).toBeVisible();
  await expect(firstCard.locator('[data-testid="year-stem"]')).toContainText(listData[0].yearStem);

  // 5. カードクリックで詳細ページ遷移
  await firstCard.click();
  await expect(page).toHaveURL(`/detail/${listData[0].id}`);
});
```

---

### シナリオ2: 正常系 - 命式削除

**目的**: 命式を削除すると一覧から削除されることを確認

#### ステップ

1. 命式リストページにアクセス
2. 削除したい命式の削除ボタンをクリック
3. 削除確認ダイアログが表示されることを確認
4. 「削除する」ボタンをクリック
5. 削除APIが呼び出されることを確認
6. 削除成功メッセージが表示されることを確認
7. 一覧から削除された命式が消えることを確認

#### 期待結果

**エンドポイント: DELETE /api/saju/{id}**
- HTTPステータス: `200 OK`
- レスポンス型: `DeleteResponse`
- 検証項目:
  - ✅ `success`: `true`
  - ✅ `message`: "命式を削除しました"

**UI検証**:
- ✅ 削除確認ダイアログが表示される
- ✅ 削除成功メッセージが表示される
- ✅ 一覧から削除された命式が消える
- ✅ 一覧が自動的に再読み込みされる

#### Playwrightテストコード例

```typescript
test('CHAIN-005-S2: 正常系 - 命式削除', async ({ page }) => {
  // 前提: ログイン＋命式リストページにアクセス
  await page.goto('/login');
  await page.fill('[data-testid="email"]', 'test@goldensaju.local');
  await page.fill('[data-testid="password"]', 'TestGoldenSaju2025!');
  await page.click('[data-testid="login-button"]');

  await page.goto('/list');
  const listResponse = await page.waitForResponse(res =>
    res.url().includes('/api/saju/list') && res.status() === 200
  );
  const listDataBefore = await listResponse.json();
  const countBefore = listDataBefore.length;
  const targetSajuId = listDataBefore[0].id;

  // 2. 削除ボタンクリック
  await page.click(`[data-testid="delete-button-${targetSajuId}"]`);

  // 3. 削除確認ダイアログ表示
  await expect(page.locator('[data-testid="delete-confirm-dialog"]')).toBeVisible();

  // 4. 削除確認
  await page.click('[data-testid="confirm-delete-button"]');

  // 5. 削除API呼び出し確認
  const deleteResponse = await page.waitForResponse(res =>
    res.url().includes(`/api/saju/${targetSajuId}`) &&
    res.request().method() === 'DELETE' &&
    res.status() === 200
  );
  const deleteData = await deleteResponse.json();

  // レスポンス検証
  expect(deleteData.success).toBe(true);
  expect(deleteData.message).toContain('削除しました');

  // 6. 削除成功メッセージ確認
  await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
  await expect(page.locator('[data-testid="success-message"]')).toContainText('削除しました');

  // 7. 一覧から削除された命式が消えることを確認
  await page.waitForTimeout(500); // UI更新待機

  // 一覧再取得
  const listResponseAfter = await page.waitForResponse(res =>
    res.url().includes('/api/saju/list') && res.status() === 200
  );
  const listDataAfter = await listResponseAfter.json();
  const countAfter = listDataAfter.length;

  expect(countAfter).toBe(countBefore - 1);
  expect(listDataAfter.find(s => s.id === targetSajuId)).toBeUndefined();
});
```

---

### シナリオ3: 正常系 - データエクスポート

**目的**: 保存された命式データをJSON形式でエクスポートできることを確認

#### ステップ

1. 設定ページ (`/settings`) にアクセス
2. 「データをエクスポート」ボタンをクリック
3. エクスポートAPIが呼び出されることを確認
4. JSONファイルがダウンロードされることを確認
5. ダウンロードされたJSONファイルの内容を確認

#### 期待結果

**エンドポイント: GET /api/saju/export**
- HTTPステータス: `200 OK`
- Content-Type: `application/json`
- レスポンス型: `Array<SajuResponse>`
- 検証項目:
  - ✅ 全ての命式データが含まれる
  - ✅ 各命式に完全なデータ（四柱、大運リスト等）が含まれる
  - ✅ JSON形式で正しくパースできる

**UI検証**:
- ✅ エクスポートボタンをクリックするとファイルがダウンロードされる
- ✅ ファイル名が `saju_export_YYYYMMDD.json` 形式である
- ✅ ダウンロード成功メッセージが表示される

#### Playwrightテストコード例

```typescript
test('CHAIN-005-S3: 正常系 - データエクスポート', async ({ page }) => {
  // 前提: ログイン＋設定ページにアクセス
  await page.goto('/login');
  await page.fill('[data-testid="email"]', 'test@goldensaju.local');
  await page.fill('[data-testid="password"]', 'TestGoldenSaju2025!');
  await page.click('[data-testid="login-button"]');

  await page.goto('/settings');

  // ダウンロード待機設定
  const downloadPromise = page.waitForEvent('download');

  // 2. エクスポートボタンクリック
  await page.click('[data-testid="export-button"]');

  // 3. エクスポートAPI呼び出し確認
  const exportResponse = await page.waitForResponse(res =>
    res.url().includes('/api/saju/export') && res.status() === 200
  );
  const exportData = await exportResponse.json();

  // レスポンス検証
  expect(exportData).toBeInstanceOf(Array);
  expect(exportData.length).toBeGreaterThan(0);
  expect(exportData[0]).toHaveProperty('id');
  expect(exportData[0]).toHaveProperty('daeunList');

  // 4. ダウンロード確認
  const download = await downloadPromise;
  const filename = download.suggestedFilename();
  expect(filename).toMatch(/saju_export_\d{8}\.json/);

  // 5. ダウンロードされたファイル内容確認
  const path = await download.path();
  const fs = require('fs');
  const fileContent = fs.readFileSync(path, 'utf-8');
  const parsedData = JSON.parse(fileContent);

  expect(parsedData).toEqual(exportData);

  // UI検証: 成功メッセージ
  await expect(page.locator('[data-testid="export-success-message"]')).toBeVisible();
});
```

---

### シナリオ4: 正常系 - 連鎖テスト（一覧→削除→エクスポート）

**目的**: 一覧取得→削除→エクスポートの一連の流れが正常に動作することを確認

#### ステップ

1. 命式リストページにアクセス（一覧取得）
2. 1件削除
3. 設定ページに移動
4. データエクスポート
5. エクスポートされたデータに削除した命式が含まれていないことを確認

#### 期待結果

- ✅ 一覧取得成功
- ✅ 削除成功
- ✅ エクスポート成功
- ✅ エクスポートデータに削除した命式が含まれていない

#### Playwrightテストコード例

```typescript
test('CHAIN-005-S4: 正常系 - 連鎖テスト（一覧→削除→エクスポート）', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[data-testid="email"]', 'test@goldensaju.local');
  await page.fill('[data-testid="password"]', 'TestGoldenSaju2025!');
  await page.click('[data-testid="login-button"]');

  // 1. 一覧取得
  await page.goto('/list');
  const listResponse1 = await page.waitForResponse(res =>
    res.url().includes('/api/saju/list') && res.status() === 200
  );
  const listData1 = await listResponse1.json();
  const targetSajuId = listData1[0].id;

  // 2. 削除
  await page.click(`[data-testid="delete-button-${targetSajuId}"]`);
  await page.click('[data-testid="confirm-delete-button"]');
  await page.waitForResponse(res =>
    res.url().includes(`/api/saju/${targetSajuId}`) &&
    res.request().method() === 'DELETE' &&
    res.status() === 200
  );

  // 3. 設定ページに移動
  await page.goto('/settings');

  // 4. エクスポート
  const downloadPromise = page.waitForEvent('download');
  await page.click('[data-testid="export-button"]');

  const exportResponse = await page.waitForResponse(res =>
    res.url().includes('/api/saju/export') && res.status() === 200
  );
  const exportData = await exportResponse.json();

  // 5. エクスポートデータに削除した命式が含まれていないことを確認
  expect(exportData.find(s => s.id === targetSajuId)).toBeUndefined();
  expect(exportData.length).toBe(listData1.length - 1);
});
```

---

### シナリオ5: 異常系 - 存在しない命式の削除

**目的**: 存在しない命式IDで削除しようとした場合のエラーハンドリング確認

#### ステップ

1. 存在しない命式IDで削除APIを呼び出す

#### 期待結果

- HTTPステータス: `404 Not Found`
- エラーメッセージ: "命式が見つかりません"

#### Playwrightテストコード例

```typescript
test('CHAIN-005-S5: 異常系 - 存在しない命式の削除', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[data-testid="email"]', 'test@goldensaju.local');
  await page.fill('[data-testid="password"]', 'TestGoldenSaju2025!');
  await page.click('[data-testid="login-button"]');

  // 直接APIを呼び出し
  const response = await page.request.delete('/api/saju/nonexistent-id');

  expect(response.status()).toBe(404);
  const errorData = await response.json();
  expect(errorData.error).toContain('見つかりません');
});
```

---

### シナリオ6: 異常系 - 空の一覧表示

**目的**: 命式データが0件の場合に空の一覧が表示されることを確認

#### ステップ

1. 全ての命式を削除
2. 命式リストページにアクセス
3. 空の一覧メッセージが表示されることを確認

#### 期待結果

- HTTPステータス: `200 OK`
- レスポンス: `[]`（空配列）
- UI: "まだ命式が保存されていません" メッセージ表示

#### Playwrightテストコード例

```typescript
test('CHAIN-005-S6: 異常系 - 空の一覧表示', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[data-testid="email"]', 'newuser@goldensaju.local');
  await page.fill('[data-testid="password"]', 'NewUser123!');
  await page.click('[data-testid="login-button"]');

  await page.goto('/list');

  const listResponse = await page.waitForResponse(res =>
    res.url().includes('/api/saju/list') && res.status() === 200
  );
  const listData = await listResponse.json();

  expect(listData).toEqual([]);

  // UI検証: 空メッセージ表示
  await expect(page.locator('[data-testid="empty-list-message"]')).toBeVisible();
  await expect(page.locator('[data-testid="empty-list-message"]')).toContainText('まだ命式が保存されていません');
});
```

---

## パフォーマンス要件

| 指標 | 閾値 | 理想値 |
|------|-----|-------|
| 一覧取得API応答時間（10件） | 500ms以内 | 300ms以内 |
| 一覧取得API応答時間（100件） | 1秒以内 | 500ms以内 |
| 削除API応答時間 | 500ms以内 | 300ms以内 |
| エクスポートAPI応答時間（10件） | 1秒以内 | 500ms以内 |
| エクスポートAPI応答時間（100件） | 3秒以内 | 2秒以内 |

---

## セキュリティ検証

### 認証チェック

**目的**: 未ログイン状態で一覧・削除・エクスポートができないことを確認

```typescript
test('CHAIN-005-SEC1: セキュリティ - 未ログイン状態で一覧取得', async ({ page }) => {
  // ログインせずに一覧APIを呼び出し
  const response = await page.request.get('/api/saju/list');

  expect(response.status()).toBe(401); // Unauthorized
  const errorData = await response.json();
  expect(errorData.error).toContain('認証が必要です');
});
```

---

## 品質ゲート

CHAIN-005テストがすべて成功するための条件:

- ✅ エンドポイント連鎖（2.1 → 2.2 → 4.2）がすべて成功
- ✅ 一覧取得・削除・エクスポートが正常に動作
- ✅ 削除後に一覧が更新される
- ✅ エクスポートデータが正しい形式である
- ✅ 空の一覧が正しく表示される
- ✅ 未ログイン時にエラーが返される

---

**作成日**: 2025年11月2日
**バージョン**: 1.0
**テストツール**: Playwright
**ステータス**: 未実装
**対応API仕様書**:
- `docs/api-specs/saju-list-api.md`
- `docs/api-specs/settings-api.md`
