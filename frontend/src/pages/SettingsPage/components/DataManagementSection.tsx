import { useState, useRef } from 'react';
import { Box, Typography, Button, Alert } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import CloudDoneIcon from '@mui/icons-material/CloudDone';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import { exportData, importData } from '../../../services/api/settingsService';
import { useNavigate } from 'react-router-dom';

interface DataManagementSectionProps {
  isLoggedIn: boolean;
}

export const DataManagementSection: React.FC<DataManagementSectionProps> = ({ isLoggedIn }) => {
  const navigate = useNavigate();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleExport = async () => {
    try {
      setError('');
      setMessage('');

      const blob = await exportData();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `saju_export_${new Date().toISOString().split('T')[0]}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      setMessage('データをエクスポートしました');
    } catch (err) {
      setError('エクスポートに失敗しました');
    }
  };

  const handleImportClick = () => {
    fileInputRef.current?.click();
  };

  const handleImport = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      setError('');
      setMessage('');

      const response = await importData(file);

      if (response.success) {
        setMessage(response.message);
      } else {
        setError(response.message);
      }
    } catch (err) {
      setError('インポートに失敗しました');
    }

    // ファイル選択をリセット
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
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
          {isLoggedIn ? <CloudUploadIcon /> : <CloudDoneIcon />}
          データ管理
        </Typography>
      </Box>

      {/* セクションコンテンツ */}
      <Box sx={{ p: 2 }}>
        {message && (
          <Alert severity="success" sx={{ mb: 2 }}>
            {message}
          </Alert>
        )}

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {isLoggedIn ? (
          // ログインモード: エクスポート/インポート
          <Box>
            <Button
              fullWidth
              variant="outlined"
              startIcon={<FileDownloadIcon />}
              onClick={handleExport}
              sx={{ mb: 1.5 }}
            >
              データをエクスポート
            </Button>
            <Button
              fullWidth
              variant="outlined"
              startIcon={<FileUploadIcon />}
              onClick={handleImportClick}
            >
              データをインポート
            </Button>
            <input
              ref={fileInputRef}
              type="file"
              accept=".json"
              onChange={handleImport}
              style={{ display: 'none' }}
            />
          </Box>
        ) : (
          // ゲストモード: 登録案内バナー
          <Box
            sx={{
              background: theme => `linear-gradient(135deg, ${theme.palette.gold.PRIMARY_GOLD} 0%, ${theme.palette.gold.DARK_GOLD} 100%)`,
              color: 'white',
              p: 2.5,
              borderRadius: 2,
              textAlign: 'center'
            }}
          >
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', mb: 1 }}>
              <CloudDoneIcon sx={{ fontSize: 24 }} />
              <Typography variant="h6" sx={{ ml: 1, fontSize: '18px', fontWeight: 500 }}>
                クラウドに保存しませんか?
              </Typography>
            </Box>
            <Typography variant="body2" sx={{ mb: 2, opacity: 0.9 }}>
              アカウントを作成すると、複数の端末でデータを同期できます。
              <br />
              大切な命式データを安全にバックアップ!
            </Typography>
            <Button
              variant="contained"
              onClick={() => navigate('/register')}
              sx={{
                background: 'white',
                color: theme => theme.palette.gold.PRIMARY_GOLD,
                '&:hover': {
                  background: 'rgba(255, 255, 255, 0.9)'
                },
                boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)'
              }}
            >
              アカウントを作成
            </Button>
          </Box>
        )}
      </Box>
    </Box>
  );
};
