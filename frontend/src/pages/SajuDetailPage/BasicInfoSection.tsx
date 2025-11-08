// 基本情報セクションコンポーネント
import { Box, Typography } from '@mui/material';
import type { SajuDetailPageData } from '../../types';
import { formatBirthDateTime, getGenderLabel } from '../../utils/sajuHelpers';

interface BasicInfoSectionProps {
  data: SajuDetailPageData;
}

export const BasicInfoSection: React.FC<BasicInfoSectionProps> = ({ data }) => {
  return (
    <Box
      sx={{
        backgroundColor: 'white',
        padding: { xs: '60px 16px 20px', sm: '80px 40px 30px' },
        borderBottom: '4px solid #D4AF37',
        borderRadius: { xs: 0, sm: '12px' },
        marginBottom: { xs: 0, sm: '20px' },
        overflow: 'hidden',
      }}
    >
      <Typography
        variant="h6"
        sx={{
          fontSize: { xs: '20px', sm: '28px' },
          fontWeight: 700,
          color: '#1a1a2e',
          mb: { xs: '20px', sm: '20px' },
        }}
      >
        基本情報
      </Typography>

      <Box>
        <Typography
          sx={{
            fontSize: { xs: '24px', sm: '32px' },
            fontWeight: 700,
            color: '#1a1a2e',
            mb: '8px',
          }}
        >
          {data.name || '未設定'} ({getGenderLabel(data.gender)})
        </Typography>
        <Typography
          sx={{
            fontSize: { xs: '16px', sm: '20px' },
            color: '#666',
          }}
        >
          {formatBirthDateTime(data.birthDatetime)}
        </Typography>
      </Box>
    </Box>
  );
};
