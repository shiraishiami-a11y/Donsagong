import { useState } from 'react';
import { Box, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import DownloadIcon from '@mui/icons-material/Download';
import UploadIcon from '@mui/icons-material/Upload';
import LogoutIcon from '@mui/icons-material/Logout';

// カスタムスイッチコンポーネント
const CustomSwitch: React.FC<{ checked: boolean; onChange: () => void }> = ({ checked, onChange }) => {
  return (
    <Box
      onClick={onChange}
      sx={{
        position: 'relative',
        width: { xs: '48px', md: '56px' },
        height: { xs: '28px', md: '32px' },
        background: checked ? '#D4AF37' : '#e0e0e0',
        borderRadius: { xs: '14px', md: '16px' },
        cursor: 'pointer',
        transition: 'all 0.3s'
      }}
    >
      <Box
        sx={{
          position: 'absolute',
          top: '2px',
          left: '2px',
          width: { xs: '24px', md: '28px' },
          height: { xs: '24px', md: '28px' },
          background: 'white',
          borderRadius: '50%',
          transition: 'all 0.3s',
          transform: checked ? { xs: 'translateX(20px)', md: 'translateX(24px)' } : 'translateX(0)',
          boxShadow: '0 2px 4px rgba(0,0,0,0.2)'
        }}
      />
    </Box>
  );
};

const SettingsPage: React.FC = () => {
  const navigate = useNavigate();

  // 仮実装：将来は認証状態から取得
  const [isLoggedIn] = useState(true);
  const userName = '白石';
  const userEmail = 'test@goldensaju.local';

  // 通知設定
  const [pushNotification, setPushNotification] = useState(true);
  const [emailNotification, setEmailNotification] = useState(false);
  const [fortuneReminder, setFortuneReminder] = useState(true);

  // 表示設定
  const [darkMode, setDarkMode] = useState(false);
  const [graphAnimation, setGraphAnimation] = useState(true);

  const handleExport = () => {
    alert('データをエクスポートします');
  };

  const handleImport = () => {
    alert('データをインポートします');
  };

  const handleLogout = () => {
    if (confirm('ログアウトしますか？')) {
      alert('ログアウトしました');
      navigate('/login');
    }
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: '#f5f5f5'
      }}
    >
      {/* ヘッダー */}
      <Box
        sx={{
          background: 'white',
          padding: { xs: '20px', md: '24px 40px' },
          borderBottom: '2px solid #D4AF37',
          borderRadius: { xs: '0', md: '0 0 16px 16px' },
          position: 'sticky',
          top: 0,
          zIndex: 100
        }}
      >
        <Typography
          sx={{
            fontSize: { xs: '20px', md: '28px' },
            fontWeight: 700,
            color: '#1a1a2e'
          }}
        >
          ⚙️ 設定
        </Typography>
        <Typography
          sx={{
            fontSize: { xs: '12px', md: '14px' },
            color: '#666',
            marginTop: '4px'
          }}
        >
          アカウント管理と各種設定
        </Typography>
      </Box>

      {/* メインコンテンツ */}
      <Box
        sx={{
          width: '100%',
          maxWidth: { xs: '100%', md: '600px', lg: '800px' },
          margin: '0 auto',
          padding: { xs: '20px', md: '30px 24px 80px', lg: '30px 40px 80px' }
        }}
      >
        {/* ユーザー情報カード */}
        {isLoggedIn && (
          <Box
            sx={{
              background: 'linear-gradient(135deg, #D4AF37, #B8941C)',
              borderRadius: { xs: '16px', md: '20px' },
              padding: { xs: '24px', md: '32px' },
              color: 'white',
              marginBottom: { xs: '20px', md: '30px' }
            }}
          >
            <Box
              sx={{
                width: { xs: '60px', md: '80px' },
                height: { xs: '60px', md: '80px' },
                borderRadius: '50%',
                background: 'white',
                color: '#D4AF37',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: { xs: '28px', md: '36px' },
                fontWeight: 700,
                marginBottom: { xs: '12px', md: '16px' }
              }}
            >
              {userName.charAt(0)}
            </Box>
            <Typography
              sx={{
                fontSize: { xs: '20px', md: '24px' },
                fontWeight: 700,
                marginBottom: '4px'
              }}
            >
              {userName}
            </Typography>
            <Typography
              sx={{
                fontSize: { xs: '14px', md: '16px' },
                opacity: 0.9
              }}
            >
              {userEmail}
            </Typography>
          </Box>
        )}

        {/* アカウント設定 */}
        {isLoggedIn && (
          <Box
            sx={{
              background: 'white',
              borderRadius: { xs: '16px', md: '20px' },
              padding: { xs: '20px', md: '30px' },
              marginBottom: { xs: '16px', md: '24px' },
              boxShadow: '0 2px 8px rgba(0,0,0,0.06)'
            }}
          >
            <Typography
              sx={{
                fontSize: { xs: '16px', md: '20px' },
                fontWeight: 700,
                color: '#1a1a2e',
                marginBottom: { xs: '16px', md: '24px' },
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}
            >
              <span>👤</span>
              アカウント設定
            </Typography>
            <Box
              sx={{
                borderBottom: '1px solid #f0f0f0',
                padding: { xs: '16px 0', md: '20px 0' },
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}
            >
              <Typography sx={{ fontSize: { xs: '14px', md: '16px' }, color: '#333', fontWeight: 500 }}>
                メールアドレス
              </Typography>
              <Typography sx={{ fontSize: { xs: '14px', md: '16px' }, color: '#666' }}>
                {userEmail}
              </Typography>
            </Box>
            <Box
              sx={{
                borderBottom: '1px solid #f0f0f0',
                padding: { xs: '16px 0', md: '20px 0' },
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                cursor: 'pointer'
              }}
            >
              <Typography sx={{ fontSize: { xs: '14px', md: '16px' }, color: '#333', fontWeight: 500 }}>
                パスワード変更
              </Typography>
              <ChevronRightIcon sx={{ color: '#D4AF37' }} />
            </Box>
            <Box
              sx={{
                padding: { xs: '16px 0', md: '20px 0' },
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                cursor: 'pointer'
              }}
            >
              <Typography sx={{ fontSize: { xs: '14px', md: '16px' }, color: '#333', fontWeight: 500 }}>
                アカウント削除
              </Typography>
              <ChevronRightIcon sx={{ color: '#f44336' }} />
            </Box>
          </Box>
        )}

        {/* 通知設定 */}
        <Box
          sx={{
            background: 'white',
            borderRadius: { xs: '16px', md: '20px' },
            padding: { xs: '20px', md: '30px' },
            marginBottom: { xs: '16px', md: '24px' },
            boxShadow: '0 2px 8px rgba(0,0,0,0.06)'
          }}
        >
          <Typography
            sx={{
              fontSize: { xs: '16px', md: '20px' },
              fontWeight: 700,
              color: '#1a1a2e',
              marginBottom: { xs: '16px', md: '24px' },
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}
          >
            <span>🔔</span>
            通知設定
          </Typography>
          <Box
            sx={{
              borderBottom: '1px solid #f0f0f0',
              padding: { xs: '16px 0', md: '20px 0' },
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}
          >
            <Typography sx={{ fontSize: { xs: '14px', md: '16px' }, color: '#333', fontWeight: 500 }}>
              プッシュ通知
            </Typography>
            <CustomSwitch checked={pushNotification} onChange={() => setPushNotification(!pushNotification)} />
          </Box>
          <Box
            sx={{
              borderBottom: '1px solid #f0f0f0',
              padding: { xs: '16px 0', md: '20px 0' },
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}
          >
            <Typography sx={{ fontSize: { xs: '14px', md: '16px' }, color: '#333', fontWeight: 500 }}>
              メール通知
            </Typography>
            <CustomSwitch checked={emailNotification} onChange={() => setEmailNotification(!emailNotification)} />
          </Box>
          <Box
            sx={{
              padding: { xs: '16px 0', md: '20px 0' },
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}
          >
            <Typography sx={{ fontSize: { xs: '14px', md: '16px' }, color: '#333', fontWeight: 500 }}>
              運勢リマインダー
            </Typography>
            <CustomSwitch checked={fortuneReminder} onChange={() => setFortuneReminder(!fortuneReminder)} />
          </Box>
        </Box>

        {/* 表示設定 */}
        <Box
          sx={{
            background: 'white',
            borderRadius: { xs: '16px', md: '20px' },
            padding: { xs: '20px', md: '30px' },
            marginBottom: { xs: '16px', md: '24px' },
            boxShadow: '0 2px 8px rgba(0,0,0,0.06)'
          }}
        >
          <Typography
            sx={{
              fontSize: { xs: '16px', md: '20px' },
              fontWeight: 700,
              color: '#1a1a2e',
              marginBottom: { xs: '16px', md: '24px' },
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}
          >
            <span>🎨</span>
            表示設定
          </Typography>
          <Box
            sx={{
              borderBottom: '1px solid #f0f0f0',
              padding: { xs: '16px 0', md: '20px 0' },
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}
          >
            <Typography sx={{ fontSize: { xs: '14px', md: '16px' }, color: '#333', fontWeight: 500 }}>
              ダークモード
            </Typography>
            <CustomSwitch checked={darkMode} onChange={() => setDarkMode(!darkMode)} />
          </Box>
          <Box
            sx={{
              padding: { xs: '16px 0', md: '20px 0' },
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}
          >
            <Typography sx={{ fontSize: { xs: '14px', md: '16px' }, color: '#333', fontWeight: 500 }}>
              グラフアニメーション
            </Typography>
            <CustomSwitch checked={graphAnimation} onChange={() => setGraphAnimation(!graphAnimation)} />
          </Box>
        </Box>

        {/* データ管理 */}
        <Box
          sx={{
            background: 'white',
            borderRadius: { xs: '16px', md: '20px' },
            padding: { xs: '20px', md: '30px' },
            marginBottom: { xs: '16px', md: '24px' },
            boxShadow: '0 2px 8px rgba(0,0,0,0.06)'
          }}
        >
          <Typography
            sx={{
              fontSize: { xs: '16px', md: '20px' },
              fontWeight: 700,
              color: '#1a1a2e',
              marginBottom: { xs: '16px', md: '24px' },
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}
          >
            <span>💾</span>
            データ管理
          </Typography>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: { xs: '12px', md: '16px' }, marginTop: { xs: '20px', md: '30px' } }}>
            <Box
              onClick={handleExport}
              sx={{
                width: '100%',
                padding: { xs: '14px', md: '16px' },
                border: '2px solid #e0e0e0',
                borderRadius: { xs: '12px', md: '16px' },
                fontSize: { xs: '16px', md: '18px' },
                fontWeight: 600,
                cursor: 'pointer',
                transition: 'all 0.2s',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
                background: 'white',
                color: '#666',
                '&:hover': {
                  borderColor: '#D4AF37',
                  color: '#D4AF37'
                }
              }}
            >
              <DownloadIcon />
              データをエクスポート
            </Box>
            <Box
              onClick={handleImport}
              sx={{
                width: '100%',
                padding: { xs: '14px', md: '16px' },
                border: '2px solid #e0e0e0',
                borderRadius: { xs: '12px', md: '16px' },
                fontSize: { xs: '16px', md: '18px' },
                fontWeight: 600,
                cursor: 'pointer',
                transition: 'all 0.2s',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
                background: 'white',
                color: '#666',
                '&:hover': {
                  borderColor: '#D4AF37',
                  color: '#D4AF37'
                }
              }}
            >
              <UploadIcon />
              データをインポート
            </Box>
          </Box>
        </Box>

        {/* その他 */}
        <Box
          sx={{
            background: 'white',
            borderRadius: { xs: '16px', md: '20px' },
            padding: { xs: '20px', md: '30px' },
            marginBottom: { xs: '16px', md: '24px' },
            boxShadow: '0 2px 8px rgba(0,0,0,0.06)'
          }}
        >
          <Typography
            sx={{
              fontSize: { xs: '16px', md: '20px' },
              fontWeight: 700,
              color: '#1a1a2e',
              marginBottom: { xs: '16px', md: '24px' },
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}
          >
            <span>📄</span>
            その他
          </Typography>
          <Box
            sx={{
              borderBottom: '1px solid #f0f0f0',
              padding: { xs: '16px 0', md: '20px 0' },
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              cursor: 'pointer'
            }}
          >
            <Typography sx={{ fontSize: { xs: '14px', md: '16px' }, color: '#333', fontWeight: 500 }}>
              利用規約
            </Typography>
            <ChevronRightIcon sx={{ color: '#D4AF37' }} />
          </Box>
          <Box
            sx={{
              borderBottom: '1px solid #f0f0f0',
              padding: { xs: '16px 0', md: '20px 0' },
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              cursor: 'pointer'
            }}
          >
            <Typography sx={{ fontSize: { xs: '14px', md: '16px' }, color: '#333', fontWeight: 500 }}>
              プライバシーポリシー
            </Typography>
            <ChevronRightIcon sx={{ color: '#D4AF37' }} />
          </Box>
          <Box
            sx={{
              padding: { xs: '16px 0', md: '20px 0' },
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}
          >
            <Typography sx={{ fontSize: { xs: '14px', md: '16px' }, color: '#333', fontWeight: 500 }}>
              アプリバージョン
            </Typography>
            <Typography sx={{ fontSize: { xs: '14px', md: '16px' }, color: '#666' }}>
              v1.0.0
            </Typography>
          </Box>
        </Box>

        {/* ログアウト */}
        {isLoggedIn && (
          <Box
            sx={{
              background: 'white',
              borderRadius: { xs: '16px', md: '20px' },
              padding: { xs: '20px', md: '30px' },
              boxShadow: '0 2px 8px rgba(0,0,0,0.06)'
            }}
          >
            <Box
              onClick={handleLogout}
              sx={{
                width: '100%',
                padding: { xs: '14px', md: '16px' },
                border: '2px solid #f44336',
                borderRadius: { xs: '12px', md: '16px' },
                fontSize: { xs: '16px', md: '18px' },
                fontWeight: 600,
                cursor: 'pointer',
                transition: 'all 0.2s',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
                background: '#fff',
                color: '#f44336',
                '&:hover': {
                  background: '#f44336',
                  color: 'white'
                }
              }}
            >
              <LogoutIcon />
              ログアウト
            </Box>
          </Box>
        )}
      </Box>

      {/* ボトムナビ */}
      <Box
        sx={{
          position: 'fixed',
          bottom: 0,
          left: { xs: 0, md: '50%' },
          right: { xs: 0, md: 'auto' },
          transform: { xs: 'none', md: 'translateX(-50%)' },
          display: 'flex',
          justifyContent: 'space-around',
          background: 'white',
          padding: { xs: '12px', md: '16px' },
          boxShadow: '0 -2px 10px rgba(0,0,0,0.05)',
          maxWidth: { xs: '100%', md: '600px', lg: '800px' },
          width: '100%',
          borderRadius: { xs: '0', md: '24px 24px 0 0' }
        }}
      >
        <Box
          onClick={() => navigate('/')}
          sx={{
            flex: 1,
            textAlign: 'center',
            padding: { xs: '8px', md: '12px' },
            color: '#999',
            cursor: 'pointer',
            transition: 'all 0.2s',
            borderRadius: '12px',
            fontSize: { xs: '12px', md: '14px' },
            '&:hover': {
              color: '#D4AF37'
            }
          }}
        >
          <Box sx={{ fontSize: { xs: '24px', md: '28px' }, marginBottom: '4px' }}>✨</Box>
          <Box>命式記入</Box>
        </Box>
        <Box
          onClick={() => navigate('/list')}
          sx={{
            flex: 1,
            textAlign: 'center',
            padding: { xs: '8px', md: '12px' },
            color: '#999',
            cursor: 'pointer',
            transition: 'all 0.2s',
            borderRadius: '12px',
            fontSize: { xs: '12px', md: '14px' },
            '&:hover': {
              color: '#D4AF37'
            }
          }}
        >
          <Box sx={{ fontSize: { xs: '24px', md: '28px' }, marginBottom: '4px' }}>📋</Box>
          <Box>命式一覧</Box>
        </Box>
        <Box
          sx={{
            flex: 1,
            textAlign: 'center',
            padding: { xs: '8px', md: '12px' },
            color: '#D4AF37',
            background: '#fffbf0',
            cursor: 'pointer',
            transition: 'all 0.2s',
            borderRadius: '12px',
            fontSize: { xs: '12px', md: '14px' }
          }}
        >
          <Box sx={{ fontSize: { xs: '24px', md: '28px' }, marginBottom: '4px' }}>⚙️</Box>
          <Box>設定</Box>
        </Box>
      </Box>
    </Box>
  );
};

export default SettingsPage;
