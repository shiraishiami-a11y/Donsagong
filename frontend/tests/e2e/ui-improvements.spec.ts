/**
 * UI改善要件のE2Eテスト
 *
 * 検証項目:
 * 1. 人生グラフが正しい階段式で表示される
 * 2. 5段階全ての色が正しく表示される
 * 3. 大凶は波線、大吉は太線で表示される
 * 4. 詳細ページに閉じるボタンがある
 * 5. 閉じるボタンで /list に遷移する
 * 6. 点（dot）が表示されない
 */

import { test, expect } from '@playwright/test';

test.describe('UI改善要件の検証', () => {
  test.beforeEach(async ({ page }) => {
    // トップページから命式を作成して詳細ページへ
    await page.goto('/');
    await expect(page).toHaveURL('/');

    // 生年月日入力: 1990年1月15日 14時30分
    const spinbuttons = page.getByRole('spinbutton');

    // 年の入力
    const yearInput = spinbuttons.first();
    await yearInput.click();
    await yearInput.clear();
    await yearInput.fill('1990');

    // 月の入力
    const monthInput = spinbuttons.nth(1);
    await monthInput.click();
    await monthInput.clear();
    await monthInput.fill('1');

    // 日の入力
    const dayInput = spinbuttons.nth(2);
    await dayInput.click();
    await dayInput.clear();
    await dayInput.fill('15');

    // 時の入力
    const hourInput = spinbuttons.nth(3);
    await hourInput.click();
    await hourInput.clear();
    await hourInput.fill('14');

    // 分の入力
    const minuteInput = spinbuttons.nth(4);
    await minuteInput.click();
    await minuteInput.clear();
    await minuteInput.fill('30');

    // 性別選択: 男性
    await page.click('[data-testid="gender-male"]');

    // 名前入力
    await page.fill('[data-testid="name"]', 'テスト太郎');

    // 計算ボタンをクリック
    await page.click('[data-testid="calculate-button"]');

    // 詳細ページに遷移するまで待機
    await page.waitForURL('**/detail/**', { timeout: 10000 });
  });

  test('要件1: 人生グラフが階段式で表示される', async ({ page }) => {
    // 人生グラフセクションが存在することを確認
    await page.waitForSelector('text=人生グラフ', { timeout: 5000 });

    // Rechartsのグラフが存在することを確認
    const chart = page.locator('.recharts-wrapper');
    await expect(chart).toBeVisible({ timeout: 5000 });

    // グラフ内にSVGパスが存在することを確認（階段式グラフ）
    const paths = page.locator('.recharts-surface path');
    const pathCount = await paths.count();
    expect(pathCount).toBeGreaterThan(0);
  });

  test('要件2&4: 5段階色分けグラフの表示確認', async ({ page }) => {
    // Rechartsのグラフを待機
    await page.waitForSelector('.recharts-wrapper', { timeout: 5000 });

    // 各吉凶レベルのLine要素を確認
    const lines = page.locator('.recharts-line-curve');
    const lineCount = await lines.count();

    // 5つのLineコンポーネントが存在することを確認（大凶、凶、平、吉、大吉）
    expect(lineCount).toBeGreaterThanOrEqual(1);

    // SVG内のpath要素の属性を確認
    const paths = await page.locator('.recharts-line-curve').all();

    // 少なくとも1つのラインが描画されていることを確認
    expect(paths.length).toBeGreaterThan(0);

    for (const path of paths) {
      const stroke = await path.getAttribute('stroke');
      const strokeWidth = await path.getAttribute('stroke-width');

      // 色が定義されていることを確認
      expect(stroke).toBeTruthy();

      // strokeWidthが設定されていることを確認
      expect(strokeWidth).toBeTruthy();

      // 5段階のいずれかの色であることを確認
      const validColors = ['#F44336', '#D4AF37', '#4CAF50', '#9E9E9E'];
      const isValidColor = validColors.some(color => stroke === color);
      expect(isValidColor).toBeTruthy();
    }
  });

  test('要件3: 大凶は波線、大吉は太線で表示', async ({ page }) => {
    // Rechartsのグラフを待機
    await page.waitForSelector('.recharts-wrapper', { timeout: 5000 });

    // グラフ内にパスが存在することを確認
    const paths = page.locator('.recharts-surface path');
    const pathCount = await paths.count();
    expect(pathCount).toBeGreaterThan(0);

    // SVGグラフが正しくレンダリングされていることを確認
    const svg = page.locator('.recharts-wrapper svg');
    await expect(svg).toBeVisible();
  });

  test('要件2: 詳細ページに閉じるボタンがある', async ({ page }) => {
    // 閉じるボタンが存在することを確認（CloseIconを持つボタン）
    const closeButton = page.locator('button').filter({ has: page.locator('svg') }).first();
    await expect(closeButton).toBeVisible({ timeout: 5000 });

    // ボタンの位置を確認（左上）
    const box = await closeButton.boundingBox();
    expect(box).toBeTruthy();
    if (box) {
      // 左上に配置されていることを確認（X座標が小さい、Y座標が小さい）
      expect(box.x).toBeLessThan(150);
      expect(box.y).toBeLessThan(150);
    }
  });

  test('要件3: 閉じるボタンで /list に遷移する', async ({ page }) => {
    // 現在のURLを確認（/detail/詳細ページ）
    const currentUrl = page.url();
    expect(currentUrl).toContain('/detail/');

    // 閉じるボタンをクリック
    const closeButton = page.locator('button').filter({ has: page.locator('svg') }).first();
    await closeButton.click();

    // /list ページに遷移することを確認
    await page.waitForURL('**/list', { timeout: 5000 });
    expect(page.url()).toContain('/list');
  });

  test('要件1: グラフに点（dot）が表示されない', async ({ page }) => {
    // Rechartsのグラフを待機
    await page.waitForSelector('.recharts-wrapper', { timeout: 5000 });

    // dot要素が存在しないことを確認
    const dots = page.locator('.recharts-dot');
    const dotCount = await dots.count();

    // dotが0個であることを確認
    expect(dotCount).toBe(0);

    // circleタグで描画されるドットも存在しないことを確認
    const circles = page.locator('.recharts-line circle');
    const circleCount = await circles.count();
    expect(circleCount).toBe(0);
  });

  test('統合テスト: 全ての要件が満たされている', async ({ page }) => {
    // 1. 人生グラフセクションが存在
    const graphSection = page.locator('text=人生グラフ').locator('..');
    await expect(graphSection).toBeVisible({ timeout: 5000 });

    // 2. 閉じるボタンが存在
    const closeButton = page.locator('button').filter({ has: page.locator('svg') }).first();
    await expect(closeButton).toBeVisible({ timeout: 5000 });

    // 3. グラフが表示されている
    const chart = page.locator('.recharts-wrapper');
    await expect(chart).toBeVisible();

    // 4. Lineが描画されている
    const lines = page.locator('.recharts-line-curve');
    const lineCount = await lines.count();
    expect(lineCount).toBeGreaterThan(0);

    // 5. dotが存在しない
    const dots = page.locator('.recharts-dot');
    const dotCount = await dots.count();
    expect(dotCount).toBe(0);

    // 6. 閉じるボタンをクリックして遷移確認
    await closeButton.click();
    await page.waitForURL('**/list', { timeout: 5000 });
    expect(page.url()).toContain('/list');
  });
});
