// PublicLayout - 公開ページ用レイアウト（Login, Register等）
import { Box, AppBar, Toolbar, Typography, Container, Paper } from '@mui/material';
import type { LayoutProps } from '../types';

export const PublicLayout: React.FC<LayoutProps> = ({ children, maxWidth = 'sm' }) => {
  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        background: 'linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%)',
      }}
    >
      {/* ヘッダー */}
      <AppBar
        position="static"
        elevation={0}
        sx={{
          background: 'linear-gradient(135deg, #D4AF37 0%, #B8941C 100%)',
        }}
      >
        <Toolbar>
          <Typography variant="h6" sx={{ fontWeight: 700, color: 'white' }}>
            Golden Peppa
          </Typography>
        </Toolbar>
      </AppBar>

      {/* メインコンテンツ（中央揃え） */}
      <Box
        sx={{
          flexGrow: 1,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          p: 3,
        }}
      >
        <Container maxWidth={maxWidth}>
          <Paper
            elevation={3}
            sx={{
              p: 4,
              borderRadius: 2,
              background: 'white',
              boxShadow: '0 8px 24px rgba(212, 175, 55, 0.15)',
            }}
          >
            {children}
          </Paper>
        </Container>
      </Box>
    </Box>
  );
};

export default PublicLayout;
