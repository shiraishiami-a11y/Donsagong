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

// 吉凶レベルからカラーを取得
export const getFortuneColor = (fortuneLevel: FortuneLevel): string => {
  const colorMap: Record<FortuneLevel, string> = {
    '大吉': 'linear-gradient(45deg, #FFD700, #FFA500)',
    '吉': 'linear-gradient(45deg, #4CAF50, #66bb6a)',
    '平': 'linear-gradient(45deg, #9E9E9E, #BDBDBD)',
    '凶': 'linear-gradient(45deg, #FF9800, #ffb74d)',
    '大凶': 'linear-gradient(45deg, #F44336, #ef5350)',
  };

  return colorMap[fortuneLevel];
};

// 吉凶レベルからアイコンを取得
export const getFortuneIcon = (fortuneLevel: FortuneLevel): string => {
  const iconMap: Record<FortuneLevel, string> = {
    '大吉': 'star',
    '吉': 'thumb_up',
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
  const date = new Date(isoString);
  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  const day = date.getDate();
  const hour = date.getHours();
  const minute = date.getMinutes();

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
