/**
 * ゴールデン四柱推命 - 命式詳細ページ v2
 * 韓国アプリ風水平スクロールインタラクション
 */

// ========== サンプルデータ ==========

// 五行マッピング
const elementMap = {
  '甲': 'wood', '乙': 'wood',
  '丙': 'fire', '丁': 'fire',
  '戊': 'earth', '己': 'earth',
  '庚': 'metal', '辛': 'metal',
  '壬': 'water', '癸': 'water',
  '寅': 'wood', '卯': 'wood', '辰': 'earth',
  '巳': 'fire', '午': 'fire', '未': 'earth',
  '申': 'metal', '酉': 'metal', '戌': 'earth',
  '亥': 'water', '子': 'water', '丑': 'earth'
};

// 吉凶アイコンマッピング
const fortuneIcons = {
  1: '🔴', // 大凶
  2: '🟠', // 凶
  3: '⚪', // 平
  4: '🟢', // 吉
  5: '⭐' // 大吉
};

// 大運サンプルデータ（10年周期）
const sampleDaeunData = [
  { startAge: 8, endAge: 17, stem: '丙', branch: '戌', sipsin: '偏印', fortuneLevel: 3, isCurrent: false },
  { startAge: 18, endAge: 27, stem: '丁', branch: '亥', sipsin: '正印', fortuneLevel: 2, isCurrent: false },
  { startAge: 28, endAge: 37, stem: '戊', branch: '子', sipsin: '偏官', fortuneLevel: 4, isCurrent: true },
  { startAge: 38, endAge: 47, stem: '己', branch: '丑', sipsin: '正官', fortuneLevel: 3, isCurrent: false },
  { startAge: 48, endAge: 57, stem: '庚', branch: '寅', sipsin: '偏財', fortuneLevel: 5, isCurrent: false },
  { startAge: 58, endAge: 67, stem: '辛', branch: '卯', sipsin: '正財', fortuneLevel: 4, isCurrent: false },
  { startAge: 68, endAge: 77, stem: '壬', branch: '辰', sipsin: '食神', fortuneLevel: 3, isCurrent: false },
  { startAge: 78, endAge: 87, stem: '癸', branch: '巳', sipsin: '傷官', fortuneLevel: 2, isCurrent: false }
];

// 年運サンプルデータ生成関数（大運期間28-37歳）
function generateYearData(startAge, endAge) {
  const years = [];
  const currentYear = 2025;
  const currentAge = 35;
  const birthYear = currentYear - currentAge;

  const stems = ['戊', '己', '庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁'];
  const branches = ['戌', '亥', '子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉'];
  const sipsins = ['偏官', '正官', '偏財', '正財', '食神', '傷官', '比肩', '劫財'];

  for (let age = startAge; age <= endAge; age++) {
    const year = birthYear + age;
    const stemIndex = (year - 4) % 10;
    const branchIndex = (year - 4) % 12;

    years.push({
      year: year,
      age: age,
      stem: stems[stemIndex],
      branch: branches[branchIndex],
      sipsin: sipsins[age % 8],
      fortuneLevel: ((age % 5) + 1),
      isCurrent: age === currentAge
    });
  }

  return years;
}

// 月運サンプルデータ生成関数（12ヶ月）
function generateMonthData(year) {
  const months = [];
  const currentMonth = new Date().getMonth() + 1;
  const currentYear = new Date().getFullYear();

  const stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
  const branches = ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑'];
  const sipsins = ['比肩', '劫財', '食神', '傷官', '偏財', '正財', '偏官', '正官', '偏印', '正印'];

  for (let month = 1; month <= 12; month++) {
    months.push({
      month: month,
      stem: stems[month % 10],
      branch: branches[month % 12],
      sipsin: sipsins[month % 10],
      fortuneLevel: ((month % 5) + 1),
      isCurrent: (year === currentYear && month === currentMonth)
    });
  }

  return months;
}

// 日運サンプルデータ生成関数（月の日数に応じて）
function generateDayData(year, month) {
  const days = [];
  const daysInMonth = new Date(year, month, 0).getDate();
  const currentDay = new Date().getDate();
  const currentMonth = new Date().getMonth() + 1;
  const currentYear = new Date().getFullYear();

  const stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
  const branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
  const sipsins = ['比肩', '劫財', '食神', '傷官', '偏財', '正財', '偏官', '正官', '偏印', '正印'];

  for (let day = 1; day <= daysInMonth; day++) {
    days.push({
      day: day,
      stem: stems[day % 10],
      branch: branches[day % 12],
      sipsin: sipsins[day % 10],
      fortuneLevel: ((day % 5) + 1),
      isToday: (year === currentYear && month === currentMonth && day === currentDay)
    });
  }

  return days;
}

