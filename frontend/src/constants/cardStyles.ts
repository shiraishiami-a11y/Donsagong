// 全セクション共通の四柱推命カードスタイル定数
// 2025年11月9日: カードサイズ統一化（「今日の運」を基準）

export const UNIFIED_CARD_STYLES = {
  // カード全体のサイズ
  card: {
    minWidth: { xs: '130px', sm: '146px', md: '166px' }, // pxを文字列で明示（ブラウザ互換性のため）
    width: { xs: '130px', sm: '146px', md: '166px' }, // widthを明示的に設定
    padding: { xs: '8px', sm: '12px' },
    borderRadius: '8px',
  },

  // 天干・地支ボックスのサイズ（大運・年月日運・今日の運用）
  pillar: {
    width: { xs: '56px', sm: '70px', md: '80px' },
    height: { xs: '56px', sm: '70px', md: '80px' },
    borderRadius: { xs: '8px', sm: '10px' },
  },

  // フォントサイズ
  fontSize: {
    pillarChar: { xs: '24px', sm: '30px', md: '36px' }, // 天干・地支文字
    label: { xs: '12px', sm: '14px' }, // ラベル（年月日、年齢範囲など）
    fortune: { xs: '11px', sm: '12px' }, // 吉凶バッジ
  },

  // 間隔
  spacing: {
    gap: { xs: '10px', sm: '12px', md: '16px' }, // カード間
    pillarGap: '6px', // 天干・地支間
  },
} as const;

// 命式（四柱）専用スタイル - 他より1.5倍大きい
export const MAIN_PILLAR_STYLES = {
  // 天干・地支ボックスのサイズ（命式専用・1.5倍）
  pillar: {
    width: { xs: '84px', sm: '105px', md: '120px' }, // 56*1.5, 70*1.5, 80*1.5
    height: { xs: '84px', sm: '105px', md: '120px' },
    borderRadius: { xs: '12px', sm: '15px' },
  },

  // フォントサイズ（命式専用・1.5倍）
  fontSize: {
    pillarChar: { xs: '36px', sm: '45px', md: '54px' }, // 24*1.5, 30*1.5, 36*1.5
    label: { xs: '18px', sm: '21px' }, // 12*1.5, 14*1.5
  },

  // 間隔（命式専用・1.5倍）
  spacing: {
    gap: { xs: '15px', sm: '18px', md: '24px' }, // 10*1.5, 12*1.5, 16*1.5
    pillarGap: '9px', // 6*1.5
  },
} as const;
