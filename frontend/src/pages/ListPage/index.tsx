// ListPage - 命式リストページ（完全実装版）
import { useState, useEffect, useMemo } from 'react';
import { Box, Typography, Button, Alert, IconButton, Dialog, DialogTitle, DialogContent, DialogContentText, DialogActions } from '@mui/material';
import { AddCircle, CloudUpload, ChevronRight, ArrowBack, Settings as SettingsIcon, Inbox } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../features/auth/hooks/useAuth';
import { SajuCard } from './components/SajuCard';
import { SearchFilterBar } from './components/SearchFilterBar';
import { getSajuList, deleteSaju } from '../../services/api/sajuListService';
import type { SajuSummary, FortuneLevel } from '../../types';

export const ListPage: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const isGuestMode = user?.role === 'guest';

  // 状態管理
  const [sajuList, setSajuList] = useState<SajuSummary[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterLevel, setFilterLevel] = useState<FortuneLevel | 'all'>('all');
  const [sortBy, setSortBy] = useState<'createdAt' | 'name' | 'birthDate'>('createdAt');
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

  // フィルタリング・ソート処理
  const filteredAndSortedList = useMemo(() => {
    let result = [...sajuList];

    // 検索フィルタ
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      result = result.filter((saju) => {
        const name = (saju.name || '').toLowerCase();
        const birthDate = saju.birthDatetime.toLowerCase();
        return name.includes(query) || birthDate.includes(query);
      });
    }

    // 吉凶レベルフィルタ
    if (filterLevel !== 'all') {
      result = result.filter((saju) => saju.fortuneLevel === filterLevel);
    }

    // ソート
    result.sort((a, b) => {
      switch (sortBy) {
        case 'createdAt':
          return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime();
        case 'name':
          return (a.name || '無題').localeCompare(b.name || '無題', 'ja');
        case 'birthDate':
          return new Date(b.birthDatetime).getTime() - new Date(a.birthDatetime).getTime();
        default:
          return 0;
      }
    });

    return result;
  }, [sajuList, searchQuery, filterLevel, sortBy]);

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
        <IconButton onClick={handleBack} sx={{ color: 'white' }} aria-label="トップページに戻る">
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
        <IconButton onClick={handleSettings} sx={{ color: 'white' }} aria-label="設定">
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
          pb: { xs: '80px', md: '80px' },
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
            background: 'linear-gradient(135deg, #D4AF37 0%, #F4E8C1 100%)',
            py: { xs: 1.5, md: 1.75 },
            fontWeight: 700,
            fontSize: { xs: '14px', md: '16px' },
            borderRadius: { xs: '10px', md: '12px' },
            boxShadow: '0 4px 12px rgba(212, 175, 55, 0.4)',
            mb: { xs: 2, md: 2.5 },
            transition: 'all 0.3s',
            '&:hover': {
              transform: 'translateY(-2px)',
              boxShadow: '0 6px 20px rgba(212, 175, 55, 0.5)',
              background: 'linear-gradient(135deg, #B8941C 0%, #D4AF37 100%)',
            },
          }}
        >
          新しい命式を作成
        </Button>

        {/* 検索・フィルタバー */}
        <SearchFilterBar
          searchQuery={searchQuery}
          onSearchChange={setSearchQuery}
          filterLevel={filterLevel}
          onFilterChange={setFilterLevel}
          sortBy={sortBy}
          onSortChange={setSortBy}
        />

        {/* 命式カード一覧 - レスポンシブグリッド（モックアップ完全一致） */}
        {filteredAndSortedList.length > 0 ? (
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
            {filteredAndSortedList.map((saju) => (
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
              gutterBottom
              sx={{ fontSize: { xs: '18px', md: '24px' } }}
            >
              {searchQuery || filterLevel !== 'all' ? '該当する命式がありません' : 'まだ命式がありません'}
            </Typography>
            <Typography
              variant="body2"
              color="text.secondary"
              sx={{
                mb: 3,
                fontSize: { xs: '14px', md: '16px' },
              }}
            >
              {searchQuery || filterLevel !== 'all'
                ? '検索条件を変更してください'
                : '「新しい命式を作成」ボタンから始めましょう'}
            </Typography>
            {(!searchQuery && filterLevel === 'all') && (
              <Button variant="contained" onClick={handleCreateNew}>
                新しい命式を作成
              </Button>
            )}
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
    </Box>
  );
};

export default ListPage;
