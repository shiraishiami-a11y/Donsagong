# E2Eテスト未実装箇所一覧

**作成日**: 2025年11月3日
**プロジェクト**: ゴールデン四柱推命アプリケーション
**最終更新**: 2025年11月3日（CHAIN-002実装完了後）

---

## 📊 現状サマリー

### 全体進捗

| 項目 | 結果 |
|------|------|
| **実装済みテスト数** | 28件（CHAIN-002追加後） |
| **仕様書総シナリオ数** | 29件 |
| **実装カバレッジ** | **66%**（19/29シナリオ） |
| **完全実装CHAIN** | CHAIN-001 (100%), CHAIN-002 (100%) |
| **部分実装CHAIN** | CHAIN-003 (60%), CHAIN-005 (17%) |
| **未実装CHAIN** | CHAIN-004 (0%) |

---

## ❌ 未実装項目一覧

### 1. CHAIN-003: インタラクティブ運勢選択（残り2項目）

**実装ステータス**: ⚠️ 部分実装（60% = 3/5）

| シナリオID | 内容 | 優先度 | 推定工数 | 実装難易度 |
|-----------|------|-------|---------|-----------|
| **E2E-CHAIN-003-S4** | UI/UX - 連続クリックでスムーズに階層移動 | 🔴 高 | 1時間 | 低 |
| **E2E-CHAIN-003-S5** | 異常系 - 範囲外の年・月・日でアクセス | 🔴 高 | 1時間 | 低 |

**実装済み**:
- ✅ S1: 大運クリックで年運表示
- ✅ S2: 年運クリックで月運表示
- ✅ S3: 月運クリックで日運表示

**必要な作業**:

#### E2E-CHAIN-003-S4: 連続クリックパフォーマンステスト
```typescript
test('E2E-CHAIN-003-S4: UI/UX - 連続クリックでスムーズに階層移動', async ({ page }) => {
  // 大運→年運→月運→日運と連続クリック
  // 各遷移が1秒以内に完了することを確認

  const startTime = Date.now();

  // 大運クリック
  await page.click('[data-testid="daeun-card-18"]');
  const time1 = Date.now() - startTime;
  expect(time1).toBeLessThan(1000);

  // 年運クリック
  await page.click('[data-testid="year-card"]');
  const time2 = Date.now() - startTime - time1;
  expect(time2).toBeLessThan(1000);

  // 月運クリック
  await page.click('[data-testid="month-card"]');
  const time3 = Date.now() - startTime - time2;
  expect(time3).toBeLessThan(1000);

  // 総時間が3秒以内
  const totalTime = Date.now() - startTime;
  expect(totalTime).toBeLessThan(3000);
});
```

#### E2E-CHAIN-003-S5: 異常系テスト
```typescript
test('E2E-CHAIN-003-S5: 異常系 - 範囲外の年・月・日', async ({ page }) => {
  // 直接APIを呼び出し
  const response = await page.request.get('/api/saju/saju-id/day/2025/99');
  expect(response.status()).toBe(400);

  const errorData = await response.json();
  expect(errorData.error).toContain('無効な月');
});
```

---

### 2. CHAIN-004: ゲスト→ログイン移行（全5項目）

**実装ステータス**: ❌ 未実装（0% = 0/5）
**前提条件**: 認証機能（JWT）の実装完了が必要

| シナリオID | 内容 | 優先度 | 推定工数 | 実装難易度 |
|-----------|------|-------|---------|-----------|
| **E2E-CHAIN-004-S1** | 正常系 - ゲストデータ移行成功 | 🟡 中 | 2時間 | 高 |
| **E2E-CHAIN-004-S2** | 正常系 - ゲストデータなしで新規登録 | 🟡 中 | 1時間 | 中 |
| **E2E-CHAIN-004-S3** | 正常系 - データ移行チェックボックスOFFで新規登録 | 🟡 中 | 1時間 | 中 |
| **E2E-CHAIN-004-S4** | 異常系 - データ移行中にエラー発生 | 🟡 中 | 1.5時間 | 高 |
| **E2E-CHAIN-004-S5** | 異常系 - 重複メールアドレスで登録 | 🟡 中 | 0.5時間 | 低 |

**必要な前提条件**:
1. ✅ `/api/auth/register` エンドポイント実装
2. ✅ `/api/auth/login` エンドポイント実装
3. ✅ `/api/saju/migrate` エンドポイント実装
4. ✅ JWTトークン管理の実装
5. ✅ LocalStorage ⇔ PostgreSQL データ移行ロジック

**実装例**:

