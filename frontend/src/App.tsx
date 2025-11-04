// App.tsx - メインアプリケーションコンポーネント
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { AuthProvider } from './features/auth/contexts/AuthContext';
import TopPage from './pages/TopPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ListPage from './pages/ListPage/';
import SettingsPage from './pages/SettingsPage';
import SajuDetailPage from './pages/SajuDetailPage';

// ゴールドテーマを作成
const theme = createTheme({
  palette: {
    primary: {
      main: '#D4AF37', // ゴールド
      light: '#F4E8C1',
      dark: '#B8941C',
    },
  },
  breakpoints: {
    values: {
      xs: 0,
      sm: 600,
      md: 768,  // タブレット: 768px
      lg: 1200, // PC: 1200px
      xl: 1536,
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            {/* 公開ルート（認証不要） */}
            <Route path="/" element={<TopPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />

            {/* ゲスト・ログイン共通ルート */}
            <Route path="/list" element={<ListPage />} />
            <Route path="/detail/:id" element={<SajuDetailPage />} />
            <Route path="/settings" element={<SettingsPage />} />

            {/* 未定義のパスはトップページにリダイレクト */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
