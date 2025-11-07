// LoginPage - P-AUTH-1: ログインページ
// モックアップ: mockups/LoginPage.html に完全準拠
import { useState } from 'react';
import { useNavigate, useLocation, Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Typography,
  TextField,
  Button,
  Link,
  Checkbox,
  FormControlLabel,
  Alert,
  IconButton,
  InputAdornment,
} from '@mui/material';
import {
  Visibility,
  VisibilityOff,
} from '@mui/icons-material';
import { useAuth } from '../features/auth/hooks/useAuth';

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const from = (location.state as any)?.from?.pathname || '/list';

  const handleLogin = async () => {
    console.log('[LoginPage] handleLogin called', { email, password: '***' });

    // バリデーション
    if (!email || !password) {
      setError('メールアドレスとパスワードを入力してください');
      console.log('[LoginPage] Validation failed');
      return;
    }

    setIsLoading(true);
    setError('');
    console.log('[LoginPage] Calling login function...');

    try {
      await login({ email, password, rememberMe });
      console.log('[LoginPage] Login success');
      // 成功時はコンテキストがユーザー情報を保持し、navigate
      navigate(from, { replace: true });
    } catch (err) {
      console.error('[LoginPage] Login error:', err);
      setError('メールアドレスまたはパスワードが正しくありません');
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleLogin();
    }
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%)',
        padding: { xs: '20px', sm: '40px' },
      }}
    >
      <Box
        sx={{
          width: '100%',
          maxWidth: {
            xs: '100%',
            sm: '480px',
            md: '600px',
          },
          margin: '0 auto',
        }}
      >
        {/* ヘッダー */}
        <Box sx={{ textAlign: 'center', mb: { xs: 4, sm: 6 } }}>
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: 1,
              mb: 1,
            }}
          >
            <Typography
              sx={{
                fontSize: { xs: '32px', sm: '42px', md: '56px' },
              }}
            >
              ✨
            </Typography>
            <Typography
              sx={{
                fontSize: { xs: '32px', sm: '42px', md: '56px' },
                fontWeight: 700,
                color: '#D4AF37',
              }}
            >
              ゴールデン四柱推命
            </Typography>
          </Box>
          <Typography
            sx={{
              fontSize: { xs: '14px', sm: '16px', md: '18px' },
              color: '#666',
              fontWeight: 500,
            }}
          >
            あなたの運命に魔法をかける
          </Typography>
        </Box>

        {/* ログインカード */}
        <Box
          sx={{
            background: '#FFFFFF',
            borderRadius: { xs: '16px', sm: '24px' },
            boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
            padding: {
              xs: '28px',
              sm: '40px',
              md: '50px 60px',
            },
            mb: { xs: 2.5, sm: 3 },
          }}
        >
          {/* タイトルセクション */}
          <Box sx={{ textAlign: 'center', mb: { xs: 3, sm: 4 } }}>
            <Typography
              sx={{
                fontSize: { xs: '22px', sm: '26px', md: '32px' },
                fontWeight: 700,
                color: '#1a1a2e',
                mb: { xs: 3, sm: 4 },
              }}
            >
              ログイン
            </Typography>
          </Box>

          {/* エラーメッセージ */}
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          {/* フォームセクション */}
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: { xs: 2.5, sm: 3.5 }, mb: 3 }}>
            {/* メールアドレス入力 */}
            <Box>
              <Typography
                sx={{
                  fontSize: { xs: '14px', sm: '16px' },
                  fontWeight: 600,
                  color: '#333',
                  mb: { xs: 1, sm: 1.5 },
                }}
              >
                メールアドレス
              </Typography>
              <TextField
                type="email"
                id="email"
                placeholder="example@email.com"
                autoComplete="email"
                fullWidth
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                onKeyPress={handleKeyPress}
                inputProps={{
                  'data-testid': 'email',
                }}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    borderRadius: { xs: '8px', sm: '12px' },
                    fontSize: { xs: '16px', sm: '18px' },
                    '& input': {
                      padding: { xs: '14px 16px', sm: '16px 20px' },
                    },
                    '& fieldset': {
                      borderWidth: '2px',
                      borderColor: '#e0e0e0',
                    },
                    '&:hover fieldset': {
                      borderColor: '#D4AF37',
                    },
                    '&.Mui-focused fieldset': {
                      borderColor: '#D4AF37',
                      boxShadow: '0 0 0 3px rgba(212, 175, 55, 0.1)',
                    },
                  },
                }}
              />
            </Box>

            {/* パスワード入力 */}
            <Box>
              <Typography
                sx={{
                  fontSize: { xs: '14px', sm: '16px' },
                  fontWeight: 600,
                  color: '#333',
                  mb: { xs: 1, sm: 1.5 },
                }}
              >
                パスワード
              </Typography>
              <TextField
                type={showPassword ? 'text' : 'password'}
                id="password"
                placeholder="パスワードを入力"
                autoComplete="current-password"
                fullWidth
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                onKeyPress={handleKeyPress}
                inputProps={{
                  'data-testid': 'password',
                }}
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton
                        onClick={() => setShowPassword(!showPassword)}
                        edge="end"
                        sx={{
                          color: '#757575',
                          '&:hover': { color: '#D4AF37' },
                        }}
                      >
                        {showPassword ? <VisibilityOff /> : <Visibility />}
                      </IconButton>
                    </InputAdornment>
                  ),
                }}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    borderRadius: { xs: '8px', sm: '12px' },
                    fontSize: { xs: '16px', sm: '18px' },
                    '& input': {
                      padding: { xs: '14px 16px', sm: '16px 20px' },
                    },
                    '& fieldset': {
                      borderWidth: '2px',
                      borderColor: '#e0e0e0',
                    },
                    '&:hover fieldset': {
                      borderColor: '#D4AF37',
                    },
                    '&.Mui-focused fieldset': {
                      borderColor: '#D4AF37',
                      boxShadow: '0 0 0 3px rgba(212, 175, 55, 0.1)',
                    },
                  },
                }}
              />
            </Box>

            {/* ログイン状態を保持 */}
            <FormControlLabel
              control={
                <Checkbox
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  sx={{
                    color: '#D4AF37',
                    width: { xs: 20, sm: 24 },
                    height: { xs: 20, sm: 24 },
                    '&.Mui-checked': {
                      color: '#D4AF37',
                    },
                  }}
                />
              }
              label={
                <Typography sx={{ fontSize: { xs: '14px', sm: '16px' }, color: '#666' }}>
                  ログイン状態を保持
                </Typography>
              }
              sx={{ mt: { xs: 2, sm: 0 } }}
            />
          </Box>

          {/* パスワードを忘れた */}
          <Box sx={{ textAlign: 'right', mt: 1, mb: 2 }}>
            <Link
              href="#"
              onClick={(e: React.MouseEvent) => {
                e.preventDefault();
                alert('パスワード再設定メールを送信します');
              }}
              sx={{
                color: '#D4AF37',
                textDecoration: 'none',
                fontSize: { xs: '14px', md: '15px' },
                fontWeight: 500,
                minHeight: '44px',
                display: 'inline-flex',
                alignItems: 'center',
                transition: 'all 0.2s',
                '&:hover': {
                  textDecoration: 'underline',
                },
              }}
            >
              パスワードを忘れた場合
            </Link>
          </Box>

          {/* ボタンセクション */}
          <Box sx={{ display: 'flex', flexDirection: 'column', mb: 3 }}>
            <Button
              data-testid="login-button"
              onClick={handleLogin}
              disabled={isLoading}
              sx={{
                width: '100%',
                padding: { xs: '16px', sm: '20px' },
                background: '#D4AF37',
                color: 'white',
                borderRadius: { xs: '12px', sm: '16px' },
                fontSize: { xs: '18px', sm: '20px' },
                fontWeight: 700,
                boxShadow: '0 4px 12px rgba(212, 175, 55, 0.3)',
                textTransform: 'none',
                transition: 'all 0.2s',
                '&:hover': {
                  background: '#B8941C',
                  transform: 'translateY(-2px)',
                  boxShadow: '0 6px 16px rgba(212, 175, 55, 0.4)',
                },
                '&:active': {
                  transform: 'translateY(0)',
                },
                '&:disabled': {
                  background: '#E0E0E0',
                  color: '#9E9E9E',
                },
              }}
            >
              {isLoading ? 'ログイン中...' : 'ログイン'}
            </Button>

            {/* ディバイダー「または」 */}
            <Box
              sx={{
                display: 'flex',
                alignItems: 'center',
                gap: 2,
                my: { xs: 3, sm: 4 },
              }}
            >
              <Box sx={{ flex: 1, height: '1px', background: '#e0e0e0' }} />
              <Typography sx={{ fontSize: { xs: '14px', sm: '16px' }, color: '#999' }}>
                または
              </Typography>
              <Box sx={{ flex: 1, height: '1px', background: '#e0e0e0' }} />
            </Box>

            {/* ゲストモードボタン */}
            <Button
              onClick={() => {
                alert('ゲストモードで利用を開始します\n（データはこの端末のみに保存されます）');
                navigate('/');
              }}
              sx={{
                width: '100%',
                padding: { xs: '16px', sm: '20px' },
                background: 'white',
                color: '#666',
                border: '2px solid #e0e0e0',
                borderRadius: { xs: '12px', sm: '16px' },
                fontSize: { xs: '18px', sm: '20px' },
                fontWeight: 700,
                textTransform: 'none',
                transition: 'all 0.2s',
                '&:hover': {
                  borderColor: '#D4AF37',
                  color: '#D4AF37',
                },
                '&:active': {
                  transform: 'translateY(0)',
                },
              }}
            >
              ゲストとして利用
            </Button>
          </Box>
        </Box>

        {/* フッター */}
        <Box sx={{ textAlign: 'center', mt: { xs: 2.5, sm: 3 } }}>
          <Typography
            sx={{
              fontSize: { xs: '14px', sm: '16px' },
              color: '#666',
            }}
          >
            アカウントをお持ちでない場合{' '}
            <Link
              component={RouterLink}
              to="/register"
              sx={{
                color: '#D4AF37',
                fontWeight: 600,
                textDecoration: 'none',
                transition: 'all 0.2s',
                '&:hover': {
                  textDecoration: 'underline',
                },
              }}
            >
              新規登録
            </Link>
          </Typography>
        </Box>
      </Box>
    </Box>
  );
};

export default LoginPage;
