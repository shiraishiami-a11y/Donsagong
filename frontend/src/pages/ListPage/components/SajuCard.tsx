// SajuCard - 命式カードコンポーネント（レスポンシブモックアップ完全一致版）
import { Box, Typography, IconButton } from '@mui/material';
import type { SajuSummary } from '../../../types';
import { formatBirthDateTime } from '../../../utils/sajuHelpers';

interface SajuCardProps {
  data: SajuSummary;
  onEdit: (id: string) => void;
  onDelete: (id: string) => void;
  onClick: (id: string) => void;
}

// 五行カラーマッピング
const elementColors: Record<string, string> = {
  wood: 'linear-gradient(135deg, #4CAF50, #66bb6a)',
  fire: 'linear-gradient(135deg, #F44336, #ef5350)',
  earth: 'linear-gradient(135deg, #FFB300, #ffa726)',
  metal: 'linear-gradient(135deg, #9E9E9E, #BDBDBD)',
  water: 'linear-gradient(135deg, #424242, #616161)',
};

// 天干・地支から五行を判定（簡易版）
const getElementFromStem = (stem: string): string => {
  const stemMap: Record<string, string> = {
    '甲': 'wood', '乙': 'wood',
    '丙': 'fire', '丁': 'fire',
    '戊': 'earth', '己': 'earth',
    '庚': 'metal', '辛': 'metal',
    '壬': 'water', '癸': 'water',
  };
  return stemMap[stem] || 'metal';
};

const getElementFromBranch = (branch: string): string => {
  const branchMap: Record<string, string> = {
    '寅': 'wood', '卯': 'wood',
    '巳': 'fire', '午': 'fire',
    '辰': 'earth', '戌': 'earth', '丑': 'earth', '未': 'earth',
    '申': 'metal', '酉': 'metal',
    '子': 'water', '亥': 'water',
  };
  return branchMap[branch] || 'earth';
};

// 吉凶レベルから表示を生成
const getFortuneBadge = (level: number): { text: string; color: string } => {
  if (level === 5) return { text: '大吉 5/5', color: '#FFD700' };
  if (level === 4) return { text: '吉 4/5', color: '#4CAF50' };
  if (level === 3) return { text: '平 3/5', color: '#9E9E9E' };
  if (level === 2) return { text: '凶 2/5', color: '#FF9800' };
  return { text: '大凶 1/5', color: '#F44336' };
};

export const SajuCard: React.FC<SajuCardProps> = ({ data, onDelete, onClick }) => {
  const handleCardClick = () => {
    onClick(data.id);
  };

  const handleDelete = (e: React.MouseEvent) => {
    e.stopPropagation();
    onDelete(data.id);
  };

  // 性別アイコン
  const genderIcon = data.gender === 'male' ? '👨' : '👩';
  const genderLabel = data.gender === 'male' ? '男性' : '女性';

  // 吉凶バッジ
  const fortuneLevel = typeof data.fortuneLevel === 'number' ? data.fortuneLevel : 3;
  const fortuneBadge = getFortuneBadge(fortuneLevel);

  // 四柱データ
  const pillars = [
    { stem: data.yearStem, branch: data.yearBranch },
    { stem: data.monthStem, branch: data.monthBranch },
    { stem: data.dayStem, branch: data.dayBranch },
    { stem: data.hourStem, branch: data.hourBranch },
  ];

  return (
    <Box
      data-testid="saju-card"
      onClick={handleCardClick}
      sx={{
        background: 'white',
        borderRadius: { xs: '16px', md: '20px' },
        padding: { xs: '20px', md: '24px' },
        boxShadow: '0 2px 8px rgba(0,0,0,0.06)',
        cursor: 'pointer',
        transition: 'all 0.2s',
        border: '2px solid transparent',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: '0 6px 20px rgba(0,0,0,0.12)',
          borderColor: '#D4AF37',
        },
      }}
    >
      {/* カードヘッダー */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
        <Box>
          <Typography
            data-testid="saju-name"
            sx={{
              fontSize: { xs: '20px', md: '24px' },
              fontWeight: 700,
              color: '#1a1a2e',
            }}
          >
            {data.name || '無題'}
          </Typography>
          <Typography
            sx={{
              fontSize: { xs: '12px', md: '14px' },
              color: '#666',
            }}
          >
            {genderIcon} {genderLabel}
          </Typography>
        </Box>
        <IconButton
          data-testid="delete-button"
          onClick={handleDelete}
          sx={{
            background: '#f5f5f5',
            width: { xs: 32, md: 36 },
            height: { xs: 32, md: 36 },
            transition: 'all 0.2s',
            '&:hover': {
              background: '#ffebee',
              color: '#f44336',
            },
          }}
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
            <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/>
          </svg>
        </IconButton>
      </Box>

      {/* 生年月日時 */}
      <Typography
        data-testid="birth-datetime"
        sx={{
          fontSize: { xs: '14px', md: '16px' },
          color: '#666',
          mb: 2,
        }}
      >
        {formatBirthDateTime(data.birthDatetime)}
      </Typography>

      {/* 四柱ミニ表示 (4×2グリッド) */}
      <Box
        sx={{
          display: 'grid',
          gridTemplateColumns: 'repeat(4, 1fr)',
          gap: { xs: '6px', md: '8px' },
          mb: { xs: 1.5, md: 2 },
        }}
      >
        {pillars.map((pillar, idx) => {
          const stemElement = getElementFromStem(pillar.stem);
          const branchElement = getElementFromBranch(pillar.branch);
          return (
            <Box key={idx} sx={{ textAlign: 'center' }}>
              {/* 天干 */}
              <Box
                data-testid={`${['year', 'month', 'day', 'hour'][idx]}-stem`}
                sx={{
                  width: '100%',
                  aspectRatio: '1',
                  borderRadius: { xs: '6px', md: '8px' },
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 700,
                  fontSize: { xs: '14px', md: '16px' },
                  color: 'white',
                  background: elementColors[stemElement],
                  mb: '2px',
                }}
              >
                {pillar.stem}
              </Box>
              {/* 地支 */}
              <Box
                sx={{
                  width: '100%',
                  aspectRatio: '1',
                  borderRadius: { xs: '6px', md: '8px' },
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 700,
                  fontSize: { xs: '14px', md: '16px' },
                  color: 'white',
                  background: elementColors[branchElement],
                }}
              >
                {pillar.branch}
              </Box>
            </Box>
          );
        })}
      </Box>

      {/* 吉凶バッジ */}
      <Box
        data-testid="fortune-icon"
        sx={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: 0.5,
          padding: { xs: '6px 12px', md: '8px 16px' },
          borderRadius: '12px',
          fontSize: { xs: '12px', md: '14px' },
          fontWeight: 600,
          color: 'white',
          background: fortuneBadge.color,
        }}
      >
        {fortuneBadge.text}
      </Box>
    </Box>
  );
};
