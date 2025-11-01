/**
 * ゴールデン四柱推命アプリケーション - MUIコンポーネントカスタマイズ
 * エレガントゴールドテーマ
 */

import type { Components, Theme } from '@mui/material/styles';
import { GOLD_PALETTE } from './palette';

export const components: Components<Theme> = {
  // ボタン
  MuiButton: {
    styleOverrides: {
      root: {
        borderRadius: 8,
        textTransform: 'none',
        fontWeight: 500,
        padding: '8px 20px',
        boxShadow: 'none',
        transition: 'all 0.3s ease',
        '&:hover': {
          boxShadow: '0 4px 12px rgba(212, 175, 55, 0.3)',
          transform: 'translateY(-2px)',
        },
      },
      contained: {
        '&:hover': {
          boxShadow: '0 6px 16px rgba(212, 175, 55, 0.4)',
        },
      },
      containedPrimary: {
        background: `linear-gradient(135deg, ${GOLD_PALETTE.PRIMARY_GOLD} 0%, ${GOLD_PALETTE.DARK_GOLD} 100%)`,
        color: '#FFFFFF',
        '&:hover': {
          background: `linear-gradient(135deg, ${GOLD_PALETTE.DARK_GOLD} 0%, ${GOLD_PALETTE.PRIMARY_GOLD} 100%)`,
        },
      },
      outlined: {
        borderWidth: 2,
        '&:hover': {
          borderWidth: 2,
          backgroundColor: `${GOLD_PALETTE.LIGHT_GOLD}20`,
        },
      },
    },
  },

  // カード
  MuiCard: {
    styleOverrides: {
      root: {
        borderRadius: 16,
        boxShadow: '0 4px 16px rgba(0, 0, 0, 0.08)',
        transition: 'all 0.3s ease',
        '&:hover': {
          boxShadow: '0 8px 24px rgba(212, 175, 55, 0.15)',
          transform: 'translateY(-4px)',
        },
      },
    },
  },

  // ペーパー
  MuiPaper: {
    styleOverrides: {
      root: {
        borderRadius: 12,
      },
      elevation1: {
        boxShadow: '0 2px 8px rgba(0, 0, 0, 0.08)',
      },
      elevation2: {
        boxShadow: '0 4px 16px rgba(0, 0, 0, 0.08)',
      },
      elevation4: {
        boxShadow: '0 8px 24px rgba(0, 0, 0, 0.12)',
      },
    },
  },

  // テキストフィールド
  MuiTextField: {
    styleOverrides: {
      root: {
        '& .MuiOutlinedInput-root': {
          borderRadius: 8,
          transition: 'all 0.3s ease',
          '&:hover': {
            '& .MuiOutlinedInput-notchedOutline': {
              borderColor: GOLD_PALETTE.PRIMARY_GOLD,
            },
          },
          '&.Mui-focused': {
            '& .MuiOutlinedInput-notchedOutline': {
              borderColor: GOLD_PALETTE.PRIMARY_GOLD,
              borderWidth: 2,
            },
          },
        },
      },
    },
  },

  // チップ
  MuiChip: {
    styleOverrides: {
      root: {
        borderRadius: 8,
        fontWeight: 500,
      },
      filled: {
        '&.MuiChip-colorPrimary': {
          background: `linear-gradient(135deg, ${GOLD_PALETTE.PRIMARY_GOLD} 0%, ${GOLD_PALETTE.DARK_GOLD} 100%)`,
          color: '#FFFFFF',
        },
      },
    },
  },

  // タブ
  MuiTab: {
    styleOverrides: {
      root: {
        textTransform: 'none',
        fontWeight: 500,
        fontSize: '1rem',
        '&.Mui-selected': {
          color: GOLD_PALETTE.PRIMARY_GOLD,
          fontWeight: 600,
        },
      },
    },
  },

  // タブインジケーター
  MuiTabs: {
    styleOverrides: {
      indicator: {
        backgroundColor: GOLD_PALETTE.PRIMARY_GOLD,
        height: 3,
        borderRadius: '3px 3px 0 0',
      },
    },
  },

  // アプリバー
  MuiAppBar: {
    styleOverrides: {
      root: {
        boxShadow: '0 2px 8px rgba(0, 0, 0, 0.08)',
      },
      colorPrimary: {
        background: `linear-gradient(135deg, ${GOLD_PALETTE.PRIMARY_GOLD} 0%, ${GOLD_PALETTE.DARK_GOLD} 100%)`,
      },
    },
  },

  // ダイアログ
  MuiDialog: {
    styleOverrides: {
      paper: {
        borderRadius: 16,
        padding: 8,
      },
    },
  },

  // リストアイテムボタン
  MuiListItemButton: {
    styleOverrides: {
      root: {
        borderRadius: 8,
        transition: 'all 0.3s ease',
        '&:hover': {
          backgroundColor: `${GOLD_PALETTE.LIGHT_GOLD}30`,
        },
        '&.Mui-selected': {
          backgroundColor: `${GOLD_PALETTE.LIGHT_GOLD}50`,
          '&:hover': {
            backgroundColor: `${GOLD_PALETTE.LIGHT_GOLD}60`,
          },
        },
      },
    },
  },

  // スイッチ
  MuiSwitch: {
    styleOverrides: {
      root: {
        '& .MuiSwitch-switchBase.Mui-checked': {
          color: GOLD_PALETTE.PRIMARY_GOLD,
          '& + .MuiSwitch-track': {
            backgroundColor: GOLD_PALETTE.PRIMARY_GOLD,
            opacity: 0.5,
          },
        },
      },
    },
  },

  // スライダー
  MuiSlider: {
    styleOverrides: {
      root: {
        color: GOLD_PALETTE.PRIMARY_GOLD,
        '& .MuiSlider-thumb': {
          '&:hover, &.Mui-focusVisible': {
            boxShadow: `0 0 0 8px ${GOLD_PALETTE.PRIMARY_GOLD}30`,
          },
        },
      },
    },
  },

  // リニアプログレス
  MuiLinearProgress: {
    styleOverrides: {
      root: {
        borderRadius: 4,
        height: 8,
      },
      colorPrimary: {
        backgroundColor: `${GOLD_PALETTE.LIGHT_GOLD}50`,
      },
      barColorPrimary: {
        background: `linear-gradient(90deg, ${GOLD_PALETTE.PRIMARY_GOLD} 0%, ${GOLD_PALETTE.DARK_GOLD} 100%)`,
      },
    },
  },

  // サーキュラープログレス
  MuiCircularProgress: {
    styleOverrides: {
      colorPrimary: {
        color: GOLD_PALETTE.PRIMARY_GOLD,
      },
    },
  },

  // バッジ
  MuiBadge: {
    styleOverrides: {
      badge: {
        fontWeight: 600,
      },
      colorPrimary: {
        background: `linear-gradient(135deg, ${GOLD_PALETTE.PRIMARY_GOLD} 0%, ${GOLD_PALETTE.DARK_GOLD} 100%)`,
      },
    },
  },

  // アバター
  MuiAvatar: {
    styleOverrides: {
      colorDefault: {
        backgroundColor: GOLD_PALETTE.LIGHT_GOLD,
        color: GOLD_PALETTE.DARK_GOLD,
      },
    },
  },

  // ツールチップ
  MuiTooltip: {
    styleOverrides: {
      tooltip: {
        backgroundColor: 'rgba(33, 33, 33, 0.95)',
        fontSize: '0.875rem',
        borderRadius: 8,
        padding: '8px 12px',
      },
      arrow: {
        color: 'rgba(33, 33, 33, 0.95)',
      },
    },
  },
};
