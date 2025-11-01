// ListPage - 命式リストページ
import { Box, Typography, Container, Button } from '@mui/material';
import { Add } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { MainLayout } from '../layouts/MainLayout';
import { Header } from '../components/Header';
import { Sidebar } from '../components/Sidebar';

export const ListPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <MainLayout header={<Header />} sidebar={<Sidebar />}>
      <Container maxWidth="lg">
        <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <Typography variant="h4" gutterBottom sx={{ fontWeight: 700 }}>
              命式リスト
            </Typography>
            <Typography variant="body1" color="text.secondary">
              保存した命式を管理します。
            </Typography>
          </div>
          <Button
            variant="contained"
            startIcon={<Add />}
            onClick={() => navigate('/')}
          >
            新規作成
          </Button>
        </Box>

        {/* TODO: 命式カード一覧を実装 */}
        <Box
          sx={{
            p: 4,
            backgroundColor: 'white',
            borderRadius: 2,
            textAlign: 'center',
          }}
        >
          <Typography variant="h6" color="text.secondary">
            命式カード一覧（実装予定）
          </Typography>
        </Box>
      </Container>
    </MainLayout>
  );
};

export default ListPage;
