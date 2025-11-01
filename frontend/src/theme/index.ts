/**
 * ゴールデン四柱推命アプリケーション - メインテーマファイル
 * エレガントゴールドテーマ
 */

import { createTheme } from '@mui/material/styles';
import type { Theme } from '@mui/material/styles';
import { palette, customPalette } from './palette';
import { typography } from './typography';
import { components } from './components';

// MUIテーマ作成
const theme: Theme = createTheme({
  palette: {
    ...palette,
    ...customPalette,
  },
  typography,
  components,
  shape: {
    borderRadius: 8,
  },
  spacing: 8,
  breakpoints: {
    values: {
      xs: 0,
      sm: 600,
      md: 960,
      lg: 1280,
      xl: 1920,
    },
  },
  shadows: [
    'none',
    '0 2px 4px rgba(0, 0, 0, 0.05)',
    '0 4px 8px rgba(0, 0, 0, 0.08)',
    '0 6px 12px rgba(0, 0, 0, 0.1)',
    '0 8px 16px rgba(0, 0, 0, 0.12)',
    '0 10px 20px rgba(0, 0, 0, 0.14)',
    '0 12px 24px rgba(0, 0, 0, 0.16)',
    '0 14px 28px rgba(0, 0, 0, 0.18)',
    '0 16px 32px rgba(0, 0, 0, 0.2)',
    '0 18px 36px rgba(0, 0, 0, 0.22)',
    '0 20px 40px rgba(0, 0, 0, 0.24)',
    '0 22px 44px rgba(0, 0, 0, 0.26)',
    '0 24px 48px rgba(0, 0, 0, 0.28)',
    '0 26px 52px rgba(0, 0, 0, 0.3)',
    '0 28px 56px rgba(0, 0, 0, 0.32)',
    '0 30px 60px rgba(0, 0, 0, 0.34)',
    '0 32px 64px rgba(0, 0, 0, 0.36)',
    '0 34px 68px rgba(0, 0, 0, 0.38)',
    '0 36px 72px rgba(0, 0, 0, 0.4)',
    '0 38px 76px rgba(0, 0, 0, 0.42)',
    '0 40px 80px rgba(0, 0, 0, 0.44)',
    '0 42px 84px rgba(0, 0, 0, 0.46)',
    '0 44px 88px rgba(0, 0, 0, 0.48)',
    '0 46px 92px rgba(0, 0, 0, 0.5)',
    '0 48px 96px rgba(0, 0, 0, 0.52)',
  ],
  transitions: {
    duration: {
      shortest: 150,
      shorter: 200,
      short: 250,
      standard: 300,
      complex: 375,
      enteringScreen: 225,
      leavingScreen: 195,
    },
    easing: {
      easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
      easeOut: 'cubic-bezier(0.0, 0, 0.2, 1)',
      easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
      sharp: 'cubic-bezier(0.4, 0, 0.6, 1)',
    },
  },
  zIndex: {
    mobileStepper: 1000,
    fab: 1050,
    speedDial: 1050,
    appBar: 1100,
    drawer: 1200,
    modal: 1300,
    snackbar: 1400,
    tooltip: 1500,
  },
});

export default theme;

// 再エクスポート
export { palette, customPalette } from './palette';
export { typography } from './typography';
export { components } from './components';
export type { Theme };
