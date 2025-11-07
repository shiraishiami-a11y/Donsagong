// ListPage - 命式リストページ（簡易版・検索フィルタなし）
import { useState, useEffect, useMemo } from 'react';
import { Box, Typography, Button, Alert, IconButton, Dialog, DialogTitle, DialogContent, DialogContentText, DialogActions } from '@mui/material';
import { AddCircle, CloudUpload, ChevronRight, ArrowBack, Settings as SettingsIcon, Inbox } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../features/auth/hooks/useAuth';
import { BottomNavigation } from '../../components/BottomNavigation';
import { SajuCard } from './components/SajuCard';
import { getSajuList, deleteSaju } from '../../services/api/sajuListService';
import type { SajuSummary } from '../../types';

export const ListPage: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const isGuestMode = user?.role === 'guest';

  // 状態管理
  const [sajuList, setSajuList] = useState<SajuSummary[]>([]);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [targetDeleteId, setTargetDeleteId] = useState<string | null>(null);

  // データ読み込み
  useEffect(() => {
    const loadSajuList = async () => {
      try {
        const data = await getSajuList();
        setSajuList(data);
      } catch (error) {
        console.error('命式一覧の取得に失敗しました:', error);
        // エラー時は空配列を設定
        setSajuList([]);
      }
    };

    loadSajuList();
  }, []);

  // デフォルトソート（作成日降順）
  const sortedList = useMemo(() => {
    const result = [...sajuList];
    result.sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime());
    return result;
  }, [sajuList]);

  // ハンドラー
  const handleCardClick = (id: string) => {
    navigate(`/detail/${id}`);
  };

  const handleEdit = (id: string) => {
    navigate(`/edit/${id}`);
  };

  const handleDelete = (id: string) => {
    setTargetDeleteId(id);
    setDeleteDialogOpen(true);
  };

  const handleConfirmDelete = async () => {
    if (!targetDeleteId) return;

    try {
      const response = await deleteSaju(targetDeleteId);
      console.log('[DELETE] APIレスポンス:', response);

      if (response.success) {
        // 一覧を再読み込み
        const updatedList = await getSajuList();
        console.log('[DELETE] 再読み込み後のtotal:', updatedList.length);
        setSajuList(updatedList);
      }
    } catch (error) {
      console.error('命式の削除に失敗しました:', error);
    } finally {
      setDeleteDialogOpen(false);
      setTargetDeleteId(null);
    }
  };

  const handleCancelDelete = () => {
    setDeleteDialogOpen(false);
    setTargetDeleteId(null);
  };

  const handleCreateNew = () => {
    navigate('/');
  };

  const handleRegister = () => {
    navigate('/register');
  };

  const handleSettings = () => {
    navigate('/settings');
  };

  const handleBack = () => {
    navigate('/');
  };

  return (
    <Box sx={{ width: '100%', minHeight: '100vh', backgroundColor: 'background.paper' }}>
      {/* カスタムヘッダー - レスポンシブ対応 */}
      <Box
        sx={{
          position: 'sticky',
          top: 0,
          background: 'linear-gradient(135deg, #D4AF37 0%, #B8941C 100%)',
          color: 'white',
          padding: { xs: '16px 20px', md: '20px 32px' },
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          boxShadow: '0 2px 8px rgba(212, 175, 55, 0.3)',
          zIndex: 100,
          borderRadius: { xs: 0, md: '0 0 16px 16px' },
        }}
      >
        <IconButton onClick={handleBack} sx={{ color: 'white', width: 48, height: 48 }} aria-label="トップページに戻る">
          <ArrowBack />
        </IconButton>
        <Typography
          variant="h6"
          sx={{
            fontWeight: { xs: 600, md: 700 },
            fontSize: { xs: '18px', md: '24px', lg: '28px' },
          }}
        >
          保存した命式
        </Typography>
        <IconButton onClick={handleSettings} sx={{ color: 'white', width: 48, height: 48 }} aria-label="設定">
          <SettingsIcon />
        </IconButton>
      </Box>

      {/* メインコンテンツ - レスポンシブコンテナ（モックアップ完全一致） */}
      <Box
        sx={{
          width: '100%',
          maxWidth: { xs: '100%', md: '900px', lg: '1400px' },
          margin: '0 auto', // 中央配置を確実に実装
          minHeight: '100vh',
          px: { xs: '20px', md: '24px', lg: '40px' },
          pb: { xs: '100px', md: '110px' }, // ボトムナビゲーション分の余白を追加
          pt: { xs: '20px', md: '30px' },
        }}
      >
        {/* ゲストモード専用バナー */}
        {isGuestMode && (
          <Alert
            severity="info"
            icon={<CloudUpload />}
            sx={{
              mb: 2.5,
              background: 'linear-gradient(135deg, rgba(212, 175, 55, 0.1) 0%, rgba(184, 148, 28, 0.1) 100%)',
              border: '2px solid #F4E8C1',
              borderRadius: '12px',
              cursor: 'pointer',
              transition: 'all 0.3s',
              '&:hover': {
                background: 'linear-gradient(135deg, rgba(212, 175, 55, 0.15) 0%, rgba(184, 148, 28, 0.15) 100%)',
                borderColor: '#D4AF37',
              },
            }}
            onClick={handleRegister}
            action={
              <IconButton size="small" sx={{ color: '#D4AF37' }}>
                <ChevronRight />
              </IconButton>
            }
          >
            <Typography variant="body1" sx={{ fontWeight: 500, mb: 0.5 }}>
              アカウント作成でクラウドに保存！
            </Typography>
            <Typography variant="body2" color="text.secondary">
              複数端末で同期できます
            </Typography>
          </Alert>
        )}

        {/* 新規作成ボタン - レスポンシブ対応 */}
        <Button
          fullWidth
          variant="contained"
          startIcon={<AddCircle />}
          onClick={handleCreateNew}
          sx={{
            background: '#EBCC42', // 濃い黄金色（単色）
            color: 'white', // 白文字
            py: { xs: 1.5, md: 1.75 },
            fontWeight: 700,
            fontSize: { xs: '14px', md: '16px' },
            borderRadius: { xs: '10px', md: '12px' },
            boxShadow: 'none', // 影なし
            mb: { xs: 2, md: 2.5 },
            transition: 'all 0.3s',
            '&:hover': {
              background: '#D4AF37', // ホバー時は通常の金色
              boxShadow: 'none', // ホバー時も影なし
            },
          }}
        >
          新しい命式を作成
        </Button>

        {/* 命式カード一覧 - レスポンシブグリッド（モックアップ完全一致） */}
        {sortedList.length > 0 ? (
          <Box
            data-testid="saju-list-container"
            sx={{
              display: 'grid',
              gridTemplateColumns: {
                xs: '1fr',               // スマホ: 1列
                md: 'repeat(2, 1fr)',    // タブレット: 2列
                lg: 'repeat(3, 1fr)',    // PC: 3列
              },
              gap: { xs: '16px', md: '20px', lg: '24px' },
            }}
          >
            {sortedList.map((saju) => (
              <SajuCard key={saju.id} data={saju} onEdit={handleEdit} onDelete={handleDelete} onClick={handleCardClick} />
            ))}
          </Box>
        ) : (
          // 空状態 - レスポンシブ対応
          <Box
            data-testid="empty-state-message"
            sx={{
              textAlign: 'center',
              py: { xs: 6, md: 8, lg: 10 },
              px: { xs: 2, md: 4 },
            }}
          >
            <Inbox sx={{ fontSize: { xs: 60, md: 80 }, color: '#E0E0E0', mb: 2 }} />
            <Typography
              variant="h6"
              color="text.secondary"
              sx={{ fontSize: { xs: '18px', md: '24px' } }}
            >
              まだ命式がありません
            </Typography>
          </Box>
        )}
      </Box>

      {/* 削除確認ダイアログ */}
      <Dialog
        open={deleteDialogOpen}
        onClose={handleCancelDelete}
        data-testid="delete-confirm-dialog"
      >
        <DialogTitle>命式を削除しますか？</DialogTitle>
        <DialogContent>
          <DialogContentText>
            この操作は取り消せません。本当に削除してもよろしいですか？
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCancelDelete} data-testid="cancel-delete-button">
            キャンセル
          </Button>
          <Button onClick={handleConfirmDelete} color="error" variant="contained" data-testid="confirm-delete-button">
            削除
          </Button>
        </DialogActions>
      </Dialog>

      {/* ボトムナビゲーション */}
      <BottomNavigation />
    </Box>
  );
};

export default ListPage;
