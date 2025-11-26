// CHAIN-001: 命式計算全体フロー - E2Eテスト
// E2E仕様書: docs/e2e-specs/CHAIN-001-saju-calculation-flow.md

import { test, expect } from '@playwright/test';

// E2E-CHAIN-001-S1: 正常系 - 男性、1990年3月15日14時30分生まれ
test('E2E-CHAIN-001-S1: 正常系 - 男性、1990年3月15日14時30分生まれ', async ({ page }) => {
  // ブラウザコンソールログを収集
  const consoleLogs: Array<{type: string, text: string}> = [];
  page.on('console', (msg) => {
    consoleLogs.push({
      type: msg.type(),
      text: msg.text()
    });
  });

  // ネットワークログを収集
  const networkLogs: Array<{url: string, status: number, method: string}> = [];
  page.on('response', (response) => {
    networkLogs.push({
      url: response.url(),
      status: response.status(),
      method: response.request().method()
    });
  });

  // 1. トップページにアクセス
  await page.goto('http://localhost:3247/');
  await expect(page).toHaveURL('http://localhost:3247/');

  // 2-5. 入力フォーム入力
  // 名前入力
  const nameInput = page.locator('input[data-testid="name"]');
  await nameInput.fill('テスト太郎');

  // 生年月日: spinbutton要素をクリア→入力（MUI DatePickerの実装）
  const yearInput = page.getByRole('spinbutton', { name: 'Year' });
  await yearInput.click();
  await yearInput.clear();
  await yearInput.fill('1990');

  const monthInput = page.getByRole('spinbutton', { name: 'Month' });
  await monthInput.click();
  await monthInput.clear();
  await monthInput.fill('03');

  const dayInput = page.getByRole('spinbutton', { name: 'Day' });
  await dayInput.click();
  await dayInput.clear();
  await dayInput.fill('15');

  // 時刻: spinbutton要素をクリア→入力（MUI TimePickerの実装）
  const hoursInput = page.getByRole('spinbutton', { name: 'Hours' });
  await hoursInput.click();
  await hoursInput.clear();
  await hoursInput.fill('14');

  const minutesInput = page.getByRole('spinbutton', { name: 'Minutes' });
  await minutesInput.click();
  await minutesInput.clear();
  await minutesInput.fill('30');

  // 性別: 男性を選択
  await page.locator('[data-testid="gender-male"]').click();

  // 6. 計算ボタンクリック前にAPI待機を開始
  const calculateResponsePromise = page.waitForResponse(
    res => res.url().includes('/api/saju/calculate') && res.request().method() === 'POST',
    { timeout: 30000 }
  );

  const calculateButton = page.locator('button:has-text("命式を計算")');
  await calculateButton.click();

  // API呼び出し確認: POST /api/saju/calculate
  const calculateResponse = await calculateResponsePromise;

  expect(calculateResponse.status()).toBe(200);
  const sajuData = await calculateResponse.json();

  // レスポンス検証
  expect(sajuData.id).toBeTruthy();
  expect(sajuData.name).toBe('テスト太郎');
  expect(sajuData.birthDatetime).toBe('1990-03-15T14:30:00+09:00');
  expect(sajuData.gender).toBe('male');
  expect(sajuData.yearStem).toBe('庚');
  expect(sajuData.yearBranch).toBe('午');
  expect(sajuData.monthStem).toBe('己');
  expect(sajuData.monthBranch).toBe('卯');
  expect(sajuData.isForward).toBe(true); // 男性 + 陽干(庚) → 順行
  expect(sajuData.daeunList).toBeInstanceOf(Array);
  expect(sajuData.daeunList.length).toBeGreaterThan(0);
  expect(['大吉', '吉', '平', '凶', '大凶']).toContain(sajuData.fortuneLevel);

  // 8. ゲストモード: LocalStorageに保存されることを確認
  const savedData = await page.evaluate(() => {
    const data = localStorage.getItem('saju_data');
    return data ? JSON.parse(data) : null;
  });

  expect(savedData).toBeTruthy();
  expect(Array.isArray(savedData)).toBe(true);
  expect(savedData.length).toBeGreaterThan(0);

  // 保存されたデータに命式IDが含まれることを確認
  const savedSaju = savedData.find((item: any) => item.id === sajuData.id);
  expect(savedSaju).toBeTruthy();
  expect(savedSaju.id).toBe(sajuData.id);

  // 9. リダイレクト確認（詳細ページに遷移）
  await page.waitForURL(`http://localhost:3247/detail/${sajuData.id}`, { timeout: 10000 });
  await expect(page).toHaveURL(`http://localhost:3247/detail/${sajuData.id}`);

  // テスト成功時はコンソールログとネットワークログを出力（デバッグ用）
  console.log('=== Test Completed Successfully ===');
  console.log('Browser Console Logs:', consoleLogs.length, 'entries');
  console.log('Network Logs:', networkLogs.length, 'requests');
});
