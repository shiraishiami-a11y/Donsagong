// 命式関連のヘルパー関数

import type { FiveElement, FortuneLevel } from '../types';

// 五行要素からカラーを取得
export const getElementColor = (element?: FiveElement): string => {
  if (!element) return '#9E9E9E';

  const colorMap: Record<FiveElement, string> = {
    wood: 'linear-gradient(135deg, #4CAF50, #66bb6a)',
    fire: 'linear-gradient(135deg, #F44336, #ef5350)',
    earth: 'linear-gradient(135deg, #FFB300, #ffa726)',
    metal: 'linear-gradient(135deg, #9E9E9E, #BDBDBD)',
    water: 'linear-gradient(135deg, #424242, #616161)',
  };

  return colorMap[element];
};

// 吉凶レベルからカラーを取得（7段階システム対応）
export const getFortuneColor = (fortuneLevel: FortuneLevel): string => {
  const colorMap: Record<FortuneLevel, string> = {
    '大吉': 'linear-gradient(45deg, #FFD700, #FFA500)',
    '吉': 'linear-gradient(45deg, #4CAF50, #66bb6a)',
    '中吉': 'linear-gradient(45deg, #66bb6a, #81c784)',
    '小吉': 'linear-gradient(45deg, #81c784, #a5d6a7)',
    '平': 'linear-gradient(45deg, #9E9E9E, #BDBDBD)',
    '凶': 'linear-gradient(45deg, #FF9800, #ffb74d)',
    '大凶': 'linear-gradient(45deg, #F44336, #ef5350)',
  };

  return colorMap[fortuneLevel];
};

// 吉凶レベルからアイコンを取得（7段階システム対応）
export const getFortuneIcon = (fortuneLevel: FortuneLevel): string => {
  const iconMap: Record<FortuneLevel, string> = {
    '大吉': 'star',
    '吉': 'thumb_up',
    '中吉': 'thumb_up',
    '小吉': 'thumb_up',
    '平': 'remove',
    '凶': 'warning',
    '大凶': 'error',
  };

  return iconMap[fortuneLevel];
};

// 天干から五行要素を判定
export const getStemElement = (stem: string): FiveElement => {
  const stemMap: Record<string, FiveElement> = {
    '甲': 'wood', '乙': 'wood',
    '丙': 'fire', '丁': 'fire',
    '戊': 'earth', '己': 'earth',
    '庚': 'metal', '辛': 'metal',
    '壬': 'water', '癸': 'water',
  };

  return stemMap[stem] || 'earth';
};

// 地支から五行要素を判定
export const getBranchElement = (branch: string): FiveElement => {
  const branchMap: Record<string, FiveElement> = {
    '寅': 'wood', '卯': 'wood',
    '巳': 'fire', '午': 'fire',
    '辰': 'earth', '戌': 'earth', '丑': 'earth', '未': 'earth',
    '申': 'metal', '酉': 'metal',
    '亥': 'water', '子': 'water',
  };

  return branchMap[branch] || 'earth';
};

// 性別を日本語に変換
export const getGenderLabel = (gender: string): string => {
  return gender === 'male' ? '男性' : '女性';
};

// 日付フォーマット（ISO 8601 → 日本語表記）
export const formatBirthDateTime = (isoString: string): string => {
  // ISO文字列から直接パース（タイムゾーン変換を避ける）
  // 形式: "1977-11-07T12:00:00+09:00" または "1977-11-07T12:00:00Z" または "1977-11-07T12:00:00.000+09:00"
  // ミリ秒を含む形式にも対応（6桁まで）
  const match = isoString.match(/^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.\d+)?([+-]\d{2}:\d{2}|Z)?/);

  if (!match) {
    // フォールバック：正規表現にマッチしない場合（異常な形式）
    // この場合、可能な限り日付を抽出するが、完全な正確性は保証できない
    console.warn('[formatBirthDateTime] ISO文字列が標準形式ではありません:', isoString);
    try {
      // 日付部分のみを抽出する試み
      const dateOnlyMatch = isoString.match(/^(\d{4})-(\d{2})-(\d{2})/);
      if (dateOnlyMatch) {
        const year = parseInt(dateOnlyMatch[1], 10);
        const month = parseInt(dateOnlyMatch[2], 10);
        const day = parseInt(dateOnlyMatch[3], 10);
        return `${year}年${month}月${day}日 時間不明`;
      }
      return '日付不明';
    } catch (error) {
      console.error('[formatBirthDateTime] ISO文字列のパースに失敗:', error, 'isoString:', isoString);
      return '日付不明';
    }
  }

  const year = parseInt(match[1], 10);
  const month = parseInt(match[2], 10);
  const day = parseInt(match[3], 10);
  const hour = parseInt(match[4], 10);
  const minute = parseInt(match[5], 10);

  // 時刻を表示（12:00や00:00も正当な時刻として扱う）
  return `${year}年${month}月${day}日 ${hour}:${minute.toString().padStart(2, '0')}`;
};

// 日付フォーマット（ISO 8601 → 日本語日付のみ）
export const formatDate = (isoString: string): string => {
  const date = new Date(isoString);
  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  const day = date.getDate();

  return `${year}年${month}月${day}日`;
};

// 現在年齢を計算
export const calculateCurrentAge = (birthDatetime: string): number => {
  const birth = new Date(birthDatetime);
  const today = new Date();

  let age = today.getFullYear() - birth.getFullYear();
  const monthDiff = today.getMonth() - birth.getMonth();

  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
    age--;
  }

  return age;
};
