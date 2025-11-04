/**
 * 大運・年月日運API サービス
 *
 * 命式詳細ページでの大運・年運・月運・日運・現在の運勢の取得
 */

import { apiGet } from './client';
import type {
  DaeunAnalysisResponse,
  YearFortuneListResponse,
  MonthFortuneListResponse,
  DayFortuneListResponse,
  CurrentFortuneDetailResponse,
} from '../../types';

/**
 * 大運リスト取得
 * GET /api/saju/{id}/daeun
 */
export const getDaeunList = async (sajuId: string): Promise<DaeunAnalysisResponse> => {
  try {
    const response = await apiGet<DaeunAnalysisResponse>(`/api/saju/${sajuId}/daeun`);

    if (!response.data) {
      throw new Error('大運データの取得に失敗しました');
    }

    return response.data;
  } catch (error) {
    console.error('Failed to fetch daeun list:', error);
    throw new Error('大運情報の取得に失敗しました');
  }
};

/**
 * 年運リスト取得（大運期間の10年分）
 * GET /api/saju/{id}/year/{daeun_start_age}
 */
export const getYearFortuneList = async (
  sajuId: string,
  daeunStartAge: number
): Promise<YearFortuneListResponse> => {
  try {
    const response = await apiGet<YearFortuneListResponse>(
      `/api/saju/${sajuId}/year/${daeunStartAge}`
    );

    if (!response.data) {
      throw new Error('年運データの取得に失敗しました');
    }

    return response.data;
  } catch (error: any) {
    console.error('Failed to fetch year fortune list:', error);

    // ゲストモード: モックデータを生成
    if (error.status === 401 || error.status === 404 || error.status === 0) {
      const years = [];
      const currentYear = new Date().getFullYear();
      const currentAge = new Date().getFullYear() - (currentYear - daeunStartAge);

      // 天干・地支の配列
      const stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
      const branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
      const fortuneLevels: Array<'大吉' | '吉' | '平' | '凶' | '大凶'> = ['大吉', '吉', '平', '凶', '大凶'];
      const sipsinList = ['比肩', '劫財', '食神', '傷官', '偏財', '正財', '偏官', '正官', '偏印', '印綬'];

      for (let i = 0; i < 10; i++) {
        const age = daeunStartAge + i;
        const targetYear = currentYear - (currentAge - age);

        // 六十干支のインデックス計算（簡易版）
        const stemIndex = (targetYear + 6) % 10;
        const branchIndex = (targetYear + 8) % 12;

        years.push({
          id: i + 1,
          sajuId: sajuId,
          daeunStartAge: daeunStartAge,
          year: targetYear,
          age: age,
          yearStem: stems[stemIndex],
          yearBranch: branches[branchIndex],
          sipsin: sipsinList[i % sipsinList.length],
          fortuneLevel: fortuneLevels[i % fortuneLevels.length],
          isCurrent: age === currentAge,
        });
      }

      return {
        daeunStartAge: daeunStartAge,
        daeunEndAge: daeunStartAge + 9,
        years,
      };
    }

    throw new Error('年運情報の取得に失敗しました');
  }
};

/**
 * 月運リスト取得（指定年の12ヶ月）
 * GET /api/saju/{id}/month/{year}
 */
