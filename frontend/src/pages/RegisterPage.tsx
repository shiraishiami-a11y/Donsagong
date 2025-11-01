// RegisterPage - 新規登録ページ
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  TextField,
  Button,
  Link,
  Alert,
  Checkbox,
  FormControlLabel,
} from '@mui/material';
import { PublicLayout } from '../layouts/PublicLayout';
import { useAuth } from '../features/auth/hooks/useAuth';

export const RegisterPage: React.FC = () => {
  const navigate = useNavigate();
  const { register } = useAuth();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');
  const [migrateGuestData, setMigrateGuestData] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (password !== passwordConfirm) {
      setError('パスワードが一致しません');
      return;
    }

    if (password.length < 8) {
      setError('パスワードは8文字以上である必要があります');
      return;
    }

    setLoading(true);

    try {
      await register({ email, password, migrateGuestData });
      navigate('/list', { replace: true });
    } catch (err) {
      setError('登録に失敗しました。このメールアドレスは既に使用されています。');
    } finally {
      setLoading(false);
    }
  };

  return (
    <PublicLayout>
      <Typography variant="h4" align="center" gutterBottom sx={{ fontWeight: 700 }}>
        新規登録
      </Typography>
      <Typography variant="body2" align="center" color="text.secondary" sx={{ mb: 3 }}>
        アカウントを作成してクラウドに保存
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
          autoComplete="new-password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <TextField
          margin="normal"
          required
          fullWidth
          name="passwordConfirm"
          label="パスワード（確認）"
          type="password"
          id="passwordConfirm"
          value={passwordConfirm}
          onChange={(e) => setPasswordConfirm(e.target.value)}
        />
        <FormControlLabel
          control={
            <Checkbox
              checked={migrateGuestData}
              onChange={(e) => setMigrateGuestData(e.target.checked)}
              color="primary"
            />
          }
          label="ゲストデータを移行する"
        />
        <Button
          type="submit"
          fullWidth
          variant="contained"
          sx={{ mt: 3, mb: 2 }}
          disabled={loading}
        >
          {loading ? '登録中...' : '登録'}
        </Button>
        <Box sx={{ textAlign: 'center' }}>
          <Link
            component="button"
            variant="body2"
            onClick={() => navigate('/login')}
            sx={{ cursor: 'pointer' }}
          >
            ログインはこちら
          </Link>
        </Box>
      </Box>
    </PublicLayout>
  );
};

export default RegisterPage;
