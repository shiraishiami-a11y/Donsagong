// Sidebar - サイドバーナビゲーション
import {
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Divider,
  Toolbar,
  Box,
} from '@mui/material';
import {
  Home,
  List as ListIcon,
  Settings,
  AdminPanelSettings,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../features/auth/hooks/useAuth';

interface MenuItem {
  text: string;
  icon: React.ReactNode;
  path: string;
  roles: Array<'guest' | 'user' | 'admin'>;
}

const userMenuItems: MenuItem[] = [
  {
    text: '命式記入',
    icon: <Home />,
    path: '/',
    roles: ['user', 'admin'],
  },
  {
    text: '命式リスト',
    icon: <ListIcon />,
    path: '/list',
    roles: ['user', 'admin'],
  },
  {
    text: '設定',
    icon: <Settings />,
    path: '/settings',
    roles: ['user', 'admin'],
  },
];

const adminMenuItems: MenuItem[] = [
  {
    text: '管理画面',
    icon: <AdminPanelSettings />,
    path: '/admin',
    roles: ['admin'],
  },
];

export const Sidebar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user } = useAuth();

  const hasAccess = (roles: Array<'guest' | 'user' | 'admin'>) => {
    return roles.includes(user?.role || 'guest');
  };

  return (
    <Box
      sx={{
        height: '100%',
        backgroundColor: 'white',
        borderRight: 1,
        borderColor: 'divider',
      }}
    >
      <Toolbar />
      <List>
        {userMenuItems
          .filter((item) => hasAccess(item.roles))
          .map((item) => (
            <ListItem key={item.path} disablePadding>
              <ListItemButton
                selected={location.pathname === item.path}
                onClick={() => navigate(item.path)}
                sx={{
                  '&.Mui-selected': {
                    backgroundColor: 'rgba(212, 175, 55, 0.1)',
                    borderRight: 3,
                    borderColor: 'gold.PRIMARY_GOLD',
                    '&:hover': {
                      backgroundColor: 'rgba(212, 175, 55, 0.15)',
                    },
                  },
                }}
              >
                <ListItemIcon
                  sx={{
                    color:
                      location.pathname === item.path
                        ? 'gold.PRIMARY_GOLD'
                        : 'text.secondary',
                  }}
                >
                  {item.icon}
                </ListItemIcon>
                <ListItemText
                  primary={item.text}
                  sx={{
                    color:
                      location.pathname === item.path
                        ? 'gold.PRIMARY_GOLD'
                        : 'text.primary',
                  }}
                />
              </ListItemButton>
            </ListItem>
          ))}
      </List>

      {/* 管理者メニュー */}
      {user?.role === 'admin' && (
        <>
          <Divider />
          <List>
            {adminMenuItems.map((item) => (
              <ListItem key={item.path} disablePadding>
                <ListItemButton
                  selected={location.pathname === item.path}
                  onClick={() => navigate(item.path)}
                  sx={{
                    '&.Mui-selected': {
                      backgroundColor: 'rgba(212, 175, 55, 0.1)',
                      borderRight: 3,
                      borderColor: 'gold.PRIMARY_GOLD',
                    },
                  }}
                >
                  <ListItemIcon
                    sx={{
                      color:
                        location.pathname === item.path
                          ? 'gold.PRIMARY_GOLD'
                          : 'text.secondary',
                    }}
                  >
                    {item.icon}
                  </ListItemIcon>
                  <ListItemText
                    primary={item.text}
                    sx={{
                      color:
                        location.pathname === item.path
                          ? 'gold.PRIMARY_GOLD'
                          : 'text.primary',
                    }}
                  />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        </>
      )}
    </Box>
  );
};

export default Sidebar;
