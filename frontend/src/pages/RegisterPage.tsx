// RegisterPage - 新規登録ページ（モックアップ完全準拠）
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Typography, TextField, Button, Checkbox, FormControlLabel, Alert } from '@mui/material';
import { useAuth } from '../features/auth/hooks/useAuth';

export const RegisterPage: React.FC = () => {
  const navigate = useNavigate();
  const { register } = useAuth();

  // フォーム状態
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');
  const [name, setName] = useState('');
  const [agreedToTerms, setAgreedToTerms] = useState(false);

  // UI状態
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // パスワード強度計算
  const calculatePasswordStrength = (pwd: string): { level: number; text: string; color: string } => {
    if (pwd.length === 0) {
      return { level: 0, text: '', color: '' };
    }

    let strength = 0;
    if (pwd.length >= 8) strength++;
    if (/[a-z]/.test(pwd)) strength++;
    if (/[A-Z]/.test(pwd)) strength++;
    if (/[0-9]/.test(pwd)) strength++;
    if (/[^a-zA-Z0-9]/.test(pwd)) strength++;

    if (strength <= 2) {
      return { level: 1, text: '弱い', color: '#f44336' };
    } else if (strength <= 3) {
      return { level: 2, text: '普通', color: '#FF9800' };
    } else {
      return { level: 3, text: '強い', color: '#4CAF50' };
    }
  };

  const passwordStrength = calculatePasswordStrength(password);

  // フォームバリデーション
  const isFormValid = () => {
    return agreedToTerms && password.length >= 8 && email.includes('@');
  };

  // 新規登録処理
  const handleRegister = async () => {
    setError('');

    if (password !== passwordConfirm) {
      setError('パスワードが一致しません');
      return;
    }

    if (password.length < 8) {
      setError('パスワードは8文字以上である必要があります');
      return;
    }

    if (!agreedToTerms) {
      setError('利用規約とプライバシーポリシーに同意してください');
      return;
    }

    setLoading(true);

    try {
      await register({ email, password, name, migrateGuestData: false });
      navigate('/list', { replace: true });
    } catch (err) {
      setError('登録に失敗しました。このメールアドレスは既に使用されています。');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: { xs: '20px', sm: '40px' },
      }}
    >
      <Box
        sx={{
          width: '100%',
          maxWidth: { xs: '100%', sm: '480px', md: '600px' },
        }}
      >
        {/* ヘッダー */}
        <Box
          sx={{
            textAlign: 'center',
            mb: { xs: 4, sm: 6 },
          }}
        >
          <Box
            sx={{
              fontSize: { xs: '32px', sm: '42px', md: '56px' },
              fontWeight: 700,
              color: '#D4AF37',
              mb: { xs: 1, sm: 1.5 },
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: { xs: 1, sm: 1.5 },
            }}
          >
            <span>✨</span>
            <span>ゴールデン四柱推命</span>
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

        {/* 新規登録カード */}
        <Box
          sx={{
            background: 'white',
            borderRadius: { xs: '16px', sm: '24px' },
            padding: { xs: '28px', sm: '40px', md: '50px 60px' },
            boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
            mb: { xs: 2.5, sm: 3 },
          }}
        >
          <Typography
            variant="h2"
            sx={{
              fontSize: { xs: '22px', sm: '26px', md: '32px' },
              fontWeight: 700,
              color: '#1a1a2e',
              mb: { xs: 3, sm: 4 },
              textAlign: 'center',
            }}
          >
            新規登録
          </Typography>

          {/* 特典リスト */}
          <Box
            sx={{
              background: '#fffbf0',
              borderRadius: { xs: '12px', sm: '16px' },
              padding: { xs: '16px', sm: '20px' },
              mb: { xs: 3, sm: 4 },
            }}
          >
            <Box
              sx={{
                fontSize: { xs: '14px', sm: '16px' },
                fontWeight: 600,
                color: '#D4AF37',
                mb: 1.5,
                display: 'flex',
                alignItems: 'center',
                gap: 0.75,
              }}
            >
              <span>🎁</span>
              <span>アカウント登録の特典</span>
            </Box>
            <Box component="ul" sx={{ listStyle: 'none', padding: 0, margin: 0 }}>
              {[
                '複数端末でデータ同期',
                '命式データの永続保存',
                'データのバックアップ',
                '運勢リマインダー機能',
              ].map((benefit) => (
                <Box
                  component="li"
                  key={benefit}
                  sx={{
                    fontSize: { xs: '13px', sm: '15px' },
                    color: '#666',
                    mb: 1,
                    display: 'flex',
                    alignItems: 'center',
                    gap: 1,
                    '&:before': {
                      content: '"✓"',
                      color: '#D4AF37',
                      fontWeight: 700,
                      fontSize: '16px',
                    },
                  }}
                >
                  {benefit}
                </Box>
              ))}
            </Box>
          </Box>

          {/* エラー表示 */}
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          {/* フォーム */}
          <Box component="form">
            {/* メールアドレス */}
            <Box sx={{ mb: { xs: 2.5, sm: 3.5 } }}>
              <Typography
                component="label"
                sx={{
                  display: 'block',
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
                fullWidth
                placeholder="example@goldensaju.local"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    fontSize: { xs: '16px', sm: '18px' },
                    borderRadius: { xs: '8px', sm: '12px' },
                    '& fieldset': {
                      borderWidth: '2px',
                      borderColor: '#e0e0e0',
                    },
                    '&:hover fieldset': {
                      borderColor: '#e0e0e0',
                    },
                    '&.Mui-focused fieldset': {
                      borderColor: '#D4AF37',
                      boxShadow: '0 0 0 3px rgba(212, 175, 55, 0.1)',
                    },
                  },
                  '& .MuiOutlinedInput-input': {
                    padding: { xs: '14px 16px', sm: '16px 20px' },
                  },
                }}
              />
              <Typography
                sx={{
                  fontSize: { xs: '12px', sm: '14px' },
                  color: '#999',
                  mt: 0.5,
                }}
              >
                登録後、確認メールをお送りします
              </Typography>
            </Box>

            {/* パスワード */}
            <Box sx={{ mb: { xs: 2.5, sm: 3.5 } }}>
              <Typography
                component="label"
                sx={{
                  display: 'block',
                  fontSize: { xs: '14px', sm: '16px' },
                  fontWeight: 600,
                  color: '#333',
                  mb: { xs: 1, sm: 1.5 },
                }}
              >
                パスワード
              </Typography>
              <TextField
                type="password"
                fullWidth
                placeholder="8文字以上"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    fontSize: { xs: '16px', sm: '18px' },
                    borderRadius: { xs: '8px', sm: '12px' },
                    '& fieldset': {
                      borderWidth: '2px',
                      borderColor: '#e0e0e0',
                    },
                    '&:hover fieldset': {
                      borderColor: '#e0e0e0',
                    },
                    '&.Mui-focused fieldset': {
                      borderColor: '#D4AF37',
                      boxShadow: '0 0 0 3px rgba(212, 175, 55, 0.1)',
                    },
                  },
                  '& .MuiOutlinedInput-input': {
                    padding: { xs: '14px 16px', sm: '16px 20px' },
                  },
                }}
              />

              {/* パスワード強度インジケータ */}
              <Box sx={{ display: 'flex', gap: 0.5, mt: 1 }}>
                {[1, 2, 3].map((barIndex) => (
                  <Box
                    key={barIndex}
                    sx={{
                      flex: 1,
                      height: { xs: '4px', md: '6px' },
                      background:
                        passwordStrength.level >= barIndex ? passwordStrength.color : '#e0e0e0',
                      borderRadius: '2px',
                      transition: 'all 0.3s',
                    }}
                  />
                ))}
              </Box>
              {passwordStrength.text && (
                <Typography
                  sx={{
                    fontSize: { xs: '12px', md: '14px' },
                    color: passwordStrength.color,
                    mt: 0.5,
                  }}
                >
                  {passwordStrength.text}
                </Typography>
              )}
              <Typography
                sx={{
                  fontSize: { xs: '12px', sm: '14px' },
                  color: '#999',
                  mt: 0.5,
                }}
              >
                8文字以上、英字・数字を含む
              </Typography>
            </Box>

            {/* パスワード確認 */}
            <Box sx={{ mb: { xs: 2.5, sm: 3.5 } }}>
              <Typography
                component="label"
                sx={{
                  display: 'block',
                  fontSize: { xs: '14px', sm: '16px' },
                  fontWeight: 600,
                  color: '#333',
                  mb: { xs: 1, sm: 1.5 },
                }}
              >
                パスワード（確認）
              </Typography>
              <TextField
                type="password"
                fullWidth
                placeholder="もう一度入力"
                value={passwordConfirm}
                onChange={(e) => setPasswordConfirm(e.target.value)}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    fontSize: { xs: '16px', sm: '18px' },
                    borderRadius: { xs: '8px', sm: '12px' },
                    '& fieldset': {
                      borderWidth: '2px',
                      borderColor: '#e0e0e0',
                    },
                    '&:hover fieldset': {
                      borderColor: '#e0e0e0',
                    },
                    '&.Mui-focused fieldset': {
                      borderColor: '#D4AF37',
                      boxShadow: '0 0 0 3px rgba(212, 175, 55, 0.1)',
                    },
                  },
                  '& .MuiOutlinedInput-input': {
                    padding: { xs: '14px 16px', sm: '16px 20px' },
                  },
                }}
              />
            </Box>

            {/* お名前（任意） */}
            <Box sx={{ mb: { xs: 2.5, sm: 3.5 } }}>
              <Typography
                component="label"
                sx={{
                  display: 'block',
                  fontSize: { xs: '14px', sm: '16px' },
                  fontWeight: 600,
                  color: '#333',
                  mb: { xs: 1, sm: 1.5 },
                }}
              >
                お名前（任意）
              </Typography>
              <TextField
                type="text"
                fullWidth
                placeholder="白石"
                value={name}
                onChange={(e) => setName(e.target.value)}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    fontSize: { xs: '16px', sm: '18px' },
                    borderRadius: { xs: '8px', sm: '12px' },
                    '& fieldset': {
                      borderWidth: '2px',
                      borderColor: '#e0e0e0',
                    },
                    '&:hover fieldset': {
                      borderColor: '#e0e0e0',
                    },
                    '&.Mui-focused fieldset': {
                      borderColor: '#D4AF37',
                      boxShadow: '0 0 0 3px rgba(212, 175, 55, 0.1)',
                    },
                  },
                  '& .MuiOutlinedInput-input': {
                    padding: { xs: '14px 16px', sm: '16px 20px' },
                  },
                }}
              />
              <Typography
                sx={{
                  fontSize: { xs: '12px', sm: '14px' },
                  color: '#999',
                  mt: 0.5,
                }}
              >
                アプリ内での表示名として使用されます
              </Typography>
            </Box>

            {/* 利用規約 */}
            <FormControlLabel
              control={
                <Checkbox
                  checked={agreedToTerms}
                  onChange={(e) => setAgreedToTerms(e.target.checked)}
                  sx={{
                    width: { xs: '20px', sm: '24px' },
                    height: { xs: '20px', sm: '24px' },
                    marginTop: 0.25,
                    color: '#e0e0e0',
                    '&.Mui-checked': {
                      color: '#D4AF37',
                    },
                  }}
                />
              }
              label={
                <Typography
                  sx={{
                    fontSize: { xs: '14px', sm: '16px' },
                    color: '#666',
                    lineHeight: 1.5,
                    cursor: 'pointer',
                  }}
                >
                  <Box
                    component="a"
                    href="#"
                    onClick={(e) => {
                      e.preventDefault();
                      alert('利用規約を表示します');
                    }}
                    sx={{
                      color: '#D4AF37',
                      textDecoration: 'none',
                      fontWeight: 600,
                      fontSize: { xs: '14px', md: '15px' },
                      minHeight: '44px',
                      display: 'inline-flex',
                      alignItems: 'center',
                      '&:hover': {
                        textDecoration: 'underline',
                      },
                    }}
                  >
                    利用規約
                  </Box>
                  と
                  <Box
                    component="a"
                    href="#"
                    onClick={(e) => {
                      e.preventDefault();
                      alert('プライバシーポリシーを表示します');
                    }}
                    sx={{
                      color: '#D4AF37',
                      textDecoration: 'none',
                      fontWeight: 600,
                      fontSize: { xs: '14px', md: '15px' },
                      minHeight: '44px',
                      display: 'inline-flex',
                      alignItems: 'center',
                      '&:hover': {
                        textDecoration: 'underline',
                      },
                    }}
                  >
                    プライバシーポリシー
                  </Box>
                  に同意する
                </Typography>
              }
              sx={{
                display: 'flex',
                alignItems: 'flex-start',
                gap: 1,
                mb: { xs: 2, sm: 3 },
              }}
            />

            {/* 新規登録ボタン */}
            <Button
              fullWidth
              variant="contained"
              disabled={!isFormValid() || loading}
              onClick={handleRegister}
              sx={{
                padding: { xs: '14px', sm: '16px' },
                fontSize: { xs: '16px', sm: '18px' },
                fontWeight: 700,
                borderRadius: { xs: '12px', sm: '16px' },
                background: '#D4AF37',
                color: 'white',
                boxShadow: '0 4px 12px rgba(212, 175, 55, 0.3)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: 1,
                textTransform: 'none',
                '&:hover': {
                  background: '#B8941C',
                  transform: 'translateY(-2px)',
                  boxShadow: '0 6px 16px rgba(212, 175, 55, 0.4)',
                },
                '&:active': {
                  transform: 'translateY(0)',
                },
                '&.Mui-disabled': {
                  background: '#e0e0e0',
                  color: '#999',
                  boxShadow: 'none',
                },
              }}
            >
              <Box
                component="svg"
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="currentColor"
              >
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" />
              </Box>
              {loading ? '登録中...' : 'アカウントを作成'}
            </Button>
          </Box>

          {/* ディバイダー */}
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

          {/* ゲストモード説明 */}
          <Box
            sx={{
              background: '#f5f5f5',
              borderRadius: '12px',
              padding: '16px',
              textAlign: 'center',
            }}
          >
            <Typography sx={{ fontSize: '14px', color: '#666', mb: 1 }}>
              登録せずにお試しいただけます
            </Typography>
            <Typography sx={{ fontSize: '12px', color: '#999' }}>
              ※データはこの端末のみに保存されます
            </Typography>
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
            すでにアカウントをお持ちの場合{' '}
            <Box
              component="a"
              href="#"
              onClick={(e) => {
                e.preventDefault();
                navigate('/login');
              }}
              sx={{
                color: '#D4AF37',
                textDecoration: 'none',
                fontWeight: 600,
                cursor: 'pointer',
                '&:hover': {
                  textDecoration: 'underline',
                },
              }}
            >
              ログイン
            </Box>
          </Typography>
        </Box>
      </Box>
    </Box>
  );
};

export default RegisterPage;
