// DayFortuneScrollSection - 日運の水平スクロールセクション
import { useState, useEffect } from 'react';
import { Box, Typography, Chip } from '@mui/material';
import type { DayFortuneInfo, FortuneLevel } from '../../../types';
import { getElementColor, getStemElement, getBranchElement } from '../../../utils/sajuHelpers';
import { getDayFortuneList } from '../../../services/api/sajuFortuneService';
import { UNIFIED_CARD_STYLES } from '../../../constants/cardStyles';

interface DayFortuneScrollSectionProps {
  sajuId: string;
  year: number;
  month: number;
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

export const DayFortuneScrollSection: React.FC<DayFortuneScrollSectionProps> = ({
  sajuId,
  year,
  month,
}) => {
  const [days, setDays] = useState<DayFortuneInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDayFortune = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await getDayFortuneList(sajuId, year, month);
        setDays(data.days);
      } catch (err) {
        console.error('日運取得エラー:', err);
        setError(err instanceof Error ? err.message : '日運の取得に失敗しました');
      } finally {
        setLoading(false);
      }
    };

    fetchDayFortune();
  }, [sajuId, year, month]);

  if (loading) {
    return (
      <Box sx={{ px: 2, py: 3, backgroundColor: '#fff', borderTop: '1px solid #e0e0e0' }}>
        <Typography sx={{ textAlign: 'center', color: '#666' }}>
          日運を読み込み中...
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
    <Box sx={{
      backgroundColor: 'white',
      padding: { xs: '20px', sm: '30px 40px' },
      margin: { xs: '16px 0', sm: '20px 0' },
      borderRadius: { xs: 0, sm: '12px' },
    }}>
      <Typography
        variant="h6"
        sx={{
          fontSize: { xs: '18px', sm: '24px' },
          fontWeight: 700,
          color: '#1a1a2e',
          mb: { xs: '16px', sm: '24px' },
        }}
      >
        日運（{year}年{month}月）
      </Typography>

      <Box
        data-testid="day-scroll-container"
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
          {[...days].reverse().map((dayFortune) => {
          const isToday = dayFortune.isToday;

          return (
            <Box
              key={dayFortune.id}
              data-testid="day-card"
              sx={{
                minWidth: UNIFIED_CARD_STYLES.card.minWidth,
                flexShrink: 0,
                p: 1.5,
                borderRadius: 2,
                border: '1px solid #e0e0e0',
                borderLeft: `4px solid ${getFortuneColorSolid(dayFortune.fortuneLevel)}`,
                background: isToday
                  ? 'linear-gradient(135deg, #FFF9E6 0%, #FFFFFF 100%)'
                  : '#fff',
                boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                transition: 'all 0.3s ease',
                '&:hover': {
                  boxShadow: '0 4px 12px rgba(212, 175, 55, 0.2)',
                  transform: 'translateY(-2px)',
                },
              }}
            >
              {/* 日 */}
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
                {dayFortune.day}日
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
                  data-testid="day-stem"
                  sx={{
                    width: UNIFIED_CARD_STYLES.pillar.width,
                    height: UNIFIED_CARD_STYLES.pillar.height,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    background: getElementColor(getStemElement(dayFortune.dayStem)),
                    borderRadius: UNIFIED_CARD_STYLES.pillar.borderRadius,
                    fontSize: UNIFIED_CARD_STYLES.fontSize.pillarChar,
                    fontWeight: 600,
                    color: '#fff',
                    textShadow: '1px 1px 2px rgba(0,0,0,0.3)',
                    boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
                  }}
                >
                  {dayFortune.dayStem}
                </Box>
                <Box
                  data-testid="day-branch"
                  sx={{
                    width: UNIFIED_CARD_STYLES.pillar.width,
                    height: UNIFIED_CARD_STYLES.pillar.height,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    background: getElementColor(getBranchElement(dayFortune.dayBranch)),
                    borderRadius: UNIFIED_CARD_STYLES.pillar.borderRadius,
                    fontSize: UNIFIED_CARD_STYLES.fontSize.pillarChar,
                    fontWeight: 600,
                    color: '#fff',
                    textShadow: '1px 1px 2px rgba(0,0,0,0.3)',
                    boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
                  }}
                >
                  {dayFortune.dayBranch}
                </Box>
              </Box>

              {/* 吉凶レベル表示 */}
              <Typography
                data-testid="fortune-icon"
                variant="caption"
                sx={{
                  display: 'block',
                  fontSize: '0.7rem',
                  fontWeight: 600,
                  color: getFortuneColorSolid(dayFortune.fortuneLevel),
                  textAlign: 'center',
                  mb: 0.5,
                }}
              >
                {dayFortune.fortuneLevel}
              </Typography>

              {/* 十神 */}
              <Typography
                variant="caption"
                sx={{
                  display: 'block',
                  fontSize: '0.6rem',
                  color: '#999',
                  textAlign: 'center',
                  mb: 0.5,
                }}
              >
                {dayFortune.sipsin}
              </Typography>

              {/* 今日バッジ */}
              {isToday && (
                <Chip
                  label="今日"
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
