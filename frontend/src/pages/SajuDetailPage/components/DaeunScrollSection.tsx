// DaeunScrollSection - 大運の水平スクロールセクション
import { Box, Typography } from '@mui/material';
import type { DaeunInfo, FortuneLevel } from '../../../types';
import { getElementColor, getStemElement, getBranchElement } from '../../../utils/sajuHelpers';

interface DaeunScrollSectionProps {
  daeunList: DaeunInfo[];
  selectedDaeunStartAge: number | null;
  onDaeunSelect: (startAge: number) => void;
  daeunNumber: number; // 大運数
}

// 吉凶カラーを取得（境界線用）
const getFortuneColorSolid = (fortuneLevel: FortuneLevel): string => {
  const colorMap: Record<FortuneLevel, string> = {
    '大吉': '#FFD700',
    '吉': '#4CAF50',
    '平': '#9E9E9E',
    '凶': '#FF9800',
    '大凶': '#F44336',
  };
  return colorMap[fortuneLevel];
};

export const DaeunScrollSection: React.FC<DaeunScrollSectionProps> = ({
  daeunList,
  selectedDaeunStartAge,
  onDaeunSelect,
  daeunNumber,
}) => {
  return (
    <Box
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
        大運（大運数：{daeunNumber}）
      </Typography>

      <Box
        data-testid="daeun-scroll-container"
        sx={{
          display: 'flex',
          flexDirection: 'row-reverse',
          gap: { xs: '12px', sm: '20px' },
          overflowX: 'auto',
          padding: { xs: '12px 0', sm: '20px 0' },
          WebkitOverflowScrolling: 'touch',
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
        {daeunList.map((daeun) => {
          const isSelected = selectedDaeunStartAge === daeun.startAge;
          const isCurrent = daeun.isCurrent;

          return (
            <Box
              key={daeun.id}
              data-testid={`daeun-card-${daeun.startAge}`}
              onClick={() => onDaeunSelect(daeun.startAge)}
              sx={{
                minWidth: { xs: '140px', md: '160px' },
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
                  fontSize: '12px',
                  color: '#666',
                  fontWeight: 600,
                  mb: '8px',
                }}
              >
                {daeun.startAge}-{daeun.endAge}歳
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
                    width: '60px',
                    height: '60px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    background: getElementColor(getStemElement(daeun.daeunStem)),
                    borderRadius: 1,
                    fontSize: { xs: '18px', md: '20px', lg: '22px' },
                    fontWeight: 600,
                    color: '#fff',
                    textShadow: '1px 1px 2px rgba(0,0,0,0.3)',
                  }}
                >
                  {daeun.daeunStem}
                </Box>
                <Box
                  sx={{
                    width: '60px',
                    height: '60px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    background: getElementColor(getBranchElement(daeun.daeunBranch)),
                    borderRadius: 1,
                    fontSize: { xs: '18px', md: '20px', lg: '22px' },
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
  );
};
