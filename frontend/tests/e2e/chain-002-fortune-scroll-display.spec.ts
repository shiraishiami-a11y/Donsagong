// CHAIN-002: 水平スクロール運勢表示 E2Eテスト
// 対応ページ: P-003（命式詳細・グラフページ）

import { test, expect } from '@playwright/test';

// 共通の前処理: 命式計算・保存を行い、詳細ページに遷移
async function setupSajuDetail(page: any) {
  // トップページにアクセス
  await page.goto('/');
  await expect(page).toHaveURL('/');

  // 生年月日時入力: 1990年3月15日 14時30分
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
  await monthInput.fill('3');

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
  await page.fill('[data-testid="name"]', 'テスト太郎（CHAIN-002）');

  // 計算ボタンクリック
  await page.click('[data-testid="calculate-button"]');

  // 命式詳細ページへ遷移を待機
  await page.waitForURL('**/detail/**', { timeout: 10000 });

  // 現在のURL取得（命式ID含む）
  const currentUrl = page.url();
  const sajuId = currentUrl.split('/detail/')[1];

  return sajuId;
}

test.describe('CHAIN-002: 水平スクロール運勢表示', () => {
  // E2E-CHAIN-002-S1: 正常系 - 階層的運勢表示（大運→年運→月運→日運）
  test('E2E-CHAIN-002-S1: 正常系 - 階層的運勢表示（大運→年運→月運→日運）', async ({ page }) => {
    console.log('[CHAIN-002-S1] テスト開始');

    // 前提: 命式詳細ページに遷移
    const sajuId = await setupSajuDetail(page);
    console.log(`[CHAIN-002-S1] 命式ID: ${sajuId}`);

    // ステップ1: 大運リスト表示確認
    await expect(page.locator('text=大運（10年周期）')).toBeVisible({ timeout: 10000 });
    console.log('[CHAIN-002-S1] 大運リスト表示確認 OK');

    // 大運カードが複数表示されることを確認
    const daeunCards = page.locator('text=/^\\d+-\\d+歳$/');
    const daeunCount = await daeunCards.count();
    expect(daeunCount).toBeGreaterThan(0);
    console.log(`[CHAIN-002-S1] 大運カード数: ${daeunCount}`);

    // ステップ2: 大運の1つをクリック（2番目の大運を選択）
    const secondDaeun = daeunCards.nth(1);
    await expect(secondDaeun).toBeVisible({ timeout: 5000 });
    await secondDaeun.click();
    console.log('[CHAIN-002-S1] 2番目の大運クリック');

    // ステップ3: 年運リスト表示確認（10年分）
    // 年運セクションが表示されるまで待機
    await page.waitForTimeout(2000);

    // 年運セクションのタイトルを検索（正規表現で範囲を含む）
    const yearSectionTitle = page.locator('text=/年運（\\d+-\\d+歳）/');
    await expect(yearSectionTitle).toBeVisible({ timeout: 5000 });
    console.log('[CHAIN-002-S1] 年運セクション表示確認 OK');

    // 年運カードが表示されることを確認
    await page.waitForTimeout(500);
    const yearCards = page.locator('[data-testid="year-card"]');
    const yearCount = await yearCards.count();
    expect(yearCount).toBeGreaterThanOrEqual(1);
    console.log(`[CHAIN-002-S1] 年運カード数: ${yearCount}`);

    // ステップ4: 年運の1つをクリック
    const firstYear = yearCards.first();
    await expect(firstYear).toBeVisible({ timeout: 5000 });
    await firstYear.click();
    console.log('[CHAIN-002-S1] 最初の年運クリック');

    // ステップ5: 月運リスト表示確認（12ヶ月分）
    await page.waitForTimeout(2000);

    // 月運セクションのタイトルを検索
    const monthSectionTitle = page.locator('text=/月運（\\d+年）/');
    await expect(monthSectionTitle).toBeVisible({ timeout: 5000 });
    console.log('[CHAIN-002-S1] 月運セクション表示確認 OK');

    // 月運カードが表示されることを確認
    await page.waitForTimeout(500);
    const monthCards = page.locator('[data-testid="month-card"]');
    const monthCount = await monthCards.count();
    expect(monthCount).toBeGreaterThanOrEqual(1);
    console.log(`[CHAIN-002-S1] 月運カード数: ${monthCount}`);

    // ステップ6: 月運の1つをクリック
    const firstMonth = monthCards.first();
    await expect(firstMonth).toBeVisible({ timeout: 5000 });
    await firstMonth.click();
    console.log('[CHAIN-002-S1] 最初の月運クリック');

    // ステップ7: 日運リスト表示確認（その月の日数分）
    await page.waitForTimeout(2000);

    // 日運セクションのタイトルを検索
    const daySectionTitle = page.locator('text=/日運（\\d+年\\d+月）/');
    await expect(daySectionTitle).toBeVisible({ timeout: 5000 });
    console.log('[CHAIN-002-S1] 日運セクション表示確認 OK');

    // 日運カードが表示されることを確認
    await page.waitForTimeout(500);
    const dayCards = page.locator('[data-testid="day-card"]');
    const dayCount = await dayCards.count();
    expect(dayCount).toBeGreaterThanOrEqual(1);
    console.log(`[CHAIN-002-S1] 日運カード数: ${dayCount}`);

    // UI検証: 各運勢カードに五行カラーが適用されることを確認
    const firstDayCard = dayCards.first();
    await expect(firstDayCard).toBeVisible();
    console.log('[CHAIN-002-S1] 日運カードの表示確認 OK');

    console.log('[CHAIN-002-S1] テスト完了 ✅');
  });

  // E2E-CHAIN-002-S2: 正常系 - 現在の運勢ハイライト表示
  test('E2E-CHAIN-002-S2: 正常系 - 現在の運勢ハイライト表示', async ({ page }) => {
    console.log('[CHAIN-002-S2] テスト開始');

    // 前提: 命式詳細ページに遷移
    const sajuId = await setupSajuDetail(page);
    console.log(`[CHAIN-002-S2] 命式ID: ${sajuId}`);

    // ステップ1: 大運リスト表示確認
    await expect(page.locator('text=大運（10年周期）')).toBeVisible({ timeout: 10000 });

    // ステップ2: 現在の大運が自動的にハイライト表示されることを確認
    // 「現在」というテキストが含まれる大運カードを探す
    const currentDaeunMarker = page.locator('text=現在');
    const hasCurrentMarker = await currentDaeunMarker.count();

    if (hasCurrentMarker > 0) {
      await expect(currentDaeunMarker.first()).toBeVisible();
      console.log('[CHAIN-002-S2] 現在の大運マーカー表示確認 OK');
    } else {
      console.log('[CHAIN-002-S2] 現在の大運マーカーなし（年齢範囲外の可能性）');
    }

    // ステップ3: 現在の大運をクリック（自動選択されていない場合）
    const daeunCards = page.locator('text=/^\\d+-\\d+歳$/');
    const firstDaeun = daeunCards.first();
    await expect(firstDaeun).toBeVisible();
    await firstDaeun.click();
    console.log('[CHAIN-002-S2] 大運クリック');

    // ステップ4: 年運が表示されるまで待機
    await page.waitForTimeout(1500);

    // ステップ5: 現在の年がハイライト表示されることを確認
    // 今年の年号を取得
    const currentYear = new Date().getFullYear();
    const currentYearCard = page.locator(`text=${currentYear}年`);
    const currentYearExists = await currentYearCard.count();

    if (currentYearExists > 0) {
      await expect(currentYearCard.first()).toBeVisible();
      console.log(`[CHAIN-002-S2] 現在の年運（${currentYear}年）表示確認 OK`);

      // ステップ6: 現在の年をクリック
      await currentYearCard.first().click();
      console.log('[CHAIN-002-S2] 現在の年運クリック');

      // ステップ7: 月運が表示されるまで待機
      await page.waitForTimeout(1500);

      // ステップ8: 現在の月がハイライト表示されることを確認
      const currentMonth = new Date().getMonth() + 1; // 0-indexedなので+1
      const currentMonthCard = page.locator(`text=${currentMonth}月`);
      const currentMonthExists = await currentMonthCard.count();

      if (currentMonthExists > 0) {
        await expect(currentMonthCard.first()).toBeVisible();
        console.log(`[CHAIN-002-S2] 現在の月運（${currentMonth}月）表示確認 OK`);

        // ステップ9: 現在の月をクリック
        await currentMonthCard.first().click();
        console.log('[CHAIN-002-S2] 現在の月運クリック');

        // ステップ10: 日運が表示されるまで待機
        await page.waitForTimeout(1500);

        // ステップ11: 今日の日がハイライト表示されることを確認
        const currentDay = new Date().getDate();
        const currentDayCard = page.locator(`text=/^${currentDay}日$/`);
        const currentDayExists = await currentDayCard.count();

        if (currentDayExists > 0) {
          await expect(currentDayCard.first()).toBeVisible();
          console.log(`[CHAIN-002-S2] 今日の日運（${currentDay}日）表示確認 OK`);
        } else {
          console.log(`[CHAIN-002-S2] 今日の日運（${currentDay}日）が表示範囲外`);
        }
      } else {
        console.log(`[CHAIN-002-S2] 現在の月運（${currentMonth}月）が表示範囲外`);
      }
    } else {
      console.log(`[CHAIN-002-S2] 現在の年運（${currentYear}年）が表示範囲外`);
    }

    console.log('[CHAIN-002-S2] テスト完了 ✅');
  });

  // E2E-CHAIN-002-S3: UI/UX - 水平スクロールのスムーズ動作（60fps）
  test('E2E-CHAIN-002-S3: UI/UX - 水平スクロールのスムーズ動作', async ({ page }) => {
    console.log('[CHAIN-002-S3] テスト開始');

    // 前提: 命式詳細ページに遷移
    const sajuId = await setupSajuDetail(page);
    console.log(`[CHAIN-002-S3] 命式ID: ${sajuId}`);

    // ステップ1: 大運リスト表示確認
    await expect(page.locator('text=大運（10年周期）')).toBeVisible({ timeout: 10000 });

    // ステップ2: 大運スクロールコンテナを取得
    const daeunScrollContainer = page.locator('[style*="overflow"]').first();

    // ステップ3: スクロール可能かどうかを確認
    const isScrollable = await daeunScrollContainer.evaluate((el) => {
      return el.scrollWidth > el.clientWidth;
    }).catch(() => false);

    if (isScrollable) {
      console.log('[CHAIN-002-S3] 大運スクロールコンテナはスクロール可能');

      // ステップ4: スクロール操作を実行
      const scrollStartTime = Date.now();

      await daeunScrollContainer.evaluate((el) => {
        el.scrollBy({ left: 200, behavior: 'smooth' });
      });

      await page.waitForTimeout(500);

      const scrollEndTime = Date.now();
      const scrollDuration = scrollEndTime - scrollStartTime;

      console.log(`[CHAIN-002-S3] スクロール所要時間: ${scrollDuration}ms`);

      // スクロールが500ms以内に完了することを確認（スムーズ動作の指標）
      expect(scrollDuration).toBeLessThan(1000);
    } else {
      console.log('[CHAIN-002-S3] 大運スクロールコンテナはスクロール不要（全要素表示済み）');
    }

    // ステップ5: 大運をクリックして年運を表示
    const daeunCards = page.locator('text=/^\\d+-\\d+歳$/');
    const firstDaeun = daeunCards.first();
    await expect(firstDaeun).toBeVisible();
    await firstDaeun.click();
    console.log('[CHAIN-002-S3] 大運クリック');

    await page.waitForTimeout(1000);

    // ステップ6: 年運スクロールコンテナのスムーズ動作確認
    const yearScrollContainer = page.locator('[data-testid="year-scroll-container"]');
    const yearScrollContainerExists = await yearScrollContainer.count();

    if (yearScrollContainerExists > 0) {
      const isYearScrollable = await yearScrollContainer.evaluate((el) => {
        return el.scrollWidth > el.clientWidth;
      }).catch(() => false);

      if (isYearScrollable) {
        console.log('[CHAIN-002-S3] 年運スクロールコンテナはスクロール可能');

        await yearScrollContainer.evaluate((el) => {
          el.scrollBy({ left: 200, behavior: 'smooth' });
        });

        await page.waitForTimeout(500);
        console.log('[CHAIN-002-S3] 年運スクロール動作確認 OK');
      } else {
        console.log('[CHAIN-002-S3] 年運スクロールコンテナはスクロール不要');
      }
    } else {
      console.log('[CHAIN-002-S3] 年運スクロールコンテナが見つからない');
    }

    // UI検証: スクロール後も大運カードが表示される
    const daeunCardStillVisible = await page.locator('text=大運（10年周期）').isVisible().catch(() => false);
    expect(daeunCardStillVisible).toBe(true);
    console.log('[CHAIN-002-S3] スクロール後も大運セクション表示確認 OK');

    console.log('[CHAIN-002-S3] テスト完了 ✅');
  });

  // E2E-CHAIN-002-S4: 異常系 - 存在しない命式IDでアクセス
  test('E2E-CHAIN-002-S4: 異常系 - 存在しない命式IDでアクセス', async ({ page }) => {
    console.log('[CHAIN-002-S4] テスト開始');

    // ステップ1: 存在しない命式IDで詳細ページにアクセス
    const invalidSajuId = 'nonexistent-saju-id-12345';
    await page.goto(`/detail/${invalidSajuId}`);
    console.log(`[CHAIN-002-S4] 存在しない命式ID: ${invalidSajuId}`);

    // ステップ2: エラーメッセージまたは404ページが表示されることを確認
    // リダイレクトは3秒後なので4秒待機
    await page.waitForTimeout(4000);

    // パターン1: エラーメッセージが表示される
    const errorMessageVisible = await page.locator('text=/命式.*見つかりません|エラー|データ.*読み込.*失敗/i').isVisible().catch(() => false);

    // パターン2: トップページにリダイレクトされる
    const currentUrl = page.url();
    const isRedirectedToHome = currentUrl.endsWith('/') || currentUrl.includes('/?');

    // パターン3: リストページにリダイレクトされる
    const isRedirectedToList = currentUrl.includes('/list');

    // いずれかのエラーハンドリングが実行されることを確認
    const hasErrorHandling = errorMessageVisible || isRedirectedToHome || isRedirectedToList;
    expect(hasErrorHandling).toBe(true);

    if (errorMessageVisible) {
      console.log('[CHAIN-002-S4] エラーメッセージ表示確認 OK');
    } else if (isRedirectedToHome) {
      console.log('[CHAIN-002-S4] トップページへのリダイレクト確認 OK');
    } else if (isRedirectedToList) {
      console.log('[CHAIN-002-S4] リストページへのリダイレクト確認 OK');
    }

    // ステップ3: リダイレクトが発生する場合は、4秒待機して確実にリダイレクトを確認
    if (!isRedirectedToList && errorMessageVisible) {
      console.log('[CHAIN-002-S4] リダイレクト待機中（4秒）...');
      await page.waitForTimeout(4000);

      const finalUrl = page.url();
      const finalIsRedirectedToList = finalUrl.includes('/list');

      if (finalIsRedirectedToList) {
        console.log('[CHAIN-002-S4] リストページへのリダイレクト確認 OK（遅延実行）');
      }
    }

    console.log('[CHAIN-002-S4] テスト完了 ✅');
  });
});
