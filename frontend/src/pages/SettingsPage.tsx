// SettingsPage - 設定ページ
import { Box, Typography, Container, Paper, Divider } from '@mui/material';
import { MainLayout } from '../layouts/MainLayout';
import { Header } from '../components/Header';
import { Sidebar } from '../components/Sidebar';
import { useAuth } from '../features/auth/hooks/useAuth';

export const SettingsPage: React.FC = () => {
  const { user } = useAuth();

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
