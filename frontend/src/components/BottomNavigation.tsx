// BottomNavigation - 全ページ共通ボトムナビゲーションバー
import { BottomNavigation as MuiBottomNavigation, BottomNavigationAction, Paper } from '@mui/material';
import { AutoAwesome, ViewList, Settings } from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

export const BottomNavigation: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  // 現在のパスに基づいて選択状態を決定
  const getValue = () => {
    const path = location.pathname;
    if (path === '/' || path.startsWith('/calculate')) {
      return 0; // 命式記入
    } else if (path.startsWith('/list') || path.startsWith('/detail')) {
      return 1; // 命式一覧
    } else if (path.startsWith('/settings')) {
      return 2; // 設定
    }
    return 0;
  };

  const handleChange = (_event: React.SyntheticEvent, newValue: number) => {
    switch (newValue) {
      case 0:
        navigate('/');
        break;
      case 1:
        navigate('/list');
        break;
      case 2:
        navigate('/settings');
        break;
    }
  };

  return (
    <Paper
      sx={{
        position: 'fixed',
        bottom: 0,
        left: 0,
        right: 0,
        zIndex: 1000,
        borderTop: '1px solid #e0e0e0',
      }}
      elevation={3}
    >
      <MuiBottomNavigation
        value={getValue()}
        onChange={handleChange}
        showLabels
        sx={{
          height: { xs: '70px', md: '80px' },
          '& .MuiBottomNavigationAction-root': {
            minWidth: 'auto',
            padding: { xs: '8px 12px', md: '12px 16px' },
            color: '#999',
            '&.Mui-selected': {
              color: '#D4AF37',
            },
          },
          '& .MuiBottomNavigationAction-label': {
            fontSize: { xs: '12px', md: '14px' },
            fontWeight: 600,
            marginTop: '4px',
            '&.Mui-selected': {
              fontSize: { xs: '12px', md: '14px' },
            },
          },
        }}
      >
        <BottomNavigationAction
          label="命式記入"
          icon={<AutoAwesome sx={{ fontSize: { xs: '24px', md: '28px' } }} />}
          data-testid="bottom-nav-input"
        />
        <BottomNavigationAction
          label="命式一覧"
          icon={<ViewList sx={{ fontSize: { xs: '24px', md: '28px' } }} />}
          data-testid="bottom-nav-list"
        />
        <BottomNavigationAction
          label="設定"
          icon={<Settings sx={{ fontSize: { xs: '24px', md: '28px' } }} />}
          data-testid="bottom-nav-settings"
        />
      </MuiBottomNavigation>
    </Paper>
  );
};

export default BottomNavigation;
