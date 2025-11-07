// SettingsPage - 設定ページ
import { Box, Typography, Paper, Divider, Button, IconButton, Alert, Stack } from '@mui/material';
import { ArrowBack, PersonAdd, Login, Logout } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { BottomNavigation } from '../components/BottomNavigation';
import { useAuth } from '../features/auth/hooks/useAuth';
import { useState } from 'react';

if (!import.meta.env.VITE_API_URL) {
  throw new Error('VITE_API_URL environment variable is not set');
}
const API_BASE_URL = import.meta.env.VITE_API_URL;

export const SettingsPage: React.FC = () => {
  const navigate = useNavigate();
  const { user, isAuthenticated, logout } = useAuth();
  const [isExporting, setIsExporting] = useState(false);

  const handleLogout = async () => {
    if (confirm('ログアウトしますか？')) {
      try {
        await logout();
        // ログアウト後も設定ページにとどまる（ページはリロードされる）
        window.location.reload();
      } catch (error) {
        console.error('Logout error:', error);
        alert('ログアウトに失敗しました');
      }
    }
  };

  const handleExport = async () => {
    setIsExporting(true);
    try {
      const authData = localStorage.getItem('auth');
      if (!authData) {
        throw new Error('認証情報が見つかりません');
      }
      const { token } = JSON.parse(authData);
      const response = await fetch(`${API_BASE_URL}/api/saju/export`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('エクスポートに失敗しました');
      }

      const data = await response.json();
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `golden-saju-export-${new Date().toISOString().split('T')[0]}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Export error:', error);
      alert('エクスポートに失敗しました');
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <Box sx={{ width: '100%', minHeight: '100vh', backgroundColor: 'background.paper' }}>
      {/* カスタムヘッダー */}
      <Box
        sx={{
          position: 'sticky',
          top: 0,
          background: 'linear-gradient(135deg, #D4AF37 0%, #B8941C 100%)',
          color: 'white',
          padding: { xs: '16px 20px', md: '20px 32px' },
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          boxShadow: '0 2px 8px rgba(212, 175, 55, 0.3)',
          zIndex: 100,
          borderRadius: { xs: 0, md: '0 0 16px 16px' },
        }}
      >
        <IconButton onClick={() => navigate('/list')} sx={{ color: 'white', width: 48, height: 48 }} aria-label="リストページに戻る">
          <ArrowBack />
        </IconButton>
        <Typography
          variant="h6"
          sx={{
            fontWeight: { xs: 600, md: 700 },
            fontSize: { xs: '18px', md: '24px', lg: '28px' },
          }}
        >
          設定
        </Typography>
        <Box sx={{ width: 48 }} /> {/* スペーサー */}
      </Box>

      {/* メインコンテンツ */}
      <Box sx={{ maxWidth: { xs: '100%', md: '900px', lg: '1400px' }, mx: 'auto', px: { xs: '20px', md: '24px', lg: '40px' }, pb: { xs: '100px', md: '110px' }, pt: { xs: '20px', md: '30px' } }}>

        {/* ゲストユーザー向け：アカウント管理（ログイン/新規登録） */}
        {!isAuthenticated && (
          <Paper sx={{ p: { xs: 2, sm: 3, md: 4 }, mb: 3 }}>
            <Typography
              variant="h6"
              gutterBottom
              sx={{
                fontSize: { xs: '18px', md: '22px', lg: '24px' },
                fontWeight: 700,
                display: 'flex',
                alignItems: 'center',
                gap: 1
              }}
            >
              <span>👤</span>
              アカウント管理
            </Typography>

            <Alert severity="info" sx={{ mb: { xs: 2, md: 3 } }}>
              ログインすると、複数端末でデータを同期できます。
            </Alert>

            <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
              <Button
                variant="contained"
                onClick={() => navigate('/register')}
                startIcon={<PersonAdd />}
                sx={{
                  minHeight: '48px',
                  fontSize: { xs: '16px', md: '18px' },
                  fontWeight: 600,
                  flex: { xs: 'none', sm: 1 },
                  background: '#D4AF37',
                  '&:hover': {
                    background: '#B8941C'
                  }
                }}
              >
                新規登録
              </Button>
              <Button
                variant="outlined"
                onClick={() => navigate('/login')}
                startIcon={<Login />}
                sx={{
                  minHeight: '48px',
                  fontSize: { xs: '16px', md: '18px' },
                  fontWeight: 600,
                  flex: { xs: 'none', sm: 1 },
                  borderColor: '#D4AF37',
                  borderWidth: '2px',
                  color: '#D4AF37',
                  '&:hover': {
                    borderColor: '#B8941C',
                    borderWidth: '2px',
                    color: '#B8941C',
                    background: 'rgba(212, 175, 55, 0.05)'
                  }
                }}
              >
                ログイン
              </Button>
            </Stack>
          </Paper>
        )}

        {/* ログインユーザー向け：アカウント情報 */}
        {isAuthenticated && (
          <Paper sx={{ p: { xs: 2, sm: 3, md: 4 }, mb: 3 }}>
            <Typography
              variant="h6"
              gutterBottom
              sx={{
                fontSize: { xs: '18px', md: '22px', lg: '24px' },
                fontWeight: 700,
                display: 'flex',
                alignItems: 'center',
                gap: 1
              }}
            >
              <span>👤</span>
              アカウント情報
            </Typography>
            <Box sx={{ mt: 2 }}>
              <Typography variant="body2" color="text.secondary">
                メールアドレス
              </Typography>
              <Typography variant="body1">{user?.email}</Typography>
            </Box>
            <Box sx={{ mt: 2 }}>
              <Typography variant="body2" color="text.secondary">
                ユーザー名
              </Typography>
              <Typography variant="body1">{user?.profile?.name}</Typography>
            </Box>
            <Box sx={{ mt: 2 }}>
              <Typography variant="body2" color="text.secondary">
                権限
              </Typography>
              <Typography variant="body1">{user?.role}</Typography>
            </Box>

            <Divider sx={{ my: 3 }} />

            {/* ログアウトボタン */}
            <Button
              variant="outlined"
              onClick={handleLogout}
              startIcon={<Logout />}
              fullWidth
              sx={{
                minHeight: '48px',
                fontSize: { xs: '16px', md: '18px' },
                fontWeight: 600,
                borderColor: '#F44336',
                borderWidth: '2px',
                color: '#F44336',
                '&:hover': {
                  borderColor: '#D32F2F',
                  borderWidth: '2px',
                  color: '#D32F2F',
                  background: 'rgba(244, 67, 54, 0.05)'
                }
              }}
            >
              ログアウト
            </Button>
          </Paper>
        )}

        <Divider sx={{ my: 3 }} />

        {/* データ管理 */}
        <Paper sx={{ p: { xs: 2, sm: 3, md: 4 }, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            データ管理
          </Typography>
          <Box sx={{ mt: 2 }}>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              保存された命式データをJSON形式でエクスポートします。
            </Typography>
            <Button
              variant="contained"
              onClick={handleExport}
              disabled={isExporting}
              data-testid="export-button"
              sx={{
                background: '#D4AF37', // 通常の金色
                color: 'white', // 白文字
                fontWeight: 600,
                boxShadow: 'none',
                '&:hover': {
                  background: '#B8941C', // ホバー時は濃い金色
                  boxShadow: 'none',
                },
                '&:disabled': {
                  background: '#E0E0E0',
                  color: '#9E9E9E',
                },
              }}
            >
              {isExporting ? 'エクスポート中...' : 'データをエクスポート'}
            </Button>
          </Box>
        </Paper>

        <Divider sx={{ my: 3 }} />

        {/* アプリ情報 */}
        <Paper sx={{ p: { xs: 2, sm: 3, md: 4 } }}>
          <Typography variant="h6" gutterBottom>
            アプリ情報
          </Typography>
          <Box sx={{ mt: 2 }}>
            <Typography variant="body2" color="text.secondary">
              バージョン
            </Typography>
            <Typography variant="body1">v1.0.0</Typography>
          </Box>
        </Paper>
      </Box>

      {/* ボトムナビゲーション */}
      <BottomNavigation />
    </Box>
  );
};

export default SettingsPage;
