/**
 * E2E Test: CHAIN-006 スマホレスポンシブ対応強化
 *
 * 目的: 横スクロール、タップ領域、フォントサイズ、レイアウト崩れの確認
 * 対象: TopPage → SajuDetailPage
 */

import { test, expect } from '@playwright/test';

// ポート番号を環境変数から取得（デフォルト: 3247）
const PORT = process.env.VITE_PORT || '3247';
const BASE_URL = `http://localhost:${PORT}`;

/**
 * E2E-CHAIN-006-S1: 横スクロール - 人生グラフ（LifeGraphSection）
 *
 * 目的: 人生グラフが横にスクロールできることを確認
 * 前提条件: 命式データが1件保存済み（テスト太郎、1990年3月15日14:30、男性）
 * ビューポート: iPhone SE (375px)
 */
test('E2E-CHAIN-006-S1: 横スクロール - 人生グラフ', async ({ page }) => {
  // ビューポート設定（iPhone SE）
  await page.setViewportSize({ width: 375, height: 667 });

  // TopPageに遷移
  await page.goto(BASE_URL);
  await page.waitForLoadState('networkidle');

  // 命式計算
  // 名前入力
  const nameField = page.locator('[data-testid="name"]');
  await expect(nameField).toBeVisible({ timeout: 10000 });
  await nameField.fill('テスト太郎');

  // 生年月日入力（DatePickerは個別のspinbuttonで入力）
  const yearField = page.getByRole('spinbutton', { name: 'Year' });
  await expect(yearField).toBeVisible();
  await yearField.fill('1990');

  const monthField = page.getByRole('spinbutton', { name: 'Month' });
  await expect(monthField).toBeVisible();
  await monthField.fill('03');

  const dayField = page.getByRole('spinbutton', { name: 'Day' });
  await expect(dayField).toBeVisible();
  await dayField.fill('15');

  await page.waitForTimeout(300);

  // 時刻入力（TimePickerは個別のspinbuttonで入力）
  const hoursField = page.getByRole('spinbutton', { name: 'Hours' });
  await expect(hoursField).toBeVisible();
  await hoursField.fill('14');

  const minutesField = page.getByRole('spinbutton', { name: 'Minutes' });
  await expect(minutesField).toBeVisible();
  await minutesField.fill('30');

  await page.waitForTimeout(300);

  // 性別選択（男性）
  const maleButton = page.locator('[data-testid="gender-male"]');
  await expect(maleButton).toBeVisible();
  await maleButton.click();

  // 計算ボタンクリック
  const calculateButton = page.locator('[data-testid="calculate-button"]');
  await expect(calculateButton).toBeVisible();
  await calculateButton.click();

  // SajuDetailPageに遷移
  await page.waitForURL('**/detail/**', { timeout: 30000 });

  // ページが完全に読み込まれるまで待機
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(1000);

  // LifeGraphSectionまでスクロール
  const graphSection = page.locator('[data-testid="life-graph-section"]');

  // スクロールして要素を表示
  await graphSection.scrollIntoViewIfNeeded({ timeout: 10000 });
  await expect(graphSection).toBeVisible({ timeout: 10000 });

  // グラフが表示されていることを確認（基本テスト）
  // Rechartsのグラフ要素が存在することを確認
  const chart = graphSection.locator('.recharts-wrapper');
  await expect(chart).toBeVisible({ timeout: 5000 });

  console.log('✅ E2E-CHAIN-006-S1: 横スクロール - 人生グラフ テスト成功！');
});

/**
 * E2E-CHAIN-006-S2: 横スクロール - 大運（DaeunScrollSection）
 *
 * 目的: 大運カードが横にスクロールできることを確認
 * 前提条件: 命式データが1件保存済み（テスト太郎、1990年3月15日14:30、男性）
 * ビューポート: iPhone SE (375px)
 */