// ========== 状態管理 ==========
let selectedDaeun = null;
let selectedYear = null;
let selectedMonth = null;

// ========== DOM操作関数 ==========

/**
 * 五行に対応するクラス名を取得
 */
function getElementClass(character) {
  return elementMap[character] || 'earth';
}

/**
 * 吉凶レベルに対応するアイコンを取得
 */
function getFortuneIcon(level) {
  return fortuneIcons[level] || '⚪';
}

/**
 * 大運カードを生成
 */
function createDaeunCard(daeun) {
  const card = document.createElement('div');
  card.className = `fortune-card daeun-card fortune-level-${daeun.fortuneLevel}`;
  if (daeun.isCurrent) {
    card.classList.add('selected');
  }

  card.innerHTML = `
    ${daeun.isCurrent ? '<span class="current-badge">現在</span>' : ''}
    <div class="age-range">${daeun.startAge}-${daeun.endAge}歳</div>
    <div class="daeun-characters">
      <div class="daeun-stem ${getElementClass(daeun.stem)}">${daeun.stem}</div>
      <div class="daeun-branch ${getElementClass(daeun.branch)}">${daeun.branch}</div>
    </div>
    <div class="sipsin">${daeun.sipsin}</div>
    <div class="fortune-icon">${getFortuneIcon(daeun.fortuneLevel)}</div>
  `;

  card.addEventListener('click', () => handleDaeunClick(daeun, card));

  return card;
}

/**
 * 年運カードを生成
 */
function createYearCard(year) {
  const card = document.createElement('div');
  card.className = `fortune-card year-card fortune-level-${year.fortuneLevel}`;
  if (year.isCurrent) {
    card.classList.add('selected');
  }

  card.innerHTML = `
    ${year.isCurrent ? '<span class="current-badge">現在</span>' : ''}
    <div class="year-number">${year.year}年</div>
    <div class="year-characters">
      <div class="year-stem ${getElementClass(year.stem)}">${year.stem}</div>
      <div class="year-branch ${getElementClass(year.branch)}">${year.branch}</div>
    </div>
    <div class="sipsin">${year.sipsin}</div>
    <div class="fortune-icon">${getFortuneIcon(year.fortuneLevel)}</div>
  `;

  card.addEventListener('click', () => handleYearClick(year, card));

  return card;
}

/**
 * 月運カードを生成
 */
function createMonthCard(month) {
  const card = document.createElement('div');
  card.className = `fortune-card month-card fortune-level-${month.fortuneLevel}`;
  if (month.isCurrent) {
    card.classList.add('selected');
  }

  card.innerHTML = `
    ${month.isCurrent ? '<span class="current-badge">現在</span>' : ''}
    <div class="month-number">${month.month}月</div>
    <div class="month-characters">
      <div class="month-stem ${getElementClass(month.stem)}">${month.stem}</div>
      <div class="month-branch ${getElementClass(month.branch)}">${month.branch}</div>
    </div>
    <div class="sipsin">${month.sipsin}</div>
    <div class="fortune-icon">${getFortuneIcon(month.fortuneLevel)}</div>
  `;

  card.addEventListener('click', () => handleMonthClick(month, card));

  return card;
}

/**
 * 日運カードを生成
 */
function createDayCard(day) {
  const card = document.createElement('div');
  card.className = `fortune-card day-card fortune-level-${day.fortuneLevel}`;
  if (day.isToday) {
    card.classList.add('selected');
  }

  card.innerHTML = `
    ${day.isToday ? '<span class="today-badge">今日</span>' : ''}
    <div class="day-number">${day.day}日</div>
    <div class="day-characters">
      <div class="day-stem ${getElementClass(day.stem)}">${day.stem}</div>
      <div class="day-branch ${getElementClass(day.branch)}">${day.branch}</div>
    </div>
    <div class="sipsin">${day.sipsin}</div>
    <div class="fortune-icon">${getFortuneIcon(day.fortuneLevel)}</div>
  `;

  return card;
}

