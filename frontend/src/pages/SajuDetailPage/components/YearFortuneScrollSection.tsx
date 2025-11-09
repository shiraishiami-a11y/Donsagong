// YearFortuneScrollSection - 年運の水平スクロールセクション
import { useState, useEffect } from 'react';
import { Box, Typography, Chip } from '@mui/material';
import type { YearFortuneInfo, FortuneLevel } from '../../../types';
import { getElementColor, getStemElement, getBranchElement } from '../../../utils/sajuHelpers';
import { getYearFortuneList } from '../../../services/api/sajuFortuneService';
import { UNIFIED_CARD_STYLES } from '../../../constants/cardStyles';

interface YearFortuneScrollSectionProps {
  sajuId: string;
  daeunStartAge: number;
  selectedYear: number | null;
  onYearSelect: (year: number) => void;
}

// 吉凶カラーを取得（境界線用）
const getFortuneColorSolid = (fortuneLevel: FortuneLevel): string => {
  const colorMap: Record<FortuneLevel, string> = {
    '大吉': '#FFD700',
    '小吉': '#4CAF50',
    '吉': '#4CAF50',
    '吉凶': '#9E9E9E',
    '平': '#9E9E9E',
    '凶': '#FF9800',
    '大凶': '#F44336',
  };
  return colorMap[fortuneLevel];
};

export const YearFortuneScrollSection: React.FC<YearFortuneScrollSectionProps> = ({
  sajuId,
  daeunStartAge,
  selectedYear,
  onYearSelect,
}) => {
  const [years, setYears] = useState<YearFortuneInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchYearFortune = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await getYearFortuneList(sajuId, daeunStartAge);
        setYears(data.years);
      } catch (err) {
        console.error('年運取得エラー:', err);
        setError(err instanceof Error ? err.message : '年運の取得に失敗しました');
      } finally {
        setLoading(false);
      }
    };

    fetchYearFortune();
  }, [sajuId, daeunStartAge]);

  if (loading) {
    return (
      <Box sx={{ px: 2, py: 3, backgroundColor: '#fff', borderTop: '1px solid #e0e0e0' }}>
        <Typography sx={{ textAlign: 'center', color: '#666' }}>
          年運を読み込み中...
        </Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ px: 2, py: 3, backgroundColor: '#fff', borderTop: '1px solid #e0e0e0' }}>
        <Typography sx={{ textAlign: 'center', color: '#F44336' }}>
          {error}
        </Typography>
      </Box>
    );
  }

  return (
    <Box
      data-testid="year-scroll-section"
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
        年運（{daeunStartAge}-{daeunStartAge + 9}歳）
      </Typography>

      <Box
        data-testid="year-scroll-container"
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
            justifyContent: { xs: 'flex-start', sm: 'flex-start' },
            minWidth: { xs: 'min-content', sm: 'auto' },
          }}
        >
          {[...years].reverse().map((yearFortune) => {
          const isSelected = selectedYear === yearFortune.year;
          const isCurrent = yearFortune.isCurrent;

          return (
            <Box
              key={yearFortune.id}
              data-testid={`year-card-${yearFortune.year}`}
              onClick={() => onYearSelect(yearFortune.year)}
              sx={{
                minWidth: UNIFIED_CARD_STYLES.card.minWidth,
                padding: { xs: '12px', sm: '20px' },
                borderRadius: '12px',
                border: isSelected
                  ? '2px solid #D4AF37'
                  : '1px solid #e0e0e0',
                borderLeft: `4px solid ${getFortuneColorSolid(yearFortune.fortuneLevel)}`,
                background: isCurrent
                  ? 'linear-gradient(135deg, #FFF9E6 0%, #FFFFFF 100%)'
                  : '#fff',
                boxShadow: isSelected
                  ? '0 4px 12px rgba(212, 175, 55, 0.3)'
                  : '0 2px 4px rgba(0,0,0,0.1)',
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                '&:hover': {
                  boxShadow: '0 4px 12px rgba(212, 175, 55, 0.2)',
                  transform: 'translateY(-2px)',
                },
              }}
            >
              {/* 年号 */}
              <Typography
                variant="caption"
                sx={{
                  display: 'block',
                  fontSize: '0.7rem',
                  color: '#666',
                  mb: 0.5,
                  textAlign: 'center',
                }}
              >
                {yearFortune.year}年
              </Typography>

              {/* 天干地支（縦並び） */}
              <Box
                sx={{
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'center',
                  alignItems: 'center',
                  gap: 0.5,
                  mb: 1,
                }}
              >
                <Box
                  data-testid="year-stem"
                  sx={{
                    width: UNIFIED_CARD_STYLES.pillar.width,
                    height: UNIFIED_CARD_STYLES.pillar.height,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    background: getElementColor(getStemElement(yearFortune.yearStem)),
                    borderRadius: UNIFIED_CARD_STYLES.pillar.borderRadius,
                    fontSize: UNIFIED_CARD_STYLES.fontSize.pillarChar,
                    fontWeight: 600,
                    color: '#fff',
                    textShadow: '1px 1px 2px rgba(0,0,0,0.3)',
                    boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
                  }}
                >
                  {yearFortune.yearStem}
                </Box>
                <Box
                  data-testid="year-branch"
                  sx={{
                    width: UNIFIED_CARD_STYLES.pillar.width,
                    height: UNIFIED_CARD_STYLES.pillar.height,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    background: getElementColor(getBranchElement(yearFortune.yearBranch)),
                    borderRadius: UNIFIED_CARD_STYLES.pillar.borderRadius,
                    fontSize: UNIFIED_CARD_STYLES.fontSize.pillarChar,
                    fontWeight: 600,
                    color: '#fff',
                    textShadow: '1px 1px 2px rgba(0,0,0,0.3)',
                    boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
                  }}
                >
                  {yearFortune.yearBranch}
                </Box>
              </Box>

              {/* 吉凶レベル表示 */}
              <Typography
                data-testid="fortune-icon"
                variant="caption"
                sx={{
                  display: 'block',
                  fontSize: '0.8rem',
                  fontWeight: 600,
                  color: getFortuneColorSolid(yearFortune.fortuneLevel),
                  textAlign: 'center',
                  mb: 0.5,
                }}
              >
                {yearFortune.fortuneLevel}
              </Typography>

              {/* 十神 */}
              <Typography
                variant="caption"
                sx={{
                  display: 'block',
                  fontSize: '0.65rem',
                  color: '#999',
                  textAlign: 'center',
                  mb: 0.5,
                }}
              >
                {yearFortune.sipsin || ''}
              </Typography>

              {/* 現在バッジ */}
              {isCurrent && (
                <Chip
                  label="現在"
                  size="small"
                  sx={{
                    height: '18px',
                    fontSize: '0.65rem',
                    backgroundColor: '#D4AF37',
                    color: 'white',
                    fontWeight: 600,
                    width: '100%',
                  }}
                />
              )}
            </Box>
          );
        })}
        </Box>
      </Box>
    </Box>
  );
};
