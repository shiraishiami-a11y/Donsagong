import { useState } from 'react';
import {
  Box,
  Typography,
  TextField,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Alert
} from '@mui/material';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import LogoutIcon from '@mui/icons-material/Logout';
import { changePassword, logout } from '../../../services/api/settingsService';
import { useNavigate } from 'react-router-dom';

interface AccountSectionProps {
  userEmail: string;
}

export const AccountSection: React.FC<AccountSectionProps> = ({ userEmail }) => {
  const navigate = useNavigate();
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [logoutDialogOpen, setLogoutDialogOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  const handlePasswordChange = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    // バリデーション
    if (!oldPassword || !newPassword || !confirmPassword) {
      setError('すべての項目を入力してください');
      return;
    }

    if (newPassword !== confirmPassword) {
      setError('新しいパスワードと確認パスワードが一致しません');
      return;
    }

    if (newPassword.length < 8) {
      setError('パスワードは8文字以上である必要があります');
      return;
    }

    try {
      setLoading(true);
      const response = await changePassword(oldPassword, newPassword);

      if (response.success) {
        setSuccess(response.message);
        setOldPassword('');
        setNewPassword('');
        setConfirmPassword('');
      } else {
        setError(response.message);
      }
    } catch (err) {
      setError('パスワード変更に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    try {
      logout();
      navigate('/list');
    } catch (err) {
      setError('ログアウトに失敗しました');
    }
  };

  return (
    <Box
      sx={{
        background: 'white',
        borderRadius: 3,
        boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)',
        mb: 2.5,
        overflow: 'hidden'
      }}
    >
      {/* セクションヘッダー */}
      <Box
        sx={{
          p: 2,
          background: theme => theme.palette.gold.LIGHT_GOLD,
          borderBottom: '1px solid',
          borderColor: 'divider'
        }}
      >
        <Typography
          variant="h6"
          sx={{
            fontSize: '16px',
            fontWeight: 500,
            color: theme => theme.palette.gold.DARK_GOLD,
            display: 'flex',
            alignItems: 'center',
            gap: 1
          }}
        >
          <AccountCircleIcon />
          アカウント設定
        </Typography>
      </Box>

      {/* セクションコンテンツ */}
      <Box sx={{ p: 2 }}>
        {/* メールアドレス表示 */}
        <Box sx={{ pb: 2, borderBottom: '1px solid', borderColor: 'divider' }}>
          <Typography variant="body2" fontWeight={500} mb={1}>
            メールアドレス
          </Typography>
          <TextField
            fullWidth
            value={userEmail}
            disabled
            size="small"
            sx={{
              '& .MuiInputBase-input.Mui-disabled': {
                WebkitTextFillColor: theme => theme.palette.text.secondary,
                background: theme => theme.palette.grey[100]
              }
            }}
          />
        </Box>

        {/* パスワード変更フォーム */}
        <Box sx={{ py: 2, borderBottom: '1px solid', borderColor: 'divider' }}>
          <Typography variant="body2" fontWeight={500} mb={2}>
            パスワード変更
          </Typography>

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          {success && (
            <Alert severity="success" sx={{ mb: 2 }}>
              {success}
            </Alert>
          )}

          <Box component="form" onSubmit={handlePasswordChange}>
            <TextField
              fullWidth
              type="password"
              label="現在のパスワード"
              value={oldPassword}
              onChange={(e) => setOldPassword(e.target.value)}
              size="small"
              sx={{ mb: 2 }}
              disabled={loading}
            />
            <TextField
              fullWidth
              type="password"
              label="新しいパスワード"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              size="small"
              sx={{ mb: 2 }}
              disabled={loading}
            />
            <TextField
              fullWidth
              type="password"
              label="パスワード確認"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              size="small"
              sx={{ mb: 2 }}
              disabled={loading}
            />
            <Button
              type="submit"
              variant="contained"
              fullWidth
              disabled={loading}
              sx={{
                background: theme => theme.palette.gold.PRIMARY_GOLD,
                '&:hover': {
                  background: theme => theme.palette.gold.DARK_GOLD
                }
              }}
            >
              変更
            </Button>
          </Box>
        </Box>

        {/* ログアウトボタン */}
        <Box sx={{ pt: 2 }}>
          <Button
            fullWidth
            variant="contained"
            color="error"
            startIcon={<LogoutIcon />}
            onClick={() => setLogoutDialogOpen(true)}
            sx={{ py: 1.5 }}
          >
            ログアウト
          </Button>
        </Box>
      </Box>

      {/* ログアウト確認ダイアログ */}
      <Dialog open={logoutDialogOpen} onClose={() => setLogoutDialogOpen(false)}>
        <DialogTitle>ログアウトしますか?</DialogTitle>
        <DialogContent>
          <DialogContentText>
            ログアウトすると、ゲストモードに移行します。再度ログインすれば、クラウドのデータにアクセスできます。
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setLogoutDialogOpen(false)}>キャンセル</Button>
          <Button onClick={handleLogout} color="error" autoFocus>
            ログアウト
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};
