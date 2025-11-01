/**
 * ゴールデン四柱推命アプリケーション - カラーパレット定義
 * エレガントゴールドテーマ
 */

import type { PaletteOptions } from '@mui/material/styles';

// ゴールドパレット（メインカラー）
export const GOLD_PALETTE = {
  PRIMARY_GOLD: '#D4AF37',
  LIGHT_GOLD: '#F4E8C1',
  DARK_GOLD: '#B8941C',
} as const;

// 五行カラー（四柱推命用）
export const WUXING_COLORS = {
  WOOD: '#4CAF50',    // 木（緑）
  FIRE: '#F44336',    // 火（赤）
  EARTH: '#FFB300',   // 土（黄/オレンジ）
  METAL: '#BDBDBD',   // 金（グレー/白）
  WATER: '#424242',   // 水（黒/ダークグレー）
} as const;

// 吉凶カラー（運勢表示用）
export const FORTUNE_COLORS = {
  GREAT_FORTUNE: '#FFD700',       // 大吉（ゴールド）
  FORTUNE: '#4CAF50',             // 吉（緑）
  NEUTRAL: '#9E9E9E',             // 平（グレー）
  MISFORTUNE: '#FF9800',          // 凶（オレンジ）
  GREAT_MISFORTUNE: '#F44336',    // 大凶（赤）
} as const;

// MUIパレット設定
export const palette: PaletteOptions = {
  mode: 'light',
  primary: {
    main: GOLD_PALETTE.PRIMARY_GOLD,
    light: GOLD_PALETTE.LIGHT_GOLD,
    dark: GOLD_PALETTE.DARK_GOLD,
    contrastText: '#FFFFFF',
  },
  secondary: {
    main: '#424242',
    light: '#6D6D6D',
    dark: '#1B1B1B',
    contrastText: '#FFFFFF',
  },
  error: {
    main: FORTUNE_COLORS.GREAT_MISFORTUNE,
  },
  warning: {
    main: FORTUNE_COLORS.MISFORTUNE,
  },
  info: {
    main: '#2196F3',
  },
  success: {
    main: FORTUNE_COLORS.FORTUNE,
  },
  background: {
    default: '#FFFFFF',
    paper: '#FAFAFA',
  },
  text: {
    primary: '#212121',
    secondary: '#757575',
    disabled: '#BDBDBD',
  },
};

// TypeScript型拡張用（カスタムカラー）
declare module '@mui/material/styles' {
  interface Palette {
    gold: typeof GOLD_PALETTE;
    wuxing: typeof WUXING_COLORS;
    fortune: typeof FORTUNE_COLORS;
  }
  interface PaletteOptions {
    gold?: typeof GOLD_PALETTE;
    wuxing?: typeof WUXING_COLORS;
    fortune?: typeof FORTUNE_COLORS;
  }
}

// カスタムパレット拡張
export const customPalette = {
  gold: GOLD_PALETTE,
  wuxing: WUXING_COLORS,
  fortune: FORTUNE_COLORS,
};
