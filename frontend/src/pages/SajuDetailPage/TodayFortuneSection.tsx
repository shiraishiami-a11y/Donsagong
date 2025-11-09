// TodayFortuneSection.tsx - 今日の運セクション（年運・月運・日運）
import { Box, Typography } from '@mui/material';
import { UNIFIED_CARD_STYLES } from '../../constants/cardStyles';

// 五行カラー
const ELEMENT_COLORS: Record<string, string> = {
  wood: 'linear-gradient(135deg, #4CAF50, #66bb6a)',
  fire: 'linear-gradient(135deg, #F44336, #ef5350)',
  earth: 'linear-gradient(135deg, #FFB300, #ffa726)',
  metal: 'linear-gradient(135deg, #9E9E9E, #BDBDBD)',
  water: 'linear-gradient(135deg, #424242, #616161)',
};

// 吉凶カラー
const FORTUNE_COLORS: Record<number, { bg: string; color: string }> = {
  5: { bg: '#FFD700', color: '#1a1a2e' }, // 大吉
  4: { bg: '#4CAF50', color: 'white' },   // 吉
  3: { bg: '#9E9E9E', color: 'white' },   // 平
  2: { bg: '#FF9800', color: 'white' },   // 凶
  1: { bg: '#F44336', color: 'white' },   // 大凶
};

const FORTUNE_LABELS: Record<number, string> = {
  5: '大吉',
  4: '吉',
  3: '平',
  2: '凶',
  1: '大凶',
};

interface FortuneCardProps {
  label: string;
  tengan: { char: string; element: string };
  jishi: { char: string; element: string };
  fortuneLevel: number;
}

const FortuneCard: React.FC<FortuneCardProps> = ({ label, tengan, jishi, fortuneLevel }) => {
  return (
    <Box
      sx={{
        minWidth: UNIFIED_CARD_STYLES.card.minWidth,
        background: '#fafafa',
        borderRadius: UNIFIED_CARD_STYLES.card.borderRadius,
        padding: UNIFIED_CARD_STYLES.card.padding,
        boxShadow: '0 2px 6px rgba(0,0,0,0.05)',
        textAlign: 'center',
        flexShrink: 0,
      }}
    >
      {/* ラベル */}
      <Typography
        variant="body2"
        sx={{
          fontSize: '12px',
          fontWeight: 600,
          color: '#666',
          mb: '8px',
        }}
      >
        {label}
      </Typography>

      {/* 天干・地支（縦並び） */}
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: '6px', alignItems: 'center', mb: '8px' }}>
        {/* 天干 */}
        <Box
          sx={{
            width: UNIFIED_CARD_STYLES.pillar.width,
            height: UNIFIED_CARD_STYLES.pillar.height,
            borderRadius: UNIFIED_CARD_STYLES.pillar.borderRadius,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontWeight: 700,
            fontSize: UNIFIED_CARD_STYLES.fontSize.pillarChar,
            color: 'white',
            textShadow: '1px 1px 2px rgba(0,0,0,0.3)',
            background: ELEMENT_COLORS[tengan.element] || '#9E9E9E',
          }}
        >
          {tengan.char}
        </Box>

        {/* 地支 */}
        <Box
          sx={{
            width: UNIFIED_CARD_STYLES.pillar.width,
            height: UNIFIED_CARD_STYLES.pillar.height,
            borderRadius: UNIFIED_CARD_STYLES.pillar.borderRadius,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontWeight: 700,
            fontSize: UNIFIED_CARD_STYLES.fontSize.pillarChar,
            color: 'white',
            textShadow: '1px 1px 2px rgba(0,0,0,0.3)',
            background: ELEMENT_COLORS[jishi.element] || '#9E9E9E',
          }}
        >
          {jishi.char}
        </Box>
      </Box>

      {/* 吉凶バッジ */}
      <Box
        sx={{
          padding: '4px 8px',
          borderRadius: '12px',
          fontSize: '11px',
          fontWeight: 600,
          display: 'inline-block',
          background: FORTUNE_COLORS[fortuneLevel]?.bg || '#9E9E9E',
          color: FORTUNE_COLORS[fortuneLevel]?.color || 'white',
        }}
      >
        {FORTUNE_LABELS[fortuneLevel] || '平'}
      </Box>
    </Box>
  );
};

interface TodayFortuneSectionProps {
  currentYear: number;
  currentMonth: number;
  currentDay: number;
  yearFortune: {
    tengan: { char: string; element: string };
    jishi: { char: string; element: string };
    fortuneLevel: number;
  };
  monthFortune: {
    tengan: { char: string; element: string };
    jishi: { char: string; element: string };
    fortuneLevel: number;
  };
  dayFortune: {
    tengan: { char: string; element: string };
    jishi: { char: string; element: string };
    fortuneLevel: number;
  };
}

export const TodayFortuneSection: React.FC<TodayFortuneSectionProps> = ({
  currentYear,
  currentMonth,
  currentDay,
  yearFortune,
  monthFortune,
  dayFortune,
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
        今日の運
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
        今日の年運・月運・日運の吉凶
      </Typography>

      {/* 3つのカード（レスポンシブ横スクロール対応） */}
      <Box
        sx={{
          display: 'flex',
          gap: UNIFIED_CARD_STYLES.spacing.gap,
          justifyContent: 'center',
          padding: '8px 0',
          overflowX: { xs: 'auto', sm: 'visible' },
          WebkitOverflowScrolling: 'touch',
        }}
      >
        {/* 年運 */}
        <FortuneCard
          label={`${currentYear}年`}
          tengan={yearFortune.tengan}
          jishi={yearFortune.jishi}
          fortuneLevel={yearFortune.fortuneLevel}
        />

        {/* 月運 */}
        <FortuneCard
          label={`${currentMonth}月`}
          tengan={monthFortune.tengan}
          jishi={monthFortune.jishi}
          fortuneLevel={monthFortune.fortuneLevel}
        />

        {/* 日運 */}
        <FortuneCard
          label={`${currentDay}日`}
          tengan={dayFortune.tengan}
          jishi={dayFortune.jishi}
          fortuneLevel={dayFortune.fortuneLevel}
        />
      </Box>
    </Box>
  );
};

export default TodayFortuneSection;
