// SajuCard - 命式カードコンポーネント（簡易版・五行吉凶表示なし）
import { Box, Typography, IconButton } from '@mui/material';
import type { SajuSummary } from '../../../types';
import { formatBirthDateTime } from '../../../utils/sajuHelpers';

interface SajuCardProps {
  data: SajuSummary;
  onEdit: (id: string) => void;
  onDelete: (id: string) => void;
  onClick: (id: string) => void;
}

export const SajuCard: React.FC<SajuCardProps> = ({ data, onEdit, onDelete, onClick }) => {
  const handleCardClick = () => {
    onClick(data.id);
  };

  const handleEdit = (e: React.MouseEvent) => {
    e.stopPropagation();
    onEdit(data.id);
  };

  const handleDelete = (e: React.MouseEvent) => {
    e.stopPropagation();
    onDelete(data.id);
  };

  // 性別アイコン
  const genderIcon = data.gender === 'male' ? '👨' : '👩';
  const genderLabel = data.gender === 'male' ? '男性' : '女性';

  return (
    <Box
      data-testid={`saju-card-${data.id}`}
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
        <Box sx={{ display: 'flex', gap: '8px' }}>
          <IconButton
            data-testid="edit-button"
            onClick={handleEdit}
            sx={{
              background: '#f5f5f5',
              minWidth: '44px',
              minHeight: '44px',
              width: { xs: '44px', md: '48px' },
              height: { xs: '44px', md: '48px' },
              borderRadius: { xs: '10px', md: '12px' },
              transition: 'all 0.2s',
              '&:hover': {
                background: '#e3f2fd',
                color: '#1976d2',
              },
            }}
            aria-label="編集"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" style={{ fontSize: '14px' }}>
              <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
            </svg>
          </IconButton>
          <IconButton
            data-testid="delete-button"
            onClick={handleDelete}
            sx={{
              background: '#f5f5f5',
              minWidth: '44px',
              minHeight: '44px',
              width: { xs: '44px', md: '48px' },
              height: { xs: '44px', md: '48px' },
              borderRadius: { xs: '10px', md: '12px' },
              transition: 'all 0.2s',
              '&:hover': {
                background: '#ffebee',
                color: '#f44336',
              },
            }}
            aria-label="削除"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" style={{ fontSize: '14px' }}>
              <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/>
            </svg>
          </IconButton>
        </Box>
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
    </Box>
  );
};