#### E2E-CHAIN-004-S1: ゲストデータ移行
```typescript
test('E2E-CHAIN-004-S1: ゲストデータ移行成功', async ({ page }) => {
  // 1. LocalStorageにテストデータを保存
  await page.evaluate(() => {
    const testData = [
      { id: 'guest-001', name: 'テスト太郎', /* ... */ },
      { id: 'guest-002', name: 'テスト花子', /* ... */ }
    ];
    localStorage.setItem('saju_data', JSON.stringify(testData));
  });

  // 2. 新規登録ページにアクセス
  await page.goto('/register');

  // 3. 新規登録
  await page.fill('[data-testid="email"]', 'test@example.com');
  await page.fill('[data-testid="password"]', 'Password123!');
  await page.check('[data-testid="migrate-guest-data"]');
  await page.click('[data-testid="register-button"]');

  // 4. データ移行成功確認
  await expect(page.locator('[data-testid="migration-success"]')).toBeVisible();

  // 5. LocalStorageが空になっていることを確認
  const localStorageData = await page.evaluate(() => {
    return localStorage.getItem('saju_data');
  });
  expect(localStorageData).toBeNull();

  // 6. 命式リストページで移行データが表示されることを確認
  await expect(page).toHaveURL('/list');
  await expect(page.locator('[data-testid="saju-list-item"]')).toHaveCount(2);
});
```

---

### 3. CHAIN-005: データ管理統合（残り5項目）

**実装ステータス**: ⚠️ 部分実装（17% = 1/6）

| シナリオID | 内容 | 優先度 | 推定工数 | 実装難易度 |
|-----------|------|-------|---------|-----------|
| **E2E-CHAIN-005-S2** | 正常系 - 命式削除 | 🔴 高 | 1.5時間 | 中 |
| **E2E-CHAIN-005-S3** | 正常系 - データエクスポート | 🟡 中 | 2時間 | 中 |
| **E2E-CHAIN-005-S4** | 正常系 - 連鎖テスト（一覧→削除→エクスポート） | 🟡 中 | 1時間 | 中 |
| **E2E-CHAIN-005-S5** | 異常系 - 存在しない命式の削除 | 🟢 低 | 0.5時間 | 低 |
| **E2E-CHAIN-005-S6** | 異常系 - 空の一覧表示 | 🟢 低 | 0.5時間 | 低 |

**実装済み**:
- ✅ S1: 命式一覧取得と表示

**必要な作業**:

#### E2E-CHAIN-005-S2: 命式削除
```typescript
test('E2E-CHAIN-005-S2: 命式削除', async ({ page }) => {
  // 1. 命式リストページにアクセス
  await page.goto('/list');

  // 2. 一覧取得
  const listResponse = await page.waitForResponse(res =>
    res.url().includes('/api/saju/list') && res.status() === 200
  );
  const listData = await listResponse.json();
  const countBefore = listData.length;
  const targetId = listData[0].id;

  // 3. 削除ボタンクリック
  await page.click(`[data-testid="delete-button-${targetId}"]`);

  // 4. 削除確認ダイアログ
  await expect(page.locator('[data-testid="delete-confirm-dialog"]')).toBeVisible();
  await page.click('[data-testid="confirm-delete-button"]');

  // 5. 削除API呼び出し確認
  const deleteResponse = await page.waitForResponse(res =>
    res.url().includes(`/api/saju/${targetId}`) &&
    res.request().method() === 'DELETE' &&
    res.status() === 200
  );

  expect(deleteResponse.status()).toBe(200);

  // 6. 一覧から削除されたことを確認
  await page.waitForTimeout(1000);
  const sajuCards = page.locator('[data-testid="saju-list-item"]');
  await expect(sajuCards).toHaveCount(countBefore - 1);
});
```

#### E2E-CHAIN-005-S3: データエクスポート
```typescript
test('E2E-CHAIN-005-S3: データエクスポート', async ({ page }) => {
  // 1. 設定ページにアクセス
  await page.goto('/settings');

  // 2. ダウンロード待機設定
  const downloadPromise = page.waitForEvent('download');

  // 3. エクスポートボタンクリック
  await page.click('[data-testid="export-button"]');

  // 4. エクスポートAPI呼び出し確認
  const exportResponse = await page.waitForResponse(res =>
    res.url().includes('/api/saju/export') && res.status() === 200
  );
  const exportData = await exportResponse.json();

  expect(exportData).toBeInstanceOf(Array);
  expect(exportData.length).toBeGreaterThan(0);

  // 5. ダウンロード確認
  const download = await downloadPromise;
  const filename = download.suggestedFilename();
  expect(filename).toMatch(/saju_export_\d{8}\.json/);

  // 6. ファイル内容確認
  const path = await download.path();
  const fs = require('fs');
  const fileContent = fs.readFileSync(path, 'utf-8');
  const parsedData = JSON.parse(fileContent);

  expect(parsedData).toEqual(exportData);
});
```

