import { Box, Typography, Link } from '@mui/material';
import InfoIcon from '@mui/icons-material/Info';

export const AppInfoSection: React.FC = () => {
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
          <InfoIcon />
          アプリ情報
        </Typography>
      </Box>

      {/* セクションコンテンツ */}
      <Box sx={{ p: 2 }}>
        {/* バージョン */}
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            pb: 1.5,
            borderBottom: '1px solid',
            borderColor: 'divider'
          }}
        >
          <Typography variant="body2">バージョン</Typography>
          <Typography variant="body2" color="text.secondary">
            v1.0.0
          </Typography>
        </Box>

        {/* 利用規約 */}
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            py: 1.5,
            borderBottom: '1px solid',
            borderColor: 'divider'
          }}
        >
          <Typography variant="body2">利用規約</Typography>
          <Link
            href="#"
            variant="body2"
            color="text.secondary"
            sx={{
              opacity: 0.5,
              pointerEvents: 'none',
              textDecoration: 'none'
            }}
          >
            準備中
          </Link>
        </Box>

        {/* プライバシーポリシー */}
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            pt: 1.5
          }}
        >
          <Typography variant="body2">プライバシーポリシー</Typography>
          <Link
            href="#"
            variant="body2"
            color="text.secondary"
            sx={{
              opacity: 0.5,
              pointerEvents: 'none',
              textDecoration: 'none'
            }}
          >
            準備中
          </Link>
        </Box>
      </Box>
    </Box>
  );
};
