// SajuDetailPage - 命式詳細ページ（P-003）
import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Box, Typography, IconButton, Button } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import SaveIcon from '@mui/icons-material/Save';
import { MainLayout } from '../../layouts/MainLayout';
import { BasicInfoSection } from './BasicInfoSection';
import { PillarsSection } from './PillarsSection';
import { LifeGraphSection } from './LifeGraphSection';
import { TodayFortuneSection } from './TodayFortuneSection';
import { DaeunScrollSection } from './components/DaeunScrollSection';
import { YearFortuneScrollSection } from './components/YearFortuneScrollSection';
import { MonthFortuneScrollSection } from './components/MonthFortuneScrollSection';
import { DayFortuneScrollSection } from './components/DayFortuneScrollSection';
import type { SajuDetailPageData, CurrentFortuneResponse } from '../../types';
import { getSajuDetail, getCurrentFortune, saveSaju } from '../../services/api/sajuListService';
import GoldenPeppaLoading from '../../components/GoldenPeppaLoading';
import { FortuneLevelMap } from '../../types';
import { ApiError } from '../../services/api/client';
import { getStemElement, getBranchElement } from '../../utils/sajuHelpers';

export const SajuDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [data, setData] = useState<SajuDetailPageData | null>(null);
  const [currentFortune, setCurrentFortune] = useState<CurrentFortuneResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [is404, setIs404] = useState(false);

  // 水平スクロール用の状態管理
  const [selectedDaeunStartAge, setSelectedDaeunStartAge] = useState<number | null>(null);
  const [selectedYear, setSelectedYear] = useState<number | null>(null);
  const [selectedMonth, setSelectedMonth] = useState<number | null>(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        setError(null);

        if (!id) {
          throw new Error('命式IDが指定されていません');
        }

        // 命式詳細を取得
        const sajuData = await getSajuDetail(id);

        // birthDatetimeから年月日時分を抽出
        const birthDate = new Date(sajuData.birthDatetime);
        const birthYear = birthDate.getFullYear();
        const birthMonth = birthDate.getMonth() + 1; // 0-indexed なので +1
        const birthDay = birthDate.getDate();
        const birthHour = birthDate.getHours();
        const birthMinute = birthDate.getMinutes();

        // 命式データから生年月日情報を取得して今日の運を取得
        const fortuneData = await getCurrentFortune(
          birthYear,
          birthMonth,
          birthDay,
          birthHour,
          birthMinute,
          sajuData.gender
        );

        setData(sajuData);
        setCurrentFortune(fortuneData);

        // デバッグ用ログ
        console.log('[SajuDetailPage] fortuneData:', fortuneData);
        console.log('[SajuDetailPage] yearFortune.fortuneLevel:', fortuneData.yearFortune.fortuneLevel, '→', FortuneLevelMap[fortuneData.yearFortune.fortuneLevel]);
        console.log('[SajuDetailPage] monthFortune.fortuneLevel:', fortuneData.monthFortune.fortuneLevel, '→', FortuneLevelMap[fortuneData.monthFortune.fortuneLevel]);
        console.log('[SajuDetailPage] dayFortune.fortuneLevel:', fortuneData.dayFortune.fortuneLevel, '→', FortuneLevelMap[fortuneData.dayFortune.fortuneLevel]);

        // 現在の大運を自動選択（初回のみ）
        const currentDaeun = sajuData.daeunList.find((d) => d.isCurrent);
        if (currentDaeun) {
          setSelectedDaeunStartAge(currentDaeun.startAge);

          // 0.5秒後に現在の年を自動選択（UX向上）
          setTimeout(() => {
            setSelectedYear(sajuData.currentYear);
          }, 500);
        }
      } catch (err) {
        console.error('命式詳細の取得に失敗しました:', err);

        // 404エラーの場合、特別なハンドリング
        if (err instanceof ApiError && err.status === 404) {
          setIs404(true);
          setError('命式が見つかりません');

          // 3秒後にリストページへリダイレクト
          setTimeout(() => {
            navigate('/list');
          }, 3000);
        } else {
          setError(err instanceof Error ? err.message : '不明なエラーが発生しました');
        }
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [id, navigate]);

  const handleDaeunSelect = (startAge: number) => {
    setSelectedDaeunStartAge(startAge);
    setSelectedYear(null);
    setSelectedMonth(null);
  };

  const handleYearSelect = (year: number) => {
    setSelectedYear(year);
    setSelectedMonth(null);
  };

  const handleMonthSelect = (month: number) => {
    setSelectedMonth(month);
  };

  if (loading) {
    return <GoldenPeppaLoading />;
  }

  if (error || !data) {
    return (
      <MainLayout>
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            minHeight: '50vh',
            gap: 2,
            px: 2,
          }}
        >
          <Typography variant="h6" color="error">
            {error || '命式データの読み込みに失敗しました'}
          </Typography>

          {is404 && (
            <>
              <Typography variant="body2" color="text.secondary">
                3秒後にリストページへ自動的に移動します...
              </Typography>
              <Button
                variant="contained"
                onClick={() => navigate('/list')}
                sx={{
                  backgroundColor: '#D4AF37',
                  '&:hover': {
                    backgroundColor: '#B8941C',
                  },
                }}
              >
                リストページへ戻る
              </Button>
            </>
          )}
        </Box>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <Box
        sx={{
          maxWidth: { sm: '900px', lg: '1400px' },
          width: '100%',
          margin: '0 auto',
          backgroundColor: '#f5f5f5',
          minHeight: '100vh',
          pb: 7.5,
          position: 'relative',
          px: { xs: '8px', sm: '16px', lg: '24px' },
          overflowX: 'hidden',
        }}
      >
        {/* ヘッダーボタン（固定位置・右端） */}
        <Box
          sx={{
            position: 'fixed',
            top: { xs: '8px', sm: '16px' },
            right: { xs: '16px', sm: '40px' },
            display: 'flex',
            gap: { xs: '8px', sm: '12px' },
            zIndex: 1000,
          }}
        >
          {/* 保存ボタン */}
          <Button
            variant="contained"
            startIcon={<SaveIcon sx={{ fontSize: '20px' }} />}
            onClick={async () => {
              if (!data) return;

              try {
                // SajuDetailPageDataからSajuDetailResponseに必要なフィールドを抽出
                const dataToSave: any = {
                  id: data.id,
                  name: data.name,
                  birthDatetime: data.birthDatetime,
                  gender: data.gender,
                  yearStem: data.yearStem,
                  yearBranch: data.yearBranch,
                  monthStem: data.monthStem,
                  monthBranch: data.monthBranch,
                  dayStem: data.dayStem,
                  dayBranch: data.dayBranch,
                  hourStem: data.hourStem,
                  hourBranch: data.hourBranch,
                  daeunList: data.daeunList,
                  fortuneLevel: data.fortuneLevel,
                  createdAt: data.createdAt,
                  daeunNumber: data.daeunNumber,
                  isForward: data.isForward,
                  afterBirthYears: data.afterBirthYears,
                  afterBirthMonths: data.afterBirthMonths,
                  afterBirthDays: data.afterBirthDays,
                  firstDaeunDate: data.firstDaeunDate,
                  lifeGraphData: data.lifeGraph?.dataPoints || [],
                  tenganAnalysis: data.tenganAnalysis || {},
                  jijiAnalysis: data.jijiAnalysis || {},
                  interpretation: data.interpretation || '',
                };

                console.log('[SajuDetailPage] 保存データ:', dataToSave);

                const result = await saveSaju(dataToSave);
                if (result.success) {
                  alert(result.message);
                  // 保存後、リストページに戻る
                  navigate('/list');
                } else {
                  alert(result.message);
                }
              } catch (error) {
                console.error('保存エラー:', error);
                alert('保存中にエラーが発生しました');
              }
            }}
            sx={{
              backgroundColor: '#D4AF37',
              color: 'white',
              fontWeight: 600,
              fontSize: { xs: '16px', sm: '18px' },
              padding: { xs: '14px 24px', sm: '16px 28px' },
              minHeight: '48px',
              borderRadius: '8px',
              boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
              transition: 'all 0.2s',
              '&:hover': {
                backgroundColor: '#B8941C',
                transform: 'translateY(-1px)',
                boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
              },
            }}
          >
            保存
          </Button>

          {/* 閉じるボタン */}
          <IconButton
            onClick={() => navigate('/list')}
            sx={{
              backgroundColor: 'white',
              boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
              minWidth: '48px',
              minHeight: '48px',
              width: { xs: '48px', sm: '52px' },
              height: { xs: '48px', sm: '52px' },
              transition: 'all 0.2s',
              '&:hover': {
                backgroundColor: '#f5f5f5',
                transform: 'scale(1.05)',
              },
            }}
          >
            <CloseIcon sx={{ fontSize: '24px' }} />
          </IconButton>
        </Box>

        {/* 基本情報 */}
        <BasicInfoSection data={data} />

        {/* 四柱表示 */}
        <PillarsSection data={data} />

        {/* 人生グラフ */}
        <LifeGraphSection
          currentAge={data.currentAge}
          graphData={data.lifeGraph.dataPoints}
          daeunList={data.daeunList}
        />

        {/* 今日の運 */}
        {currentFortune && (
          <TodayFortuneSection
            currentYear={data.currentYear}
            currentMonth={data.currentMonth}
            currentDay={data.currentDay}
            yearFortune={{
              tengan: {
                char: currentFortune.yearFortune.stem,
                element: getStemElement(currentFortune.yearFortune.stem),
              },
              jishi: {
                char: currentFortune.yearFortune.branch,
                element: getBranchElement(currentFortune.yearFortune.branch),
              },
              fortuneLevel: FortuneLevelMap[currentFortune.yearFortune.fortuneLevel] ?? 3,
            }}
            monthFortune={{
              tengan: {
                char: currentFortune.monthFortune.stem,
                element: getStemElement(currentFortune.monthFortune.stem),
              },
              jishi: {
                char: currentFortune.monthFortune.branch,
                element: getBranchElement(currentFortune.monthFortune.branch),
              },
              fortuneLevel: FortuneLevelMap[currentFortune.monthFortune.fortuneLevel] ?? 3,
            }}
            dayFortune={{
              tengan: {
                char: currentFortune.dayFortune.stem,
                element: getStemElement(currentFortune.dayFortune.stem),
              },
              jishi: {
                char: currentFortune.dayFortune.branch,
                element: getBranchElement(currentFortune.dayFortune.branch),
              },
              fortuneLevel: FortuneLevelMap[currentFortune.dayFortune.fortuneLevel] ?? 3,
            }}
          />
        )}

        {/* 大運スクロールセクション */}
        <DaeunScrollSection
          daeunList={data.daeunList}
          selectedDaeunStartAge={selectedDaeunStartAge}
          onDaeunSelect={handleDaeunSelect}
          daeunNumber={data.daeunNumber || 0}
        />

        {/* 年運スクロールセクション（大運選択時のみ表示） */}
        {selectedDaeunStartAge !== null && (
          <YearFortuneScrollSection
            sajuId={data.id}
            daeunStartAge={selectedDaeunStartAge}
            selectedYear={selectedYear}
            onYearSelect={handleYearSelect}
          />
        )}

        {/* 月運スクロールセクション（年選択時のみ表示） */}
        {selectedYear !== null && (
          <MonthFortuneScrollSection
            sajuId={data.id}
            year={selectedYear}
            selectedMonth={selectedMonth}
            onMonthSelect={handleMonthSelect}
          />
        )}

        {/* 日運スクロールセクション（月選択時のみ表示） */}
        {selectedMonth !== null && selectedYear !== null && (
          <DayFortuneScrollSection
            sajuId={data.id}
            year={selectedYear}
            month={selectedMonth}
          />
        )}
      </Box>
    </MainLayout>
  );
};

export default SajuDetailPage;
