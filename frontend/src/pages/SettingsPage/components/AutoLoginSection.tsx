import { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Switch,
  FormControlLabel,
  Radio,
  RadioGroup,
  FormControl
} from '@mui/material';
import VpnKeyIcon from '@mui/icons-material/VpnKey';
import { updateUserSettings, getUserSettings } from '../../../services/api/settingsService';
import type { UserSettings } from '../../../types';

export const AutoLoginSection: React.FC = () => {
  const [rememberMe, setRememberMe] = useState(true);
  const [sessionDuration, setSessionDuration] = useState<'7d' | '30d' | 'forever'>('30d');

  // 初期設定を読み込み
  useEffect(() => {
    const settings = getUserSettings();
    setRememberMe(settings.rememberMe);
    setSessionDuration(settings.sessionDuration);
  }, []);

  const handleRememberMeChange = async (checked: boolean) => {
    setRememberMe(checked);

    const settings: UserSettings = {
      rememberMe: checked,
      sessionDuration
    };

    await updateUserSettings(settings);
  };

  const handleSessionDurationChange = async (value: '7d' | '30d' | 'forever') => {
    setSessionDuration(value);

    const settings: UserSettings = {
      rememberMe,
      sessionDuration: value
    };

    await updateUserSettings(settings);
  };

  return (
    <Box
      sx={{
        background: 'white',
        borderRadius: 3,
        boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)',
        mb: 2.5,
        overflow: 'hidden'
      }}
    >
      {/* セクションヘッダー */}
      <Box
        sx={{
          p: 2,
          background: theme => theme.palette.gold.LIGHT_GOLD,
          borderBottom: '1px solid',
          borderColor: 'divider'
        }}
      >
        <Typography
          variant="h6"
          sx={{
            fontSize: '16px',
            fontWeight: 500,
            color: theme => theme.palette.gold.DARK_GOLD,
            display: 'flex',
            alignItems: 'center',
            gap: 1
          }}
        >
          <VpnKeyIcon />
          自動ログイン設定
        </Typography>
      </Box>

      {/* セクションコンテンツ */}
      <Box sx={{ p: 2 }}>
        {/* トグルスイッチ */}
        <Box sx={{ pb: 2, borderBottom: '1px solid', borderColor: 'divider' }}>
          <FormControlLabel
            control={
              <Switch
                checked={rememberMe}
                onChange={(e) => handleRememberMeChange(e.target.checked)}
                sx={{
                  '& .MuiSwitch-switchBase.Mui-checked': {
                    color: theme => theme.palette.gold.PRIMARY_GOLD
                  },
                  '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': {
                    backgroundColor: theme => theme.palette.gold.PRIMARY_GOLD
                  }
                }}
              />
            }
            label="ログイン状態を保持"
          />
        </Box>

        {/* セッション有効期限 */}
        <Box sx={{ pt: 2 }}>
          <Typography variant="body2" fontWeight={500} mb={1.5}>
            セッション有効期限
          </Typography>
          <FormControl component="fieldset">
            <RadioGroup
              value={sessionDuration}
              onChange={(e) => handleSessionDurationChange(e.target.value as '7d' | '30d' | 'forever')}
            >
              <FormControlLabel
                value="7d"
                control={
                  <Radio
                    sx={{
                      '&.Mui-checked': {
                        color: theme => theme.palette.gold.PRIMARY_GOLD
                      }
                    }}
                  />
                }
                label="7日間"
              />
              <FormControlLabel
                value="30d"
                control={
                  <Radio
                    sx={{
                      '&.Mui-checked': {
                        color: theme => theme.palette.gold.PRIMARY_GOLD
                      }
                    }}
                  />
                }
                label="30日間"
              />
              <FormControlLabel
                value="forever"
                control={
                  <Radio
                    sx={{
                      '&.Mui-checked': {
                        color: theme => theme.palette.gold.PRIMARY_GOLD
                      }
                    }}
                  />
                }
                label="無期限"
              />
            </RadioGroup>
          </FormControl>
        </Box>
      </Box>
    </Box>
  );
};