// ========== イベントハンドラー ==========

/**
 * 大運カードクリック時の処理
 */
function handleDaeunClick(daeun, clickedCard) {
  selectedDaeun = daeun;

  // 全ての大運カードからselectedクラスを削除
  document.querySelectorAll('.daeun-card').forEach(card => {
    card.classList.remove('selected');
  });

  // クリックされたカードにselectedクラスを追加
  clickedCard.classList.add('selected');

  // 年運セクションを表示
  const yearSection = document.getElementById('year-section');
  const yearSubtitle = document.getElementById('year-subtitle');
  const yearScroll = document.getElementById('year-scroll');

  yearSection.style.display = 'block';
  yearSubtitle.textContent = `${daeun.startAge}-${daeun.endAge}歳 (${daeun.stem}${daeun.branch}) の年別運勢`;

  // 年運データを生成して表示
  const yearData = generateYearData(daeun.startAge, daeun.endAge);
  yearScroll.innerHTML = '';
  yearData.forEach(year => {
    yearScroll.appendChild(createYearCard(year));
  });

  // 月運・日運セクションを非表示
  document.getElementById('month-section').style.display = 'none';
  document.getElementById('day-section').style.display = 'none';

  // スムーズスクロール
  yearSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * 年運カードクリック時の処理
 */
function handleYearClick(year, clickedCard) {
  selectedYear = year;

  // 全ての年運カードからselectedクラスを削除
  document.querySelectorAll('.year-card').forEach(card => {
    card.classList.remove('selected');
  });

  // クリックされたカードにselectedクラスを追加
  clickedCard.classList.add('selected');

  // 月運セクションを表示
  const monthSection = document.getElementById('month-section');
  const monthSubtitle = document.getElementById('month-subtitle');
  const monthScroll = document.getElementById('month-scroll');

  monthSection.style.display = 'block';
  monthSubtitle.textContent = `${year.year}年 (${year.stem}${year.branch}) の月別運勢`;

  // 月運データを生成して表示
  const monthData = generateMonthData(year.year);
  monthScroll.innerHTML = '';
  monthData.forEach(month => {
    monthScroll.appendChild(createMonthCard(month));
  });

  // 日運セクションを非表示
  document.getElementById('day-section').style.display = 'none';

  // スムーズスクロール
  monthSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * 月運カードクリック時の処理
 */
function handleMonthClick(month, clickedCard) {
  selectedMonth = month;

  // 全ての月運カードからselectedクラスを削除
  document.querySelectorAll('.month-card').forEach(card => {
    card.classList.remove('selected');
  });

  // クリックされたカードにselectedクラスを追加
  clickedCard.classList.add('selected');

  // 日運セクションを表示
  const daySection = document.getElementById('day-section');
  const daySubtitle = document.getElementById('day-subtitle');
  const dayScroll = document.getElementById('day-scroll');

  daySection.style.display = 'block';
  daySubtitle.textContent = `${selectedYear.year}年${month.month}月 (${month.stem}${month.branch}) の日別運勢`;

  // 日運データを生成して表示
  const dayData = generateDayData(selectedYear.year, month.month);
  dayScroll.innerHTML = '';
  dayData.forEach(day => {
    dayScroll.appendChild(createDayCard(day));
  });

  // スムーズスクロール
  daySection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// ========== 初期化 ==========

/**
 * ページ初期化
 */
function initializePage() {
  // 大運データを表示
  const daeunScroll = document.getElementById('daeun-scroll');
  sampleDaeunData.forEach(daeun => {
    daeunScroll.appendChild(createDaeunCard(daeun));
  });

  // 現在の大運を自動的に選択して年運を表示（オプション）
  const currentDaeun = sampleDaeunData.find(d => d.isCurrent);
  if (currentDaeun) {
    const currentCard = daeunScroll.querySelector('.daeun-card.selected');
    if (currentCard) {
      // 少し遅延させて自動展開（UX向上）
      setTimeout(() => {
        handleDaeunClick(currentDaeun, currentCard);
      }, 500);
    }
  }

  console.log('✅ ページ初期化完了');
  console.log('📊 大運データ:', sampleDaeunData.length, '件');
}

// DOM読み込み完了後に初期化
document.addEventListener('DOMContentLoaded', initializePage);
