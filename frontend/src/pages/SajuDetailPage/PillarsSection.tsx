// 四柱表示セクションコンポーネント
import { Box, Typography } from '@mui/material';
import type { SajuDetailPageData } from '../../types';
import { getElementColor } from '../../utils/sajuHelpers';
import { MAIN_PILLAR_STYLES } from '../../constants/cardStyles';

interface PillarsSectionProps {
  data: SajuDetailPageData;
}

export const PillarsSection: React.FC<PillarsSectionProps> = ({ data }) => {
  return (
    <Box
      data-testid="pillars-section"
      sx={{
        backgroundColor: 'white',
        padding: { xs: '16px 8px', sm: '24px 16px' },
        margin: { xs: '12px 0', sm: '16px 0' },
        borderRadius: { xs: 0, sm: '12px' },
      }}
    >
      {/* タイトル */}
      <Typography
        variant="h6"
        sx={{
          fontSize: { xs: '18px', sm: '24px' },
          fontWeight: 700,
          color: '#1a1a2e',
          mb: { xs: '12px', sm: '20px' },
        }}
      >
        命式（四柱）
      </Typography>

      {/* 四柱グリッド（横スクロール対応） */}
      <Box
        sx={{
          overflowX: 'auto',
          WebkitOverflowScrolling: 'touch',
          pb: '8px',
        }}
      >
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'row',
            gap: MAIN_PILLAR_STYLES.spacing.gap,
            justifyContent: 'center',
            minWidth: 'min-content',
          }}
        >
          {data.pillars.slice().reverse().map((pillar) => (
            <Box
              key={pillar.type}
              sx={{
                textAlign: 'center',
                flexShrink: 0,
              }}
            >
            <Typography
              variant="caption"
              sx={{
                fontSize: MAIN_PILLAR_STYLES.fontSize.label,
                color: '#666',
                mb: { xs: '8px', sm: '12px' },
                display: 'block',
              }}
            >
              {pillar.type}
            </Typography>

            <Box
              sx={{
                display: 'flex',
                flexDirection: 'column',
                gap: MAIN_PILLAR_STYLES.spacing.pillarGap,
                alignItems: 'center',
              }}
            >
              {/* 天干（命式専用サイズ・1.5倍） */}
              <Box
                sx={{
                  width: MAIN_PILLAR_STYLES.pillar.width,
                  height: MAIN_PILLAR_STYLES.pillar.height,
                  borderRadius: MAIN_PILLAR_STYLES.pillar.borderRadius,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 700,
                  fontSize: MAIN_PILLAR_STYLES.fontSize.pillarChar,
                  color: 'white',
                  textShadow: '1px 1px 2px rgba(0,0,0,0.3)',
                  background: getElementColor(pillar.stemElement),
                  boxShadow: '0 2px 6px rgba(0,0,0,0.1)',
                }}
              >
                {pillar.stem}
              </Box>

              {/* 地支（命式専用サイズ・1.5倍） */}
              <Box
                sx={{
                  width: MAIN_PILLAR_STYLES.pillar.width,
                  height: MAIN_PILLAR_STYLES.pillar.height,
                  borderRadius: MAIN_PILLAR_STYLES.pillar.borderRadius,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 700,
                  fontSize: MAIN_PILLAR_STYLES.fontSize.pillarChar,
                  color: 'white',
                  textShadow: '1px 1px 2px rgba(0,0,0,0.3)',
                  background: getElementColor(pillar.branchElement),
                  boxShadow: '0 2px 6px rgba(0,0,0,0.1)',
                }}
              >
                {pillar.branch}
              </Box>
            </Box>
          </Box>
        ))}
        </Box>
      </Box>
    </Box>
  );
};
