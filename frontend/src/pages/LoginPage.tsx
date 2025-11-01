// LoginPage - ログインページ
import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Box,
  Typography,
  TextField,
  Button,
  Link,
  Checkbox,
  FormControlLabel,
  Alert,
} from '@mui/material';
import { PublicLayout } from '../layouts/PublicLayout';
import { useAuth } from '../features/auth/hooks/useAuth';

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(true);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const from = (location.state as any)?.from?.pathname || '/list';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await login({ email, password, rememberMe });
      navigate(from, { replace: true });
    } catch (err) {
      setError('メールアドレスまたはパスワードが正しくありません');
    } finally {
      setLoading(false);
    }
  };

  return (
    <PublicLayout>
      <Typography variant="h4" align="center" gutterBottom sx={{ fontWeight: 700 }}>
        ログイン
      </Typography>
      <Typography variant="body2" align="center" color="text.secondary" sx={{ mb: 3 }}>
        ゴールデン四柱推命へようこそ
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Box component="form" onSubmit={handleSubmit} noValidate>
        <TextField
          margin="normal"
          required
          fullWidth
          id="email"
          label="メールアドレス"
          name="email"
          autoComplete="email"
          autoFocus
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <TextField
          margin="normal"
          required
          fullWidth
          name="password"
          label="パスワード"
          type="password"
          id="password"
          autoComplete="current-password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <FormControlLabel
          control={
            <Checkbox
              checked={rememberMe}
              onChange={(e) => setRememberMe(e.target.checked)}
              color="primary"
            />
          }
          label="ログイン状態を保持"
        />
        <Button
          type="submit"
          fullWidth
          variant="contained"
          sx={{ mt: 3, mb: 2 }}
          disabled={loading}
        >
          {loading ? 'ログイン中...' : 'ログイン'}
        </Button>
        <Box sx={{ textAlign: 'center' }}>
          <Link
            component="button"
            variant="body2"
            onClick={() => navigate('/register')}
            sx={{ cursor: 'pointer' }}
          >
            新規登録はこちら
          </Link>
        </Box>
      </Box>

      {/* デモアカウント情報 */}
      <Box sx={{ mt: 4, p: 2, backgroundColor: '#fafafa', borderRadius: 1 }}>
        <Typography variant="caption" display="block" gutterBottom>
          <strong>デモアカウント:</strong>
        </Typography>
        <Typography variant="caption" display="block">
          メール: demo@goldensaju.local
        </Typography>
        <Typography variant="caption" display="block">
          パスワード: demo123
        </Typography>
      </Box>
    </PublicLayout>
  );
};

export default LoginPage;
