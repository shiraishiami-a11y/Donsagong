// SettingsPage - 設定ページ
import { Box, Typography, Container, Paper, Divider, Button } from '@mui/material';
import { MainLayout } from '../layouts/MainLayout';
import { Header } from '../components/Header';
import { Sidebar } from '../components/Sidebar';
import { useAuth } from '../features/auth/hooks/useAuth';
import { useState } from 'react';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8432';

export const SettingsPage: React.FC = () => {
  const { user } = useAuth();
  const [isExporting, setIsExporting] = useState(false);

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
    <MainLayout header={<Header />} sidebar={<Sidebar />}>
      <Container maxWidth="lg">
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" gutterBottom sx={{ fontWeight: 700 }}>
            設定
          </Typography>
          <Typography variant="body1" color="text.secondary">
            アカウント設定とアプリ設定を管理します。
          </Typography>
        </Box>

        {/* アカウント情報 */}
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
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
        </Paper>

        <Divider sx={{ my: 3 }} />

        {/* データ管理 */}
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            データ管理
          </Typography>
          <Box sx={{ mt: 2 }}>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              保存された命式データをJSON形式でエクスポートします。
            </Typography>
            <Button
              variant="contained"
              color="primary"
              onClick={handleExport}
              disabled={isExporting}
              data-testid="export-button"
            >
              {isExporting ? 'エクスポート中...' : 'データをエクスポート'}
            </Button>
          </Box>
        </Paper>

        <Divider sx={{ my: 3 }} />

        {/* アプリ情報 */}
        <Paper sx={{ p: 3 }}>
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
      </Container>
    </MainLayout>
  );
};

export default SettingsPage;
