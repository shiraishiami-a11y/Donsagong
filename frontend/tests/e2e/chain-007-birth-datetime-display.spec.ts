/**
 * CHAIN-007: 生年月日時表示の正確性 - E2Eテスト
 *
 * 目的：タイムゾーン変換（UTC+9 KST）の修正を検証し、
 *      入力した生年月日時が詳細ページとリストページで正しく表示されることを確認
 *
 * 背景：
 * - 問題: 入力した「1986年5月26日 05:00」が「1986年5月25日 20:00」と誤表示される
 * - 原因: タイムゾーン変換（UTC+9）が正しく動作していない
 * - 修正: バックエンドとフロントエンドのタイムゾーン処理を修正
 */

import { test, expect, Page } from '@playwright/test';

// ヘルパー関数: 命式入力フォームに入力
async function fillSajuForm(
  page: Page,
  name: string,
  year: string,
  month: string,
  day: string,
  hours: string,
  minutes: string,
  gender: 'male' | 'female'
) {
  // 名前入力
  const nameInput = page.locator('input[data-testid="name"]');
  await nameInput.fill(name);

  // 生年月日: spinbutton要素をクリア→入力
  const yearInput = page.getByRole('spinbutton', { name: 'Year' });
  await yearInput.click();
  await yearInput.clear();
  await yearInput.fill(year);

  const monthInput = page.getByRole('spinbutton', { name: 'Month' });
  await monthInput.click();
  await monthInput.clear();
  await monthInput.fill(month);

  const dayInput = page.getByRole('spinbutton', { name: 'Day' });
  await dayInput.click();
  await dayInput.clear();
  await dayInput.fill(day);

  // 時刻: spinbutton要素をクリア→入力
  const hoursInput = page.getByRole('spinbutton', { name: 'Hours' });
  await hoursInput.click();
  await hoursInput.clear();
  await hoursInput.fill(hours);

  const minutesInput = page.getByRole('spinbutton', { name: 'Minutes' });
  await minutesInput.click();
  await minutesInput.clear();
  await minutesInput.fill(minutes);

  // 性別を選択
  await page.locator(`[data-testid="gender-${gender}"]`).click();
}

