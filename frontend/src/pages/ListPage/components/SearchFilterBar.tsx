// SearchFilterBar - 検索・フィルタバーコンポーネント
import { Box, TextField, Button, InputAdornment, Menu, MenuItem } from '@mui/material';
import { Search, FilterList, Sort, Star, ThumbUp, Remove, Warning, Error as ErrorIcon } from '@mui/icons-material';
import { useState } from 'react';
import type { FortuneLevel } from '../../../types';

interface SearchFilterBarProps {
  searchQuery: string;
  onSearchChange: (query: string) => void;
  filterLevel: FortuneLevel | 'all';
  onFilterChange: (level: FortuneLevel | 'all') => void;
  sortBy: 'createdAt' | 'name' | 'birthDate';
  onSortChange: (sort: 'createdAt' | 'name' | 'birthDate') => void;
}

export const SearchFilterBar: React.FC<SearchFilterBarProps> = ({
  searchQuery,
  onSearchChange,
  filterLevel,
  onFilterChange,
  sortBy,
  onSortChange,
}) => {
  const [sortMenuAnchor, setSortMenuAnchor] = useState<null | HTMLElement>(null);

  const handleSortMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setSortMenuAnchor(event.currentTarget);
  };

  const handleSortMenuClose = () => {
    setSortMenuAnchor(null);
  };

  const handleSortSelect = (sort: 'createdAt' | 'name' | 'birthDate') => {
    onSortChange(sort);
    handleSortMenuClose();
  };

  const filterButtons: Array<{ level: FortuneLevel | 'all'; icon: React.ReactNode; label: string }> = [
    { level: 'all', icon: <FilterList />, label: 'すべて' },
    { level: '大吉', icon: <Star />, label: '大吉' },
    { level: '吉', icon: <ThumbUp />, label: '吉' },
    { level: '平', icon: <Remove />, label: '平' },
    { level: '凶', icon: <Warning />, label: '凶' },
    { level: '大凶', icon: <ErrorIcon />, label: '大凶' },
  ];

  const sortLabels: Record<'createdAt' | 'name' | 'birthDate', string> = {
    createdAt: '作成日',
    name: '名前',
    birthDate: '生年月日',
  };

  return (
    <Box
      sx={{
        background: 'white',
        padding: 2,
        borderRadius: '12px',
        boxShadow: '0 2px 8px rgba(0, 0, 0, 0.08)',
        mb: 2.5,
      }}
    >
      {/* 検索ボックス */}
      <TextField
        fullWidth
        variant="outlined"
        placeholder="名前・生年月日で検索..."
        value={searchQuery}
        onChange={(e) => onSearchChange(e.target.value)}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <Search color="action" />
            </InputAdornment>
          ),
        }}
        sx={{
          mb: 1.5,
          '& .MuiOutlinedInput-root': {
            backgroundColor: 'background.paper',
            '&:hover fieldset': {
              borderColor: 'primary.main',
            },
          },
        }}
      />

      {/* フィルタ・ソートボタン */}
      <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
        {filterButtons.map((btn) => (
          <Button
            key={btn.level}
            variant={filterLevel === btn.level ? 'contained' : 'outlined'}
            size="small"
            startIcon={btn.icon}
            onClick={() => onFilterChange(btn.level)}
            sx={{
              borderRadius: '20px',
              textTransform: 'none',
              fontWeight: filterLevel === btn.level ? 600 : 400,
              ...(filterLevel === btn.level && {
                background: 'linear-gradient(135deg, #D4AF37 0%, #F4E8C1 100%)',
                borderColor: 'transparent',
                color: 'white',
                '&:hover': {
                  background: 'linear-gradient(135deg, #B8941C 0%, #D4AF37 100%)',
                },
              }),
              ...((filterLevel !== btn.level && btn.level !== 'all') && {
                borderColor: '#E0E0E0',
                color: 'text.secondary',
                '&:hover': {
                  borderColor: 'primary.main',
                  color: 'primary.main',
                },
              }),
            }}
          >
            {btn.label}
          </Button>
        ))}

        {/* ソートボタン */}
        <Button
          variant="outlined"
          size="small"
          startIcon={<Sort />}
          onClick={handleSortMenuOpen}
          sx={{
            borderRadius: '20px',
            textTransform: 'none',
            borderColor: '#E0E0E0',
            color: 'text.secondary',
            '&:hover': {
              borderColor: 'primary.main',
              color: 'primary.main',
            },
          }}
        >
          {sortLabels[sortBy]}
        </Button>
        <Menu anchorEl={sortMenuAnchor} open={Boolean(sortMenuAnchor)} onClose={handleSortMenuClose}>
          <MenuItem onClick={() => handleSortSelect('createdAt')}>作成日</MenuItem>
          <MenuItem onClick={() => handleSortSelect('name')}>名前</MenuItem>
          <MenuItem onClick={() => handleSortSelect('birthDate')}>生年月日</MenuItem>
        </Menu>
      </Box>
    </Box>
  );
};
