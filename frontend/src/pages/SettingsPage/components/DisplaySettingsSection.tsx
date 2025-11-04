import { Box, Typography } from '@mui/material';
import PaletteIcon from '@mui/icons-material/Palette';

export const DisplaySettingsSection: React.FC = () => {
  return (
    <Box
      sx={{
        background: 'white',
        borderRadius: 3,
        boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)',
        mb: 2.5,
        overflow: 'hidden'
      }}
    >
      {/* セクションヘッダー */}
      <Box
        sx={{
          p: 2,
          background: theme => theme.palette.gold.LIGHT_GOLD,
          borderBottom: '1px solid',
          borderColor: 'divider'
        }}
      >
        <Typography
          variant="h6"
          sx={{
            fontSize: '16px',
            fontWeight: 500,
            color: theme => theme.palette.gold.DARK_GOLD,
            display: 'flex',
            alignItems: 'center',
            gap: 1
          }}
        >
          <PaletteIcon />
          表示設定
        </Typography>
      </Box>

      {/* セクションコンテンツ */}
      <Box sx={{ p: 2 }}>
        {/* テーマ */}
        <Box sx={{ pb: 2, borderBottom: '1px solid', borderColor: 'divider' }}>
          <Typography variant="body2" fontWeight={500} mb={0.5}>
            テーマ
          </Typography>
          <Box
            sx={{
              display: 'inline-block',
              px: 1.5,
              py: 1,
              background: theme => theme.palette.grey[100],
              borderRadius: 1,
              opacity: 0.5
            }}
          >
            <Typography variant="body2" color="text.secondary">
              ゴールド（固定）
            </Typography>
          </Box>
        </Box>

        {/* 言語 */}
        <Box sx={{ pt: 2 }}>
          <Typography variant="body2" fontWeight={500} mb={0.5}>
            言語
          </Typography>
          <Box
            sx={{
              display: 'inline-block',
              px: 1.5,
              py: 1,
              background: theme => theme.palette.grey[100],
              borderRadius: 1,
              opacity: 0.5
            }}
          >
            <Typography variant="body2" color="text.secondary">
              日本語（固定）
            </Typography>
          </Box>
        </Box>
      </Box>
    </Box>
  );
};