---

## 🔧 追加で必要な修正

### 1. `test.only` の削除（緊急）

**ファイル**: `frontend/tests/e2e/chain-003-interactive-fortune.spec.ts:240`

```typescript
// 修正前
test.only('E2E-CHAIN-003-S3: 正常系 - 月運クリックで日運表示', async ({ page }) => {

// 修正後
test('E2E-CHAIN-003-S3: 正常系 - 月運クリックで日運表示', async ({ page }) => {
```

**影響**: `test.only` があると他のテストがスキップされる
**優先度**: 🔴 **最高**（即座に対応必要）

---

## 📈 優先順位別実装ロードマップ

### 🔴 最高優先度（即座に対応）

1. **`test.only` 削除** - `chain-003-interactive-fortune.spec.ts:240`
   - 推定工数: 1分
   - 理由: 他のテストがスキップされる

### 🔴 高優先度（1週間以内）

2. **CHAIN-003完全実装** - S4, S5追加
   - 推定工数: 2時間
   - 理由: 既存実装の拡張で済む

3. **CHAIN-005-S2** - 命式削除テスト
   - 推定工数: 1.5時間
   - 理由: 基本的なCRUD操作の検証

### 🟡 中優先度（1ヶ月以内）

4. **CHAIN-005-S3** - データエクスポート
   - 推定工数: 2時間

5. **CHAIN-005-S4-S6** - 連鎖テスト・異常系
   - 推定工数: 2時間

6. **data-testid追加** - 主要コンポーネント
   - 推定工数: 3時間
   - 対象:
     - MonthFortuneScrollSection
     - DayFortuneScrollSection
     - ListPage コンポーネント
     - SettingsPage コンポーネント

### 🟢 低優先度（3ヶ月以内）

7. **CHAIN-004全体** - ゲスト→ログイン移行
   - 推定工数: 8時間
   - 前提条件: 認証機能実装完了

---

## 📊 実装完了後の予想カバレッジ

### 短期完了後（1週間）

| CHAIN | 現在 | 短期完了後 |
|-------|------|----------|
| CHAIN-001 | 100% (11/11) | 100% |
| CHAIN-002 | 100% (4/4) | 100% |
| CHAIN-003 | 60% (3/5) | **100% (5/5)** ✅ |
| CHAIN-004 | 0% (0/5) | 0% |
| CHAIN-005 | 17% (1/6) | **50% (3/6)** ⬆️ |
| **合計** | **66% (19/29)** | **79% (23/29)** |

### 中期完了後（1ヶ月）

| CHAIN | 短期 | 中期完了後 |
|-------|------|----------|
| CHAIN-001 | 100% | 100% |
| CHAIN-002 | 100% | 100% |
| CHAIN-003 | 100% | 100% |
| CHAIN-004 | 0% | 0% |
| CHAIN-005 | 50% | **100% (6/6)** ✅ |
| **合計** | **79%** | **86% (25/29)** |

### 長期完了後（3ヶ月）

| CHAIN | 中期 | 長期完了後 |
|-------|------|----------|
| CHAIN-001 | 100% | 100% |
| CHAIN-002 | 100% | 100% |
| CHAIN-003 | 100% | 100% |
| CHAIN-004 | 0% | **100% (5/5)** ✅ |
| CHAIN-005 | 100% | 100% |
| **合計** | **86%** | **100% (29/29)** 🎉 |

---

## 📝 まとめ

### 現状

- ✅ **実装済み**: 19シナリオ（66%）
  - CHAIN-001: 100%（11シナリオ）
  - CHAIN-002: 100%（4シナリオ）
  - CHAIN-003: 60%（3シナリオ）
  - CHAIN-005: 17%（1シナリオ）

- ❌ **未実装**: 10シナリオ（34%）
  - CHAIN-003: 2シナリオ（S4, S5）
  - CHAIN-004: 5シナリオ（全て）
  - CHAIN-005: 5シナリオ（S2-S6）

### 次のアクション

#### 即座に対応（今日中）
1. ✅ `test.only` 削除

#### 短期対応（1週間以内）
2. CHAIN-003-S4, S5 実装
3. CHAIN-005-S2 実装

#### 中期対応（1ヶ月以内）
4. CHAIN-005-S3-S6 実装
5. `data-testid` 追加

#### 長期対応（3ヶ月以内）
6. CHAIN-004全体実装（認証機能実装後）

---

**作成日**: 2025年11月3日
**最終更新**: 2025年11月3日
**次回更新予定**: 短期対応完了後
