// EditSajuModal - 命式編集モーダルコンポーネント
import { useState, useEffect } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, IconButton, Box, Typography } from '@mui/material';
import { Close, Edit } from '@mui/icons-material';
import { SajuInputForm } from '../../../components/SajuInputForm';
import { updateSaju } from '../../../services/api/sajuUpdateService';
import type { SajuSummary, SajuUpdateRequest } from '../../../types';

interface EditSajuModalProps {
  open: boolean;
  sajuData: SajuSummary | null;
  onClose: () => void;
  onSaved: () => void; // 保存後のリスト更新用コールバック
}

export const EditSajuModal: React.FC<EditSajuModalProps> = ({ open, sajuData, onClose, onSaved }) => {
  // フォーム状態
  const [name, setName] = useState('');
  const [birthDate, setBirthDate] = useState<Date | null>(null);
  const [birthTime, setBirthTime] = useState<Date | null>(null);
  const [gender, setGender] = useState<'male' | 'female' | ''>('');
  const [timeUnknown, setTimeUnknown] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  // sajuDataが変更されたらフォームを初期化
  useEffect(() => {
    if (sajuData) {
      setName(sajuData.name || '');
      setGender(sajuData.gender as 'male' | 'female');

      // ISO 8601形式の文字列をDateオブジェクトに変換
      const dateTime = new Date(sajuData.birthDatetime);
      setBirthDate(dateTime);

      // 時刻が正午12:00の場合は「時刻不明」と判定
      const hour = dateTime.getHours();
      const minute = dateTime.getMinutes();
      if (hour === 12 && minute === 0) {
        setTimeUnknown(true);
        setBirthTime(null);
      } else {
        setTimeUnknown(false);
        setBirthTime(dateTime);
      }
    }
  }, [sajuData]);

  // 保存ハンドラー
  const handleSave = async () => {
    if (!sajuData) return;

    // バリデーション
    if (!birthDate) {
      alert('生年月日を入力してください');
      return;
    }

    if (!timeUnknown && !birthTime) {
      alert('時刻を入力するか、「時刻不明」にチェックしてください');
      return;
    }

    if (!gender) {
      alert('性別を選択してください');
      return;
    }

    // 日付範囲バリデーション
    const year = birthDate.getFullYear();
    if (year < 1900 || year > 2109) {
      alert('1900-2109年の範囲内で入力してください');
      return;
    }

    // ISO 8601形式で生年月日時を生成
    const month = String(birthDate.getMonth() + 1).padStart(2, '0');
    const day = String(birthDate.getDate()).padStart(2, '0');
    const hour = timeUnknown ? '12' : String(birthTime!.getHours()).padStart(2, '0');
    const minute = timeUnknown ? '00' : String(birthTime!.getMinutes()).padStart(2, '0');
    const birthDatetime = `${year}-${month}-${day}T${hour}:${minute}:00+09:00`;

    const requestData: SajuUpdateRequest = {
      name: name || undefined,
      birthDatetime,
      gender,
      timezoneOffset: 9, // KST
    };

    setIsSaving(true);

    try {
      await updateSaju(sajuData.id, requestData);
      console.log('[EditSajuModal] 命式を更新しました:', requestData);
      onSaved(); // 親コンポーネントにリスト更新を通知
      onClose(); // モーダルを閉じる
    } catch (error) {
      console.error('[EditSajuModal] 命式の更新に失敗しました:', error);
      alert('命式の更新に失敗しました');
    } finally {
      setIsSaving(false);
    }
  };

  // キャンセルハンドラー
  const handleCancel = () => {
    onClose();
  };

  return (
    <Dialog
      open={open}
      onClose={handleCancel}
      maxWidth="sm"
      fullWidth
      data-testid="edit-saju-modal"
      sx={{
        '& .MuiDialog-paper': {
          borderRadius: { xs: 0, md: '24px' },
          maxHeight: '90vh',
        },
      }}
    >
      {/* モーダルヘッダー */}
      <DialogTitle
        sx={{
          padding: { xs: '20px 24px', md: '24px 32px' },
          borderBottom: '1px solid #e0e0e0',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <Edit sx={{ color: '#D4AF37', fontSize: { xs: '20px', md: '24px' } }} />
          <Typography
            sx={{
              fontSize: { xs: '20px', md: '24px' },
              fontWeight: 700,
              color: '#1a1a2e',
            }}
          >
            命式を編集
          </Typography>
        </Box>
        <IconButton
          onClick={handleCancel}
          sx={{
            color: '#666',
            '&:hover': {
              background: '#f5f5f5',
            },
          }}
          aria-label="閉じる"
        >
          <Close />
        </IconButton>
      </DialogTitle>

      {/* モーダルコンテンツ */}
      <DialogContent
        sx={{
          padding: { xs: '24px', md: '32px' },
        }}
      >
        <SajuInputForm
          name={name}
          birthDate={birthDate}
          birthTime={birthTime}
          gender={gender}
          timeUnknown={timeUnknown}
          onNameChange={setName}
          onBirthDateChange={setBirthDate}
          onBirthTimeChange={setBirthTime}
          onGenderChange={setGender}
          onTimeUnknownChange={setTimeUnknown}
        />
      </DialogContent>

      {/* モーダルフッター */}
      <DialogActions
        sx={{
          padding: { xs: '20px 24px', md: '24px 32px' },
          borderTop: '1px solid #e0e0e0',
          gap: '12px',
        }}
      >
        <Button
          onClick={handleCancel}
          disabled={isSaving}
          sx={{
            padding: { xs: '12px 24px', md: '16px 32px' },
            fontSize: { xs: '16px', md: '18px' },
            fontWeight: 700,
            borderRadius: { xs: '8px', md: '12px' },
            background: '#f5f5f5',
            color: '#333',
            textTransform: 'none',
            '&:hover': {
              background: '#e0e0e0',
            },
          }}
        >
          キャンセル
        </Button>
        <Button
          onClick={handleSave}
          disabled={isSaving}
          sx={{
            padding: { xs: '12px 24px', md: '16px 32px' },
            fontSize: { xs: '16px', md: '18px' },
            fontWeight: 700,
            borderRadius: { xs: '8px', md: '12px' },
            background: '#D4AF37',
            color: 'white',
            textTransform: 'none',
            boxShadow: '0 4px 12px rgba(212, 175, 55, 0.3)',
            '&:hover': {
              background: '#B8941C',
              transform: 'translateY(-2px)',
              boxShadow: '0 6px 16px rgba(212, 175, 55, 0.4)',
            },
            '&:disabled': {
              background: '#e0e0e0',
              color: '#999',
            },
          }}
        >
          {isSaving ? '保存中...' : '保存'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};