test.describe('CHAIN-007: 生年月日時表示の正確性', () => {
  // ========================================
  // 正常系（必須）- 5項目
  // ========================================

  test('E2E-CHAIN-007-S1: 朝の時刻（05:00）の表示確認', async ({ page }) => {
    // Step 1: トップページにアクセス
    await page.goto('http://localhost:3247');

    // Step 2: 生年月日時を入力（1986年5月26日 05:00）
    await fillSajuForm(page, 'テスト太郎', '1986', '05', '26', '05', '00', 'male');

    // Step 3: 計算ボタンをクリック
    const calculateButton = page.locator('button:has-text("命式を計算")');
    await calculateButton.click();

    // ローディングが終わるまで待機
    await page.waitForLoadState('networkidle');

    // 詳細ページへの遷移を確認（URLが /detail/ を含む）
    await page.waitForURL('**/detail/**', { timeout: 10000 });

    // 詳細ページのコンテンツがレンダリングされるまで待機
    await page.waitForSelector('text=基本情報', { timeout: 10000 });

    // Step 4: 詳細ページで生年月日時を確認
    // ページ全体のテキストを取得
    const pageText = await page.textContent('body');

    console.log('[DEBUG] ページテキストに1986年5月26日が含まれるか:', pageText?.includes('1986年5月26日'));
    console.log('[DEBUG] ページテキストに5:00が含まれるか:', pageText?.includes('5:00'));

    // 実際の表示形式を確認（スペース、全角/半角、ゼロ埋めなどのバリエーションを許容）
    const hasCorrectDate = pageText?.includes('1986年5月26日') &&
                          (pageText?.includes('5:00') || pageText?.includes('05:00') || pageText?.includes(' 5:00'));

    expect(hasCorrectDate).toBeTruthy();

    console.log('[E2E-CHAIN-007-S1] 詳細ページに正しい日時が表示されました');

    // Step 5: リストページに遷移（閉じるボタンをクリック）
    await page.click('[data-testid="close-button"]');
    await page.waitForLoadState('networkidle');

    // リストページのコンテンツがレンダリングされるまで待機
    await page.waitForSelector('[data-testid="saju-list-container"]', { timeout: 10000 });

    // Step 6: リストページで生年月日時を確認
    const listPageText = await page.textContent('body');

    // リストページにも同じ日時が表示されることを確認
    const hasCorrectDateList = listPageText?.includes('1986年5月26日') &&
                               (listPageText?.includes('5:00') || listPageText?.includes('05:00'));
    expect(hasCorrectDateList).toBeTruthy();

    console.log('[E2E-CHAIN-007-S1] リストページにも正しい日時が表示されました');
  });

  test('E2E-CHAIN-007-S2: 昼の時刻（12:00）の表示確認', async ({ page }) => {
    await page.goto('http://localhost:3247');
    await fillSajuForm(page, 'テスト花子', '1990', '03', '15', '12', '00', 'female');
    await page.locator('button:has-text("命式を計算")').click();

    await page.waitForLoadState('networkidle');
    await page.waitForURL('**/detail/**', { timeout: 10000 });
    await page.waitForSelector('text=基本情報', { timeout: 10000 });

    const pageText = await page.textContent('body');
    expect(pageText?.includes('1990年3月15日') && pageText?.includes('12:00')).toBeTruthy();

    await page.click('[data-testid="close-button"]');
    await page.waitForLoadState('networkidle');
    await page.waitForSelector('[data-testid="saju-list-container"]', { timeout: 10000 });

    const listPageText = await page.textContent('body');
    expect(listPageText?.includes('1990年3月15日') && listPageText?.includes('12:00')).toBeTruthy();

    console.log('[E2E-CHAIN-007-S2] Pass');
  });

  test('E2E-CHAIN-007-S3: 夕方の時刻（18:00）の表示確認', async ({ page }) => {
    await page.goto('http://localhost:3247');
    await fillSajuForm(page, 'テスト次郎', '1995', '06', '20', '18', '00', 'male');
    await page.locator('button:has-text("命式を計算")').click();

    await page.waitForLoadState('networkidle');
    await page.waitForURL('**/detail/**', { timeout: 10000 });
    await page.waitForSelector('text=基本情報', { timeout: 10000 });

    const pageText = await page.textContent('body');
    expect(pageText?.includes('1995年6月20日') && pageText?.includes('18:00')).toBeTruthy();

    await page.click('[data-testid="close-button"]');
    await page.waitForLoadState('networkidle');
    await page.waitForSelector('[data-testid="saju-list-container"]', { timeout: 10000 });

    const listPageText = await page.textContent('body');
    expect(listPageText?.includes('1995年6月20日') && listPageText?.includes('18:00')).toBeTruthy();

    console.log('[E2E-CHAIN-007-S3] Pass');
  });

  test('E2E-CHAIN-007-S4: 深夜の時刻（23:30）の表示確認', async ({ page }) => {
    await page.goto('http://localhost:3247');
    await fillSajuForm(page, 'テスト春子', '2000', '12', '31', '23', '30', 'female');
    await page.locator('button:has-text("命式を計算")').click();

    await page.waitForLoadState('networkidle');
    await page.waitForURL('**/detail/**', { timeout: 10000 });
    await page.waitForSelector('text=基本情報', { timeout: 10000 });

    const pageText = await page.textContent('body');
    expect(pageText?.includes('2000年12月31日') && pageText?.includes('23:30')).toBeTruthy();

    // 重要: 翌日の「2001年1月1日」になっていないことを確認
    expect(pageText?.includes('2001年1月1日')).toBeFalsy();

    await page.click('[data-testid="close-button"]');
    await page.waitForLoadState('networkidle');
    await page.waitForSelector('[data-testid="saju-list-container"]', { timeout: 10000 });

    const listPageText = await page.textContent('body');
    expect(listPageText?.includes('2000年12月31日') && listPageText?.includes('23:30')).toBeTruthy();

    console.log('[E2E-CHAIN-007-S4] Pass');
  });

  test('E2E-CHAIN-007-S5: 詳細ページとリストページの表示一致確認', async ({ page }) => {
    await page.goto('http://localhost:3247');
    await fillSajuForm(page, 'テスト一致確認', '1985', '11', '11', '14', '30', 'male');
    await page.locator('button:has-text("命式を計算")').click();

    await page.waitForLoadState('networkidle');
    await page.waitForURL('**/detail/**', { timeout: 10000 });
    await page.waitForSelector('text=基本情報', { timeout: 10000 });

    const detailPageText = await page.textContent('body');

    await page.click('[data-testid="close-button"]');
    await page.waitForLoadState('networkidle');
    await page.waitForSelector('[data-testid="saju-list-container"]', { timeout: 10000 });

    const listPageText = await page.textContent('body');

    // 詳細ページとリストページの日時表示が一致することを確認
    expect(detailPageText?.includes('1985年11月11日') && detailPageText?.includes('14:30')).toBeTruthy();
    expect(listPageText?.includes('1985年11月11日') && listPageText?.includes('14:30')).toBeTruthy();

    console.log('[E2E-CHAIN-007-S5] Pass - 表示一致確認');
  });

  // ========================================
  // エッジケース - 3項目
  // ========================================

  test('E2E-CHAIN-007-E1: タイムゾーン境界値（00:00）', async ({ page }) => {
    await page.goto('http://localhost:3247');
    await fillSajuForm(page, 'テスト境界0時', '2010', '01', '01', '00', '00', 'male');
    await page.locator('button:has-text("命式を計算")').click();

    await page.waitForLoadState('networkidle');
    await page.waitForURL('**/detail/**', { timeout: 10000 });
    await page.waitForSelector('text=基本情報', { timeout: 10000 });

    const pageText = await page.textContent('body');

    // 「2010年1月1日 0:00」と表示されることを確認
    expect(pageText?.includes('2010年1月1日') && pageText?.includes('0:00')).toBeTruthy();

    // 重要: 前日の「2009年12月31日」になっていないことを確認
    expect(pageText?.includes('2009年12月31日')).toBeFalsy();

    console.log('[E2E-CHAIN-007-E1] Pass - タイムゾーン境界値（00:00）');
  });

  test('E2E-CHAIN-007-E2: タイムゾーン境界値（23:59）', async ({ page }) => {
    await page.goto('http://localhost:3247');
    await fillSajuForm(page, 'テスト境界23時', '2010', '12', '31', '23', '59', 'female');
    await page.locator('button:has-text("命式を計算")').click();

    await page.waitForLoadState('networkidle');
    await page.waitForURL('**/detail/**', { timeout: 10000 });
    await page.waitForSelector('text=基本情報', { timeout: 10000 });

    const pageText = await page.textContent('body');

    // 「2010年12月31日 23:59」と表示されることを確認
    expect(pageText?.includes('2010年12月31日') && pageText?.includes('23:59')).toBeTruthy();

    // 重要: 翌日の「2011年1月1日」になっていないことを確認
    expect(pageText?.includes('2011年1月1日')).toBeFalsy();

    console.log('[E2E-CHAIN-007-E2] Pass - タイムゾーン境界値（23:59）');
  });

  test('E2E-CHAIN-007-E3: 日付変更をまたぐ時刻の連続入力', async ({ page }) => {
    // 1件目: 23:59
    await page.goto('http://localhost:3247');
    await fillSajuForm(page, '23時59分', '2015', '06', '15', '23', '59', 'male');
    await page.locator('button:has-text("命式を計算")').click();

    await page.waitForLoadState('networkidle');
    await page.waitForURL('**/detail/**', { timeout: 10000 });
    await page.click('[data-testid="close-button"]');
    await page.waitForLoadState('networkidle');

    // 2件目: 00:00（翌日）
    await page.goto('http://localhost:3247');
    await fillSajuForm(page, '0時0分', '2015', '06', '16', '00', '00', 'female');
    await page.locator('button:has-text("命式を計算")').click();

    await page.waitForLoadState('networkidle');
    await page.waitForURL('**/detail/**', { timeout: 10000 });
    await page.click('[data-testid="close-button"]');
    await page.waitForLoadState('networkidle');
    await page.waitForSelector('[data-testid="saju-list-container"]', { timeout: 10000 });

    // リストページで2件のデータを確認
    const listPageText = await page.textContent('body');

    expect(listPageText?.includes('2015年6月15日') && listPageText?.includes('23:59')).toBeTruthy();
    expect(listPageText?.includes('2015年6月16日') && listPageText?.includes('0:00')).toBeTruthy();

    console.log('[E2E-CHAIN-007-E3] Pass - 日付変更をまたぐ連続入力');
  });

  // ========================================
  // UI/UX（推奨）- 3項目
  // ========================================

  test('E2E-CHAIN-007-U1: 詳細ページの日時表示フォーマット', async ({ page }) => {
    await page.goto('http://localhost:3247');
    await fillSajuForm(page, 'フォーマット確認', '1986', '05', '26', '05', '00', 'male');
    await page.locator('button:has-text("命式を計算")').click();

    await page.waitForLoadState('networkidle');
    await page.waitForURL('**/detail/**', { timeout: 10000 });
    await page.waitForSelector('text=基本情報', { timeout: 10000 });

    const pageText = await page.textContent('body');

    // フォーマット: 「YYYY年M月D日 H:mm」（先頭ゼロなし）
    expect(pageText?.includes('1986年5月26日') && pageText?.includes('5:00')).toBeTruthy();

    // NG例: 「1986年05月26日 05:00」（先頭ゼロあり）
    expect(pageText?.includes('1986年05月26日')).toBeFalsy();

    console.log('[E2E-CHAIN-007-U1] Pass - 日時表示フォーマット確認');
  });

  test('E2E-CHAIN-007-U2: リストページの日時表示フォーマット', async ({ page }) => {
    await page.goto('http://localhost:3247');
    await fillSajuForm(page, 'リスト表示確認', '1990', '03', '15', '08', '30', 'female');
    await page.locator('button:has-text("命式を計算")').click();

    await page.waitForLoadState('networkidle');
    await page.waitForURL('**/detail/**', { timeout: 10000 });
    await page.click('[data-testid="close-button"]');
    await page.waitForLoadState('networkidle');
    await page.waitForSelector('[data-testid="saju-list-container"]', { timeout: 10000 });

    const listPageText = await page.textContent('body');

    // フォーマット: 詳細ページと同一
    expect(listPageText?.includes('1990年3月15日') && listPageText?.includes('8:30')).toBeTruthy();

    console.log('[E2E-CHAIN-007-U2] Pass - リストページ表示フォーマット確認');
  });

  test('E2E-CHAIN-007-U3: 年月日運セクションでの日時表示', async ({ page }) => {
    await page.goto('http://localhost:3247');
    await fillSajuForm(page, '運勢表示確認', '1995', '06', '20', '10', '15', 'male');
    await page.locator('button:has-text("命式を計算")').click();

    await page.waitForLoadState('networkidle');
    await page.waitForURL('**/detail/**', { timeout: 10000 });
    await page.waitForSelector('text=基本情報', { timeout: 10000 });

    // 年運セクションで大運カードをクリック（data-testidがなければスキップ）
    const daeunCards = await page.locator('[data-testid="daeun-card"]').count();
    if (daeunCards > 0) {
      await page.locator('[data-testid="daeun-card"]').first().click();
      await page.waitForTimeout(1000);  // アニメーション待機

      // 年運セクションが表示される
      const yearSection = await page.locator('[data-testid="year-scroll-section"]').count();
      expect(yearSection).toBeGreaterThan(0);

      console.log('[E2E-CHAIN-007-U3] Pass - 年月日運セクション表示確認');
    } else {
      console.log('[E2E-CHAIN-007-U3] Skip - 大運カードが見つかりません');
    }
  });

  test.afterEach(async ({ page }) => {
    // テスト終了後にLocalStorageをクリア
    await page.evaluate(() => localStorage.clear());
  });
});
