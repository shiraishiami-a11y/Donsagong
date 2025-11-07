// MonthFortuneScrollSection - 月運の水平スクロールセクション
import { useState, useEffect } from 'react';
import { Box, Typography, Chip } from '@mui/material';
import type { MonthFortuneInfo, FortuneLevel } from '../../../types';
import { getElementColor, getStemElement, getBranchElement } from '../../../utils/sajuHelpers';
import { getMonthFortuneList } from '../../../services/api/sajuFortuneService';

interface MonthFortuneScrollSectionProps {
  sajuId: string;
  year: number;
  selectedMonth: number | null;
  onMonthSelect: (month: number) => void;
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

export const MonthFortuneScrollSection: React.FC<MonthFortuneScrollSectionProps> = ({
  sajuId,
  year,
  selectedMonth,
  onMonthSelect,
}) => {
  const [months, setMonths] = useState<MonthFortuneInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchMonthFortune = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await getMonthFortuneList(sajuId, year);
        setMonths(data.months);
      } catch (err) {
        console.error('月運取得エラー:', err);
        setError(err instanceof Error ? err.message : '月運の取得に失敗しました');
      } finally {
        setLoading(false);
      }
    };

    fetchMonthFortune();
  }, [sajuId, year]);

  if (loading) {
    return (
      <Box sx={{ px: 2, py: 3, backgroundColor: '#fff', borderTop: '1px solid #e0e0e0' }}>
        <Typography sx={{ textAlign: 'center', color: '#666' }}>
          月運を読み込み中...
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
    <Box sx={{ px: 2, py: 3, backgroundColor: '#fff', borderTop: '1px solid #e0e0e0' }}>
      <Typography
        variant="h6"
        sx={{
          fontSize: '1rem',
          fontWeight: 600,
          color: '#1a1a2e',
          mb: 2,
        }}
      >
        月運（{year}年）
      </Typography>

      <Box
        data-testid="month-scroll-container"
        sx={{
          display: 'flex',
          flexDirection: 'row-reverse',
          gap: 1.5,
          overflowX: 'auto',
          WebkitOverflowScrolling: 'touch',
          pb: 1.5,
          '&::-webkit-scrollbar': {
            height: '6px',
          },
          '&::-webkit-scrollbar-track': {
            background: '#f1f1f1',
            borderRadius: '10px',
          },
          '&::-webkit-scrollbar-thumb': {
            background: '#D4AF37',
            borderRadius: '10px',
          },
        }}
      >
        {months.map((monthFortune) => {
          const isSelected = selectedMonth === monthFortune.month;
          const isCurrent = monthFortune.isCurrent;

          return (
            <Box
              key={monthFortune.id}
              data-testid="month-card"
              onClick={() => onMonthSelect(monthFortune.month)}
              sx={{
                minWidth: { xs: '85px', sm: '95px' },
                p: 1.5,
                borderRadius: 2,
                border: isSelected
                  ? '2px solid #D4AF37'
                  : '1px solid #e0e0e0',
                borderLeft: `4px solid ${getFortuneColorSolid(monthFortune.fortuneLevel)}`,
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
              {/* 月 */}
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
                {monthFortune.month}月
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
                  data-testid="month-stem"
                  sx={{
                    width: '40px',
                    height: '40px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    background: getElementColor(getStemElement(monthFortune.monthStem)),
                    borderRadius: 1,
                    fontSize: '1.2rem',
                    fontWeight: 600,
                    color: '#fff',
                    textShadow: '1px 1px 2px rgba(0,0,0,0.3)',
                    boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
                  }}
                >
                  {monthFortune.monthStem}
                </Box>
                <Box
                  data-testid="month-branch"
                  sx={{
                    width: '40px',
                    height: '40px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    background: getElementColor(getBranchElement(monthFortune.monthBranch)),
                    borderRadius: 1,
                    fontSize: '1.2rem',
                    fontWeight: 600,
                    color: '#fff',
                    textShadow: '1px 1px 2px rgba(0,0,0,0.3)',
                    boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
                  }}
                >
                  {monthFortune.monthBranch}
                </Box>
              </Box>

              {/* 吉凶レベル表示 */}
              <Typography
                data-testid="fortune-icon"
                variant="caption"
                sx={{
                  display: 'block',
                  fontSize: '0.75rem',
                  fontWeight: 600,
                  color: getFortuneColorSolid(monthFortune.fortuneLevel),
                  textAlign: 'center',
                  mb: 0.5,
                }}
              >
                {monthFortune.fortuneLevel}
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
                {monthFortune.sipsin}
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
  );
};