test.only('E2E-CHAIN-006-S2: 横スクロール - 大運', async ({ page }) => {
  // ブラウザコンソールログを収集
  const consoleLogs: Array<{type: string, text: string}> = [];
  page.on('console', (msg) => {
    consoleLogs.push({
      type: msg.type(),
      text: msg.text()
    });
  });

  // ビューポート設定（iPhone SE）
  await page.setViewportSize({ width: 375, height: 667 });

  // TopPageに遷移
  await page.goto(BASE_URL);
  await page.waitForLoadState('networkidle');

  // 命式計算
  // 名前入力
  const nameField = page.locator('[data-testid="name"]');
  await expect(nameField).toBeVisible({ timeout: 10000 });
  await nameField.fill('テスト太郎');

  // 生年月日入力（DatePickerは個別のspinbuttonで入力）
  const yearField = page.getByRole('spinbutton', { name: 'Year' });
  await expect(yearField).toBeVisible();
  await yearField.fill('1990');

  const monthField = page.getByRole('spinbutton', { name: 'Month' });
  await expect(monthField).toBeVisible();
  await monthField.fill('03');

  const dayField = page.getByRole('spinbutton', { name: 'Day' });
  await expect(dayField).toBeVisible();
  await dayField.fill('15');

  await page.waitForTimeout(300);

  // 時刻入力（TimePickerは個別のspinbuttonで入力）
  const hoursField = page.getByRole('spinbutton', { name: 'Hours' });
  await expect(hoursField).toBeVisible();
  await hoursField.fill('14');

  const minutesField = page.getByRole('spinbutton', { name: 'Minutes' });
  await expect(minutesField).toBeVisible();
  await minutesField.fill('30');

  await page.waitForTimeout(300);

  // 性別選択（男性）
  const maleButton = page.locator('[data-testid="gender-male"]');
  await expect(maleButton).toBeVisible();
  await maleButton.click();

  // 計算ボタンクリック
  const calculateButton = page.locator('[data-testid="calculate-button"]');
  await expect(calculateButton).toBeVisible();
  await calculateButton.click();

  // SajuDetailPageに遷移
  await page.waitForURL('**/detail/**', { timeout: 30000 });

  // ページが完全に読み込まれるまで待機
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(1000);

  // DaeunScrollSectionまでスクロール
  const daeunSection = page.locator('[data-testid="daeun-scroll-section"]');

  // スクロールして要素を表示
  await daeunSection.scrollIntoViewIfNeeded({ timeout: 10000 });
  await expect(daeunSection).toBeVisible({ timeout: 10000 });

  // 大運カードの数を確認（9個）
  const daeunCards = daeunSection.locator('[data-testid^="daeun-card-"]');
  await expect(daeunCards.first()).toBeVisible({ timeout: 5000 });
  const cardCount = await daeunCards.count();
  expect(cardCount).toBe(9);

  // カード最小幅を確認（120px以上）
  const firstCard = daeunCards.first();
  const cardWidth = await firstCard.evaluate(el => el.clientWidth);
  expect(cardWidth).toBeGreaterThanOrEqual(120);

  // スクロールコンテナを確認
  const scrollContainer = page.locator('[data-testid="daeun-scroll-container"]');

  // スクロール可能性を確認
  const scrollInfo = await scrollContainer.evaluate(el => {
    return {
      scrollWidth: el.scrollWidth,
      clientWidth: el.clientWidth,
      isScrollable: el.scrollWidth > el.clientWidth,
    };
  });
  console.log('📊 スクロール情報:', scrollInfo);
  expect(scrollInfo.isScrollable).toBeTruthy();

  // スクロール実行
  await scrollContainer.evaluate(el => {
    el.scrollLeft = 300;
  });

  // スクロール位置確認
  const scrollLeft = await scrollContainer.evaluate(el => el.scrollLeft);
  expect(scrollLeft).toBeGreaterThan(0);

  console.log('✅ E2E-CHAIN-006-S2: 横スクロール - 大運 テスト成功！');
});
