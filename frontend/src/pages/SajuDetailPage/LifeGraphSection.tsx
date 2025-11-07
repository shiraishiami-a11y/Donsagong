// LifeGraphSection.tsx - 人生グラフセクション
import { Box, Typography } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import type { DaeunInfo } from '../../types';

// カスタムDotコンポーネント（将来の拡張用）
// const CustomDot = () => null;

interface LifeGraphSectionProps {
  currentAge: number;
  graphData: Array<{
    age: number;
    fortuneLevel: number;
  }>;
  daeunList: DaeunInfo[];
}

export const LifeGraphSection: React.FC<LifeGraphSectionProps> = ({ currentAge, graphData, daeunList }) => {
  // 大運の範囲を計算
  const firstDaeun = daeunList[0];
  const lastDaeun = daeunList[Math.min(9, daeunList.length - 1)];
  const minAge = firstDaeun?.startAge || 0;
  const maxAge = lastDaeun?.endAge || 100;

  // X軸の目盛り
  const xAxisTicks = daeunList.slice(0, 10).map(d => d.startAge);

  // 大運の範囲内のデータだけフィルタリング
  const filteredData = graphData.filter(point => point.age >= minAge && point.age <= maxAge);

  // グラフデータを作成
  const chartData = filteredData.map(point => ({
    age: point.age,
    fortuneLevel: point.fortuneLevel,
  }));

  return (
    <Box
      sx={{
        backgroundColor: 'white',
        padding: { xs: '20px', sm: '30px 40px' },
        margin: { xs: '16px 0', sm: '20px 0' },
        borderRadius: { xs: 0, sm: '12px' },
      }}
    >
      {/* タイトル */}
      <Typography
        variant="h6"
        sx={{
          fontSize: { xs: '18px', sm: '24px' },
          fontWeight: 700,
          color: '#1a1a2e',
          mb: { xs: '16px', sm: '24px' },
        }}
      >
        人生グラフ（吉凶の流れ）
      </Typography>

      {/* サブタイトル */}
      <Typography
        variant="body2"
        sx={{
          fontSize: '14px',
          color: '#666',
          mb: '16px',
        }}
      >
        大運ベースの吉凶レベル推移（{minAge}-{maxAge}歳、左右スクロール可能）
      </Typography>

      {/* グラフコンテナ（横スクロール可能） */}
      <Box
        sx={{
          overflowX: 'auto',
          WebkitOverflowScrolling: 'touch',
          padding: '12px 0',
        }}
      >
        <Box
          sx={{
            minWidth: { xs: '800px', sm: '1000px', lg: '1200px' },
            height: { xs: '250px', sm: '350px', lg: '450px' },
            background: 'white',
            borderRadius: '12px',
            padding: '20px',
            boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          }}
        >
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={chartData}
              margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
            >
              <CartesianGrid strokeDasharray="2 2" stroke="#e0e0e0" />

              <XAxis
                dataKey="age"
                stroke="#666"
                style={{ fontSize: '0.7rem' }}
                domain={[minAge, maxAge]}
                ticks={xAxisTicks}
              />

              <YAxis
                stroke="#666"
                style={{ fontSize: '0.7rem' }}
                domain={[1, 5]}
                ticks={[1, 2, 3, 4, 5]}
              />

              <Tooltip
                contentStyle={{
                  background: 'white',
                  border: '1px solid #ccc',
                  borderRadius: '4px',
                  padding: '8px',
                }}
                labelFormatter={(value) => `${value}歳`}
                formatter={(value) => {
                  const numValue = typeof value === 'number' ? value :
                                   typeof value === 'string' ? parseFloat(value) : null;
                  if (numValue === null || isNaN(numValue)) return null;
                  const labels: Record<number, string> = {
                    5: '大吉',
                    4: '吉',
                    3: '平',
                    2: '凶',
                    1: '大凶',
                  };
                  return [labels[numValue] || '不明', '吉凶'];
                }}
              />

              {/* 吉凶レベルの折れ線グラフ（滑らかな曲線） */}
              <Line
                type="monotone"
                dataKey="fortuneLevel"
                stroke="#D4AF37"
                strokeWidth={4}
                dot={false}
                connectNulls={false}
              />

              {/* 現在年齢の垂直線（最後に描画して確実に表示） */}
              {currentAge >= minAge && currentAge <= maxAge && (
                <ReferenceLine
                  x={currentAge}
                  stroke="#F44336"
                  strokeDasharray="5 5"
                  strokeWidth={2}
                  label={{
                    value: `現在${currentAge}歳`,
                    position: 'top',
                    fill: '#F44336',
                    fontSize: 12,
                    fontWeight: 'bold',
                  }}
                />
              )}
            </LineChart>
          </ResponsiveContainer>
        </Box>
      </Box>
    </Box>
  );
};

export default LifeGraphSection;
