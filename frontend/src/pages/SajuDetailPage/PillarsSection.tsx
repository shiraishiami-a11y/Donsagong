// 四柱表示セクションコンポーネント
import { Box, Typography } from '@mui/material';
import type { SajuDetailPageData } from '../../types';
import { getElementColor } from '../../utils/sajuHelpers';

interface PillarsSectionProps {
  data: SajuDetailPageData;
}

export const PillarsSection: React.FC<PillarsSectionProps> = ({ data }) => {
  return (
    <Box
      sx={{
        backgroundColor: 'white',
        padding: { xs: '20px', sm: '30px 40px' },
        margin: { xs: '16px 0', sm: '20px 0' },
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
          mb: { xs: '16px', sm: '24px' },
        }}
      >
        命式（四柱）
      </Typography>

      {/* サブタイトル */}
      <Typography
        variant="body2"
        sx={{
          fontSize: '14px',
          color: '#666',
          mb: '16px',
        }}
      >
        右から年柱→月柱→日柱→時柱
      </Typography>

      {/* 四柱グリッド（レスポンシブ） */}
      <Box
        sx={{
          display: 'grid',
          gridTemplateColumns: {
            xs: 'repeat(2, 1fr)',  // モバイル: 2カラム（2x2グリッド）
            sm: 'repeat(4, 1fr)',  // タブレット以上: 4カラム（1行）
          },
          gap: { xs: '12px', sm: '20px', lg: '30px' },
          maxWidth: { xs: '100%', sm: '800px', lg: '1000px' },
          margin: '0 auto',
        }}
      >
        {[...data.pillars].reverse().map((pillar) => (
          <Box
            key={pillar.type}
            sx={{
              textAlign: 'center',
            }}
          >
            <Typography
              variant="caption"
              sx={{
                fontSize: { xs: '12px', md: '14px', lg: '16px' },
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
                gap: '6px',
                alignItems: 'center',
              }}
            >
              {/* 天干（レスポンシブサイズ） */}
              <Box
                sx={{
                  width: '100%',
                  aspectRatio: '1',
                  borderRadius: { xs: '12px', sm: '16px' },
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 700,
                  fontSize: { xs: '24px', md: '28px', lg: '32px' },
                  color: 'white',
                  textShadow: '1px 1px 2px rgba(0,0,0,0.3)',
                  background: getElementColor(pillar.stemElement),
                  boxShadow: '0 2px 6px rgba(0,0,0,0.1)',
                }}
              >
                {pillar.stem}
              </Box>

              {/* 地支（レスポンシブサイズ） */}
              <Box
                sx={{
                  width: '100%',
                  aspectRatio: '1',
                  borderRadius: { xs: '12px', sm: '16px' },
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 700,
                  fontSize: { xs: '24px', md: '28px', lg: '32px' },
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
  );
};
