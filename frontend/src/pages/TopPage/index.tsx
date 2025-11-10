// TopPage - P-001: 命式記入（トップページ）
// レスポンシブデザイン対応
import { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  TextField,
  Button,
  FormControl,
  FormLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  Checkbox,
} from '@mui/material';
import {
  Calculate,
  AutoAwesome,
} from '@mui/icons-material';
import { LocalizationProvider, DatePicker, TimePicker } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { ja } from 'date-fns/locale/ja';
import { GoldenPeppaLoading } from '../../components/GoldenPeppaLoading';
import { BottomNavigation } from '../../components/BottomNavigation';
import { calculateSaju, saveSaju } from '../../services/api/sajuCalculationService';
import { AuthContext } from '../../features/auth/contexts/AuthContext';
import type { BirthDataRequest, SajuResponse } from '../../types';

export const TopPage: React.FC = () => {
  const navigate = useNavigate();
  const authContext = useContext(AuthContext);
  const isAuthenticated = authContext?.isAuthenticated ?? false;

  // フォーム状態
  const [name, setName] = useState('');
  const [birthDate, setBirthDate] = useState<Date | null>(null);
  const [birthTime, setBirthTime] = useState<Date | null>(null);
  const [gender, setGender] = useState<'male' | 'female' | ''>('');
  const [timeUnknown, setTimeUnknown] = useState(false);

  // UI状態
  const [isLoading, setIsLoading] = useState(false);
  const [validationError, setValidationError] = useState<string>('');
  const [networkError, setNetworkError] = useState<string>('');

  // 命式計算 → 自動保存 → 詳細ページ遷移
  const handleCalculate = async (e: React.FormEvent) => {
    e.preventDefault();

    // バリデーションエラーをクリア
    setValidationError('');
    setNetworkError('');

    // 生年月日時バリデーション
    if (!birthDate) {
      setValidationError('生年月日を入力してください');
      return;
    }

    if (!timeUnknown && !birthTime) {
      setValidationError('時刻を入力するか、「時刻不明」にチェックしてください');
      return;
    }

    // 性別バリデーション
    if (!gender) {
      setValidationError('性別を選択してください');
      return;
    }

    // 日付範囲バリデーション（1900-2109年）
    const year = birthDate.getFullYear();
    if (year < 1900 || year > 2109) {
      setValidationError('1900-2109年の範囲内で入力してください');
      return;
    }

    // ISO 8601形式で生年月日時を結合
    const month = String(birthDate.getMonth() + 1).padStart(2, '0');
    const day = String(birthDate.getDate()).padStart(2, '0');

    // デバッグ: DatePickerの生の値をログ出力
    console.log('[TopPage DEBUG] birthDate:', birthDate);
    console.log('[TopPage DEBUG] birthDate.toISOString():', birthDate.toISOString());
    console.log('[TopPage DEBUG] year:', year, 'month:', month, 'day:', day);

    if (!timeUnknown && birthTime) {
      console.log('[TopPage DEBUG] birthTime:', birthTime);
      console.log('[TopPage DEBUG] birthTime.toISOString():', birthTime.toISOString());
    }

    // 時刻不明の場合は正午（12:00）を使用
    const hour = timeUnknown ? '12' : String(birthTime!.getHours()).padStart(2, '0');
    const minute = timeUnknown ? '00' : String(birthTime!.getMinutes()).padStart(2, '0');
    const birthDatetime = `${year}-${month}-${day}T${hour}:${minute}:00+09:00`;

    console.log('[TopPage DEBUG] 生成されたbirthDatetime:', birthDatetime);

    const requestData: BirthDataRequest = {
      birthDatetime,
      gender,
      name: name || undefined,
      timezoneOffset: 9, // KST
    };

    console.log('[TopPage DEBUG] APIリクエストデータ:', JSON.stringify(requestData, null, 2));

    setIsLoading(true);

    // ローディングアニメーションの表示を確実にするため、次のイベントループまで待つ
    await new Promise(resolve => setTimeout(resolve, 0));

    try {
      // 1. 命式計算
      const result = await calculateSaju(requestData);

      // 2. 保存処理（ゲスト/ログインモードで分岐）
      let savedId: string;

      if (isAuthenticated) {
        // ログインモード: サーバーに保存
        const saveResult = await saveSaju(result);
        savedId = saveResult.id;
      } else {
        // ゲストモード: LocalStorageに保存
        savedId = result.id;
        const existingData = localStorage.getItem('saju_data');
        const sajuList: SajuResponse[] = existingData ? JSON.parse(existingData) : [];

        console.log('[TopPage] 保存前のLocalStorage:', sajuList.length, '件');

        // 既存データがあれば更新、なければ追加
        const existingIndex = sajuList.findIndex(item => item.id === result.id);
        if (existingIndex >= 0) {
          sajuList[existingIndex] = result;
          console.log('[TopPage] 既存データを更新:', result.id);
        } else {
          sajuList.push(result);
          console.log('[TopPage] 新規データを追加:', result.id);
        }

        localStorage.setItem('saju_data', JSON.stringify(sajuList));
        console.log('[TopPage] 保存後のLocalStorage:', sajuList.length, '件');
      }

      // 3. 詳細ページに遷移
      navigate(`/detail/${savedId}`);
    } catch (error) {
      console.error('命式計算エラー:', error);
      setIsLoading(false);
      setNetworkError('ネットワークエラーが発生しました。接続を確認して再度お試しください。');
    }
  };

  // ローディング表示
  if (isLoading) {
    return <GoldenPeppaLoading />;
  }

  return (
    <>
      <Box
        sx={{
          minHeight: '100vh',
          background: 'linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: { xs: '20px', md: '40px' },
          paddingBottom: { xs: '90px', md: '100px' }, // ボトムナビゲーション分の余白
        }}
      >
      {/* メインコンテナ */}
      <Box
        sx={{
          width: '100%',
          maxWidth: { xs: '100%', md: '600px', lg: '800px' },
          margin: '0 auto',
        }}
      >
        {/* ヘッダー */}
        <Box
          sx={{
            textAlign: 'center',
            marginBottom: { xs: '40px', md: '60px' },
          }}
        >
          {/* ペッパーミル画像 + キラキラエフェクト（統合画像） */}
          <Box
            component="img"
            src="/images/peppa-with-sparkles.png"
            alt="Golden Peppa"
            sx={{
              width: { xs: '160px', md: '200px', lg: '240px' },
              height: { xs: '160px', md: '200px', lg: '240px' },
              objectFit: 'contain',
              marginBottom: { xs: '16px', md: '20px' },
              display: 'block',
              marginLeft: 'auto',
              marginRight: 'auto',
            }}
          />

          {/* Golden Peppa タイトル */}
          <Typography
            sx={{
              fontSize: { xs: '40px', md: '52px', lg: '68px' },
              fontWeight: 400,
              color: '#D4AF37',
              marginBottom: { xs: '8px', md: '8px' },
              letterSpacing: '1px',
              fontFamily: "'Indie Flower', cursive",
            }}
          >
            Golden Peppa
          </Typography>

          {/* サブタイトル */}
          <Typography
            sx={{
              fontSize: { xs: '14px', md: '16px', lg: '18px' },
              color: '#666',
              fontWeight: 500,
            }}
          >
            あなたの運命に魔法をかける
          </Typography>
        </Box>

        {/* 命式記入カード */}
        <Box
          sx={{
            background: 'white',
            borderRadius: { xs: '16px', md: '24px' },
            boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
            padding: { xs: '24px', md: '40px', lg: '50px 60px' },
            marginBottom: { xs: '20px', md: '30px' },
          }}
        >
          <Typography
            sx={{
              fontSize: { xs: '20px', md: '24px', lg: '28px' },
              fontWeight: 700,
              color: '#1a1a2e',
              marginBottom: { xs: '20px', md: '30px' },
              textAlign: 'center',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px',
            }}
          >
            <AutoAwesome sx={{ color: '#D4AF37', fontSize: { xs: '20px', md: '24px', lg: '28px' } }} />
            命式を記入
          </Typography>

          <Box component="form" onSubmit={handleCalculate}>
            {/* 名前入力 */}
            <Box sx={{ marginBottom: { xs: '24px', md: '32px' } }}>
              <Typography
                sx={{
                  fontSize: { xs: '14px', md: '16px' },
                  fontWeight: 600,
                  color: '#333',
                  marginBottom: { xs: '8px', md: '12px' },
                }}
              >
                名前（任意）
              </Typography>
              <TextField
                fullWidth
                placeholder="白石"
                value={name}
                onChange={(e) => setName(e.target.value)}
                inputProps={{
                  'data-testid': 'name',
                }}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    borderRadius: { xs: '8px', md: '12px' },
                    fontSize: { xs: '16px', md: '18px' },
                    '& input': {
                      padding: { xs: '12px 16px', md: '14px 20px' },
                    },
                    '&:hover fieldset': {
                      borderColor: '#D4AF37',
                    },
                    '&.Mui-focused fieldset': {
                      borderColor: '#D4AF37',
                      boxShadow: '0 0 0 3px rgba(212, 175, 55, 0.1)',
                    },
                  },
                }}
              />
            </Box>

            {/* 生年月日時入力 */}
            <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ja}>
              <Box sx={{ marginBottom: { xs: '24px', md: '32px' } }}>
                <Typography
                  sx={{
                    fontSize: { xs: '14px', md: '16px' },
                    fontWeight: 600,
                    color: '#333',
                    marginBottom: { xs: '8px', md: '12px' },
                  }}
                >
                  生年月日時
                </Typography>
                <Box sx={{ marginBottom: '12px' }}>
                  <DatePicker
                    value={birthDate}
                    onChange={(newValue: Date | null) => setBirthDate(newValue)}
                    minDate={new Date(1900, 0, 1)}
                    maxDate={new Date(2109, 11, 31)}
                    format="yyyy年MM月dd日"
                    slotProps={{
                      textField: {
                        fullWidth: true,
                        inputProps: {
                          'data-testid': 'birth-date',
                        },
                        sx: {
                          '& .MuiOutlinedInput-root': {
                            borderRadius: { xs: '8px', md: '12px' },
                            fontSize: { xs: '16px', md: '18px' },
                            '& input': {
                              padding: { xs: '12px 16px', md: '14px 20px' },
                            },
                            '&:hover fieldset': {
                              borderColor: '#D4AF37',
                            },
                            '&.Mui-focused fieldset': {
                              borderColor: '#D4AF37',
                              boxShadow: '0 0 0 3px rgba(212, 175, 55, 0.1)',
                            },
                          },
                        },
                      },
                    }}
                  />
                </Box>
                <TimePicker
                  value={birthTime}
                  onChange={(newValue: Date | null) => setBirthTime(newValue)}
                  disabled={timeUnknown}
                  ampm={false}
                  format="HH:mm"
                  slotProps={{
                    textField: {
                      fullWidth: true,
                      inputProps: {
                        'data-testid': 'birth-time',
                      },
                      sx: {
                        '& .MuiOutlinedInput-root': {
                          borderRadius: { xs: '8px', md: '12px' },
                          fontSize: { xs: '16px', md: '18px' },
                          opacity: timeUnknown ? 0.5 : 1,
                          '& input': {
                            padding: { xs: '12px 16px', md: '14px 20px' },
                          },
                          '&:hover fieldset': {
                            borderColor: '#D4AF37',
                          },
                          '&.Mui-focused fieldset': {
                            borderColor: '#D4AF37',
                            boxShadow: '0 0 0 3px rgba(212, 175, 55, 0.1)',
                          },
                        },
                      },
                    },
                  }}
                />
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={timeUnknown}
                      onChange={(e) => {
                        setTimeUnknown(e.target.checked);
                        if (e.target.checked) {
                          setBirthTime(null);
                        }
                      }}
                      data-testid="time-unknown-checkbox"
                      sx={{
                        color: '#D4AF37',
                        '&.Mui-checked': {
                          color: '#D4AF37',
                        },
                      }}
                    />
                  }
                  label="時刻不明（正午12:00で計算）"
                  sx={{
                    marginTop: { xs: '12px', md: '12px' },
                    color: '#666',
                    '& .MuiFormControlLabel-label': {
                      fontSize: { xs: '14px', md: '16px' },
                    },
                  }}
                />
              </Box>
            </LocalizationProvider>

            {/* 性別選択 */}
            <Box sx={{ marginBottom: { xs: '24px', md: '32px' } }}>
              <FormControl component="fieldset" fullWidth>
                <FormLabel
                  sx={{
                    fontSize: { xs: '14px', md: '16px' },
                    fontWeight: 600,
                    color: '#333',
                    marginBottom: { xs: '8px', md: '12px' },
                    '&.Mui-focused': {
                      color: '#333',
                    },
                  }}
                >
                  性別
                </FormLabel>
                <RadioGroup
                  row
                  value={gender}
                  onChange={(e) => setGender(e.target.value as 'male' | 'female')}
                  sx={{ gap: { xs: '12px', md: '20px' }, display: 'flex' }}
                >
                  <FormControlLabel
                    value="male"
                    data-testid="gender-male"
                    control={
                      <Radio
                        sx={{
                          display: 'none',
                        }}
                      />
                    }
                    label={
                      <Box sx={{ textAlign: 'center' }}>
                        <Typography sx={{ fontSize: '24px', marginBottom: '4px' }}>👨</Typography>
                        <Typography sx={{ fontSize: { xs: '16px', md: '18px' }, fontWeight: 600, color: gender === 'male' ? 'white' : '#666' }}>男性</Typography>
                      </Box>
                    }
                    sx={{
                      flex: 1,
                      margin: 0,
                      padding: { xs: '14px', md: '18px' },
                      minHeight: '48px',
                      border: '2px solid #e0e0e0',
                      borderRadius: { xs: '8px', md: '12px' },
                      transition: 'all 0.2s',
                      cursor: 'pointer',
                      ...(gender === 'male' && {
                        borderColor: '#D4AF37',
                        background: '#D4AF37',
                      }),
                      '&:hover': {
                        borderColor: '#D4AF37',
                        background: gender === 'male' ? '#D4AF37' : '#fffbf0',
                      },
                    }}
                  />
                  <FormControlLabel
                    value="female"
                    data-testid="gender-female"
                    control={
                      <Radio
                        sx={{
                          display: 'none',
                        }}
                      />
                    }
                    label={
                      <Box sx={{ textAlign: 'center' }}>
                        <Typography sx={{ fontSize: '24px', marginBottom: '4px' }}>👩</Typography>
                        <Typography sx={{ fontSize: { xs: '16px', md: '18px' }, fontWeight: 600, color: gender === 'female' ? 'white' : '#666' }}>女性</Typography>
                      </Box>
                    }
                    sx={{
                      flex: 1,
                      margin: 0,
                      padding: { xs: '14px', md: '18px' },
                      minHeight: '48px',
                      border: '2px solid #e0e0e0',
                      borderRadius: { xs: '8px', md: '12px' },
                      transition: 'all 0.2s',
                      cursor: 'pointer',
                      ...(gender === 'female' && {
                        borderColor: '#D4AF37',
                        background: '#D4AF37',
                      }),
                      '&:hover': {
                        borderColor: '#D4AF37',
                        background: gender === 'female' ? '#D4AF37' : '#fffbf0',
                      },
                    }}
                  />
                </RadioGroup>
              </FormControl>
            </Box>

            {/* バリデーションエラーメッセージ */}
            {validationError && (
              <Box
                data-testid="error-message"
                sx={{
                  marginBottom: '16px',
                  padding: '12px 16px',
                  minHeight: '40px',
                  background: '#FFEBEE',
                  border: '1px solid #F44336',
                  borderRadius: '8px',
                  color: '#C62828',
                  fontSize: { xs: '14px', md: '15px' },
                  fontWeight: 500,
                }}
              >
                {validationError}
              </Box>
            )}

            {/* ネットワークエラーメッセージ */}
            {networkError && (
              <Box
                data-testid="error-message"
                sx={{
                  marginBottom: '16px',
                  padding: '12px 16px',
                  minHeight: '40px',
                  background: '#FFEBEE',
                  border: '1px solid #F44336',
                  borderRadius: '8px',
                  color: '#C62828',
                  fontSize: { xs: '14px', md: '15px' },
                  fontWeight: 500,
                }}
              >
                {networkError}
              </Box>
            )}

            {/* 計算ボタン */}
            <Button
              type="submit"
              fullWidth
              data-testid="calculate-button"
              sx={{
                padding: { xs: '16px', md: '20px' },
                background: '#D4AF37',
                color: 'white',
                borderRadius: { xs: '12px', md: '16px' },
                fontSize: { xs: '18px', md: '20px' },
                fontWeight: 700,
                boxShadow: '0 4px 12px rgba(212, 175, 55, 0.3)',
                textTransform: 'none',
                transition: 'all 0.2s',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
                '&:hover': {
                  background: '#B8941C',
                  transform: 'translateY(-2px)',
                  boxShadow: '0 6px 16px rgba(212, 175, 55, 0.4)',
                },
                '&:active': {
                  transform: 'translateY(0)',
                },
              }}
            >
              <Calculate sx={{ fontSize: { xs: '20px', md: '24px' } }} />
              命式を計算
            </Button>
          </Box>
        </Box>
      </Box>
      </Box>

      {/* ボトムナビゲーション */}
      <BottomNavigation />
    </>
  );
};

export default TopPage;
