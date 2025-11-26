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

// 五行カラー（ブランディングガイドライン準拠）
export const WUXING_COLORS = {
  WOOD: '#388E3C',    // 木（緑）- 起業運
  FIRE: '#D32F2F',    // 火（赤）- メインブランディングと兼用
  EARTH: '#F57C00',   // 土（オレンジ）- 人脈運
  METAL: '#BDBDBD',   // 金（グレー）- 投資運
  WATER: '#1976D2',   // 水（青）- 仕事運
} as const;

// 吉凶カラー（運勢表示用・五行カラー準拠）
export const FORTUNE_COLORS = {
  GREAT_FORTUNE: '#FFD700',       // 大吉（ゴールド）
  FORTUNE: '#388E3C',             // 吉（緑・木の色）
  NEUTRAL: '#757575',             // 平（グレー）
  MISFORTUNE: '#F57C00',          // 凶（オレンジ・土の色）
  GREAT_MISFORTUNE: '#D32F2F',    // 大凶（赤・火の色）
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
