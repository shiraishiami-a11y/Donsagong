// MainLayout - 認証後ページ用レイアウト（Dashboard, List, Detail, Settings等）
import { Box, Drawer, Toolbar } from '@mui/material';
import { useState } from 'react';
import type { LayoutProps } from '../types';

const DRAWER_WIDTH = 240;

interface MainLayoutProps extends LayoutProps {
  header?: React.ReactNode;
  sidebar?: React.ReactNode;
}

export const MainLayout: React.FC<MainLayoutProps> = ({ children, header, sidebar }) => {
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      {/* ヘッダー（propsで注入） */}
      {header}

      {/* サイドバー（レスポンシブDrawer） */}
      {sidebar && (
        <Box
          component="nav"
          sx={{ width: { sm: DRAWER_WIDTH }, flexShrink: { sm: 0 } }}
        >
          {/* モバイル用Drawer */}
          <Drawer
            variant="temporary"
            open={mobileOpen}
            onClose={handleDrawerToggle}
            ModalProps={{ keepMounted: true }}
            sx={{
              display: { xs: 'block', sm: 'none' },
              '& .MuiDrawer-paper': { width: DRAWER_WIDTH },
            }}
          >
            {sidebar}
          </Drawer>

          {/* デスクトップ用Drawer */}
          <Drawer
            variant="permanent"
            sx={{
              display: { xs: 'none', sm: 'block' },
              '& .MuiDrawer-paper': { width: DRAWER_WIDTH },
            }}
            open
          >
            {sidebar}
          </Drawer>
        </Box>
      )}

      {/* メインコンテンツ */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${DRAWER_WIDTH}px)` },
          backgroundColor: '#fafafa',
        }}
      >
        <Toolbar />
        {children}
      </Box>
    </Box>
  );
};

export default MainLayout;
