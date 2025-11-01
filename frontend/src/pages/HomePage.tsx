// HomePage - 命式記入ページ（トップページ）
import { Box, Typography, Container } from '@mui/material';
import { MainLayout } from '../layouts/MainLayout';
import { Header } from '../components/Header';
import { Sidebar } from '../components/Sidebar';

export const HomePage: React.FC = () => {
  return (
    <MainLayout header={<Header />} sidebar={<Sidebar />}>
      <Container maxWidth="lg">
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" gutterBottom sx={{ fontWeight: 700 }}>
            命式記入
          </Typography>
          <Typography variant="body1" color="text.secondary">
            生年月日時を入力して、あなたの運命を計算します。
          </Typography>
        </Box>

        {/* TODO: 命式入力フォームを実装 */}
        <Box
          sx={{
            p: 4,
            backgroundColor: 'white',
            borderRadius: 2,
            textAlign: 'center',
          }}
        >
          <Typography variant="h6" color="text.secondary">
            命式入力フォーム（実装予定）
          </Typography>
        </Box>
      </Container>
    </MainLayout>
  );
};

export default HomePage;
