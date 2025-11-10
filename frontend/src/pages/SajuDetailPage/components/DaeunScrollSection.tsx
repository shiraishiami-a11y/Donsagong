// DaeunScrollSection - 大運の水平スクロールセクション
import { Box, Typography } from '@mui/material';
import type { DaeunInfo, FortuneLevel } from '../../../types';
import { getElementColor, getStemElement, getBranchElement } from '../../../utils/sajuHelpers';
import { UNIFIED_CARD_STYLES } from '../../../constants/cardStyles';

interface DaeunScrollSectionProps {
  daeunList: DaeunInfo[];
  selectedDaeunStartAge: number | null;
  onDaeunSelect: (startAge: number) => void;
  daeunNumber: number; // 大運数
}

// 吉凶カラーを取得（境界線用） - 7段階システム対応
const getFortuneColorSolid = (fortuneLevel: FortuneLevel): string => {
  const colorMap: Record<FortuneLevel, string> = {
    '大吉': '#FFD700',
    '吉': '#4CAF50',
    '中吉': '#66bb6a',
    '小吉': '#81c784',
    '平': '#9E9E9E',
    '凶': '#FF9800',
    '大凶': '#F44336',
  };
  return colorMap[fortuneLevel];
};

// 大運の開始年齢のみを表示
const getAgeRangeLabel = (startAge: number, _endAge: number): string => {
  return `${startAge}`;
};

export const DaeunScrollSection: React.FC<DaeunScrollSectionProps> = ({
  daeunList,
  selectedDaeunStartAge,
  onDaeunSelect,
}) => {
  // 最初の大運の年齢範囲を取得してタイトルに表示
  const firstDaeun = daeunList[0];
  const titleLabel = firstDaeun
    ? getAgeRangeLabel(firstDaeun.startAge, firstDaeun.endAge)
    : '大運';

  return (
    <Box
      data-testid="daeun-scroll-section"
      sx={{
        backgroundColor: 'white',
        padding: { xs: '20px', sm: '30px 40px' },
        margin: { xs: '16px 0', sm: '20px 0' },
        borderRadius: { xs: 0, sm: '12px' },
      }}
    >
      <Typography
        variant="h6"
        sx={{
          fontSize: { xs: '18px', sm: '24px' },
          fontWeight: 700,
          color: '#1a1a2e',
          mb: { xs: '16px', sm: '24px' },
        }}
      >
        大運（{titleLabel}）
      </Typography>

      {/* スクロールコンテナ */}
      <Box
        data-testid="daeun-scroll-container"
        sx={{
          maxWidth: '100%',
          overflowX: 'auto',
          WebkitOverflowScrolling: 'touch',
          padding: { xs: '12px 0', sm: '20px 0' },
          scrollbarWidth: 'thin',
          scrollbarColor: '#D4AF37 #f5f5f5',
          '&::-webkit-scrollbar': {
            height: '6px',
          },
          '&::-webkit-scrollbar-track': {
            background: '#f5f5f5',
            borderRadius: '10px',
          },
          '&::-webkit-scrollbar-thumb': {
            background: '#D4AF37',
            borderRadius: '10px',
          },
        }}
      >
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'row',
            gap: UNIFIED_CARD_STYLES.spacing.gap,
            minWidth: 'min-content',
          }}
        >
        {[...daeunList].reverse().map((daeun) => {
          const isSelected = selectedDaeunStartAge === daeun.startAge;
          const isCurrent = daeun.isCurrent;

          return (
            <Box
              key={daeun.id}
              data-testid={`daeun-card-${daeun.startAge}`}
              onClick={() => onDaeunSelect(daeun.startAge)}
              sx={{
                minWidth: UNIFIED_CARD_STYLES.card.minWidth,
                boxSizing: 'border-box',
                padding: { xs: '12px', sm: '20px' },
                borderRadius: '12px',
                border: isCurrent
                  ? '3px solid #4CAF50'
                  : isSelected
                  ? '2px solid #D4AF37'
                  : '2px solid #e0e0e0',
                background: isCurrent ? '#f0f9f0' : '#fafafa',
                boxShadow: isSelected
                  ? '0 6px 16px rgba(212, 175, 55, 0.2)'
                  : '0 2px 4px rgba(0,0,0,0.1)',
                cursor: 'pointer',
                transition: 'all 0.2s',
                '&:hover': {
                  borderColor: '#D4AF37',
                  transform: 'translateY(-4px)',
                  boxShadow: '0 6px 16px rgba(212, 175, 55, 0.2)',
                },
                textAlign: 'center',
              }}
            >
              {/* 年齢範囲 */}
              <Typography
                variant="caption"
                sx={{
                  display: 'block',
                  fontSize: '14px',
                  color: '#666',
                  fontWeight: 600,
                  mb: '8px',
                }}
              >
                {getAgeRangeLabel(daeun.startAge, daeun.endAge)}
              </Typography>

              {/* 天干地支（縦並び） */}
              <Box
                sx={{
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'center',
                  alignItems: 'center',
                  gap: '6px',
                  mb: '8px',
                }}
              >
                <Box
                  sx={{
                    width: UNIFIED_CARD_STYLES.pillar.width,
                    height: UNIFIED_CARD_STYLES.pillar.height,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    background: getElementColor(getStemElement(daeun.daeunStem)),
                    borderRadius: UNIFIED_CARD_STYLES.pillar.borderRadius,
                    fontSize: UNIFIED_CARD_STYLES.fontSize.pillarChar,
                    fontWeight: 600,
                    color: '#fff',
                    textShadow: '1px 1px 2px rgba(0,0,0,0.3)',
                  }}
                >
                  {daeun.daeunStem}
                </Box>
                <Box
                  sx={{
                    width: UNIFIED_CARD_STYLES.pillar.width,
                    height: UNIFIED_CARD_STYLES.pillar.height,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    background: getElementColor(getBranchElement(daeun.daeunBranch)),
                    borderRadius: UNIFIED_CARD_STYLES.pillar.borderRadius,
                    fontSize: UNIFIED_CARD_STYLES.fontSize.pillarChar,
                    fontWeight: 600,
                    color: '#fff',
                    textShadow: '1px 1px 2px rgba(0,0,0,0.3)',
                  }}
                >
                  {daeun.daeunBranch}
                </Box>
              </Box>

              {/* 吉凶レベル表示 */}
              <Box
                sx={{
                  padding: '6px 12px',
                  borderRadius: '12px',
                  fontSize: '12px',
                  fontWeight: 600,
                  background: getFortuneColorSolid(daeun.fortuneLevel),
                  color: 'white',
                  mb: '4px',
                }}
              >
                {daeun.fortuneLevel}
              </Box>

              {/* 十神 */}
              {daeun.sipsin && (
                <Typography
                  variant="caption"
                  sx={{
                    display: 'block',
                    fontSize: '10px',
                    color: '#999',
                  }}
                >
                  {daeun.sipsin}
                </Typography>
              )}
            </Box>
          );
        })}
        </Box>
      </Box>
    </Box>
  );
};