export const getMonthFortuneList = async (
  sajuId: string,
  year: number
): Promise<MonthFortuneListResponse> => {
  try {
    const response = await apiGet<MonthFortuneListResponse>(
      `/api/saju/${sajuId}/month/${year}`
    );

    if (!response.data) {
      throw new Error('月運データの取得に失敗しました');
    }

    return response.data;
  } catch (error: any) {
    console.error('Failed to fetch month fortune list:', error);

    // ゲストモード: モックデータを生成
    if (error.status === 401 || error.status === 404 || error.status === 0) {
      const months = [];
      const currentDate = new Date();
      const currentYear = currentDate.getFullYear();
      const currentMonth = currentDate.getMonth() + 1;

      // 天干・地支の配列
      const stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
      const fortuneLevels: Array<'大吉' | '吉' | '平' | '凶' | '大凶'> = ['大吉', '吉', '平', '凶', '大凶'];
      const sipsinList = ['比肩', '劫財', '食神', '傷官', '偏財', '正財', '偏官', '正官', '偏印', '印綬'];

      // 月支の配列（固定）
      const monthBranches = ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑'];

      for (let i = 1; i <= 12; i++) {
        // 年干から月干を計算（簡易版）
        const stemIndex = ((year * 2 + i - 2) % 10 + 10) % 10;

        months.push({
          id: i,
          sajuId: sajuId,
          year: year,
          month: i,
          monthStem: stems[stemIndex],
          monthBranch: monthBranches[i - 1],
          sipsin: sipsinList[i % sipsinList.length],
          fortuneLevel: fortuneLevels[i % fortuneLevels.length],
          isCurrent: year === currentYear && i === currentMonth,
        });
      }

      return { year, months };
    }

    throw new Error('月運情報の取得に失敗しました');
  }
};

/**
 * 日運リスト取得（指定月の日数分）
 * GET /api/saju/{id}/day/{year}/{month}
 */
export const getDayFortuneList = async (
  sajuId: string,
  year: number,
  month: number
): Promise<DayFortuneListResponse> => {
  try {
    const response = await apiGet<DayFortuneListResponse>(
      `/api/saju/${sajuId}/day/${year}/${month}`
    );

    if (!response.data) {
      throw new Error('日運データの取得に失敗しました');
    }

    return response.data;
  } catch (error: any) {
    console.error('Failed to fetch day fortune list:', error);

    // ゲストモード: モックデータを生成
    if (error.status === 401 || error.status === 404 || error.status === 0) {
      const daysInMonth = new Date(year, month, 0).getDate();
      const days = [];
      const currentDate = new Date();
      const currentYear = currentDate.getFullYear();
      const currentMonth = currentDate.getMonth() + 1;
      const currentDay = currentDate.getDate();

      // 天干・地支の配列
      const stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
      const branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
      const fortuneLevels: Array<'大吉' | '吉' | '平' | '凶' | '大凶'> = ['大吉', '吉', '平', '凶', '大凶'];
      const sipsinList = ['比肩', '劫財', '食神', '傷官', '偏財', '正財', '偏官', '正官', '偏印', '印綬'];

      for (let i = 1; i <= daysInMonth; i++) {
        // 日干支の計算（簡易版: 2000年1月1日を甲子として計算）
        const baseDate = new Date(2000, 0, 1); // 2000年1月1日
        const targetDate = new Date(year, month - 1, i);
        const daysDiff = Math.floor((targetDate.getTime() - baseDate.getTime()) / (1000 * 60 * 60 * 24));
        const stemIndex = (daysDiff % 10 + 10) % 10;
        const branchIndex = (daysDiff % 12 + 12) % 12;

        days.push({
          id: i,
          sajuId: sajuId,
          year: year,
          month: month,
          day: i,
          dayStem: stems[stemIndex],
          dayBranch: branches[branchIndex],
          sipsin: sipsinList[i % sipsinList.length],
          fortuneLevel: fortuneLevels[i % fortuneLevels.length],
          isToday: year === currentYear && month === currentMonth && i === currentDay,
        });
      }

      return { year, month, days };
    }

    throw new Error('日運情報の取得に失敗しました');
  }
};

/**
 * 現在の年月日運取得
 * GET /api/saju/{id}/current
 */
export const getCurrentFortune = async (
  sajuId: string
): Promise<CurrentFortuneDetailResponse> => {
  try {
    const response = await apiGet<CurrentFortuneDetailResponse>(
      `/api/saju/${sajuId}/current`
    );

    if (!response.data) {
      throw new Error('現在の運勢データの取得に失敗しました');
    }

    return response.data;
  } catch (error) {
    console.error('Failed to fetch current fortune:', error);
    throw new Error('現在の運勢情報の取得に失敗しました');
  }
};
