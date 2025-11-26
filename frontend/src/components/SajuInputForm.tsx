// SajuInputForm - 命式入力フォームコンポーネント
// TopPageとEditSajuModalで共用
import { Box, Typography, TextField, FormControl, FormLabel, RadioGroup, FormControlLabel, Radio, Checkbox } from '@mui/material';
import { LocalizationProvider, DatePicker, TimePicker } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { ja } from 'date-fns/locale/ja';

interface SajuInputFormProps {
  name: string;
  birthDate: Date | null;
  birthTime: Date | null;
  gender: 'male' | 'female' | '';
  timeUnknown: boolean;
  onNameChange: (value: string) => void;
  onBirthDateChange: (value: Date | null) => void;
  onBirthTimeChange: (value: Date | null) => void;
  onGenderChange: (value: 'male' | 'female') => void;
  onTimeUnknownChange: (value: boolean) => void;
}

export const SajuInputForm: React.FC<SajuInputFormProps> = ({
  name,
  birthDate,
  birthTime,
  gender,
  timeUnknown,
  onNameChange,
  onBirthDateChange,
  onBirthTimeChange,
  onGenderChange,
  onTimeUnknownChange,
}) => {
  return (
    <Box>
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
          onChange={(e) => onNameChange(e.target.value)}
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
              onChange={(newValue: Date | null) => onBirthDateChange(newValue)}
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
            onChange={(newValue: Date | null) => onBirthTimeChange(newValue)}
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
                  onTimeUnknownChange(e.target.checked);
                  if (e.target.checked) {
                    onBirthTimeChange(null);
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
            onChange={(e) => onGenderChange(e.target.value as 'male' | 'female')}
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
    </Box>
  );
};
