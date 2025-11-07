/**
 * 命式管理 API Service
 * スライス3: 命式リスト・詳細・削除のAPI統合
 *
 * エンドポイント:
 * - GET /api/saju/list - 命式一覧取得
 * - GET /api/saju/{id} - 命式詳細取得
 * - DELETE /api/saju/{id} - 命式削除
 */

import { apiGet, apiDelete } from './client';
import type {
  SajuSummary,
  SajuDetailPageData,
  SajuDetailResponse,
  DeleteResponse,
  CurrentFortuneResponse
} from '../../types';
import { FortuneLevelMap } from '../../types';
import { getStemElement, getBranchElement } from '../../utils/sajuHelpers';

/**
 * ページネーションレスポンス型
 */
interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  hasNext: boolean;
}

/**
 * 命式一覧取得
 * @returns 命式サマリーの配列
 * @throws ApiError
 */
export async function getSajuList(): Promise<SajuSummary[]> {
  // まずLocalStorageから取得を試みる（ゲストモード優先）
  const localData = localStorage.getItem('saju_data');

  if (localData) {
    try {
      const sajuList: SajuSummary[] = JSON.parse(localData);
      console.log('[getSajuList] LocalStorageから取得:', sajuList.length, '件');
      return sajuList;
    } catch (parseError) {
      console.error('[getSajuList] LocalStorageのパースに失敗:', parseError);
      // パースエラーの場合、LocalStorageをクリアして続行
      localStorage.removeItem('saju_data');
    }
  }

  // LocalStorageにデータがない場合、APIから取得を試みる（ログインユーザー用）
  try {
    const response = await apiGet<PaginatedResponse<SajuSummary>>('/api/saju/list');

    if (!response.data) {
      throw new Error('命式一覧の取得に失敗しました');
    }

    console.log('[getSajuList] APIから取得:', response.data.items.length, '件');
    // ページネーション形式から items を抽出
    return response.data.items;
  } catch (error: any) {
    console.error('[getSajuList] API取得エラー:', error);
    // APIエラーの場合は空配列を返す（LocalStorageも空だった場合）
    return [];
  }
}

/**
 * 命式詳細取得
 * @param id - 命式ID
 * @returns 命式詳細データ
 * @throws ApiError
 */
export async function getSajuDetail(id: string): Promise<SajuDetailPageData> {
  let sajuData: SajuDetailResponse;

  try {
    // まずAPIから取得を試みる（ログインユーザー用）
    const response = await apiGet<SajuDetailResponse>(`/api/saju/${id}`);

    if (!response.data) {
      throw new Error('命式詳細の取得に失敗しました');
    }

    sajuData = response.data;
  } catch (error: any) {
    // 401 または 404の場合、LocalStorageから取得を試みる（ゲストユーザー用）
    if (error.status === 401 || error.status === 404 || error.status === 0) {
      const localData = localStorage.getItem('saju_data');

      if (!localData) {
        throw new Error('命式データが見つかりません');
      }

      const sajuList: SajuDetailResponse[] = JSON.parse(localData);
      const found = sajuList.find(item => item.id === id);

      if (!found) {
        throw new Error('指定された命式IDが見つかりません');
      }

      sajuData = found;
    } else {
      // その他のエラーは再スロー
      throw error;
    }
  }

  // 現在の年齢を計算
  const birthDate = new Date(sajuData.birthDatetime);
  const today = new Date();
  const currentAge = today.getFullYear() - birthDate.getFullYear();

  // 人生グラフデータを生成（大運リストから）
  // 各大運の開始年齢と終了年齢の両方にデータポイントを作成（階段状グラフのため）
  const graphDataPoints = [];

  if (sajuData.daeunList && sajuData.daeunList.length > 0) {
    for (let i = 0; i < sajuData.daeunList.length; i++) {
      const daeun = sajuData.daeunList[i];
      const fortuneNumber = FortuneLevelMap[daeun.fortuneLevel];

      // 大運の開始年齢にデータポイントを追加
      graphDataPoints.push({
        age: daeun.startAge,
        fortuneLevel: fortuneNumber,
        daeunStem: daeun.daeunStem,
        daeunBranch: daeun.daeunBranch,
        label: `${daeun.startAge}-${daeun.endAge}歳: ${daeun.daeunStem}${daeun.daeunBranch}`
      });

      // 大運の終了年齢にもデータポイントを追加（階段状グラフのため）
      graphDataPoints.push({
        age: daeun.endAge,
        fortuneLevel: fortuneNumber,
        daeunStem: daeun.daeunStem,
        daeunBranch: daeun.daeunBranch,
        label: `${daeun.startAge}-${daeun.endAge}歳: ${daeun.daeunStem}${daeun.daeunBranch}`
      });
    }
  }

  // 四柱データを生成（モックアップに合わせた構造）
  const pillars = [
    {
      type: '年柱' as const,
      stem: sajuData.yearStem,
      branch: sajuData.yearBranch,
      stemElement: getStemElement(sajuData.yearStem),
      branchElement: getBranchElement(sajuData.yearBranch)
    },
    {
      type: '月柱' as const,
      stem: sajuData.monthStem,
      branch: sajuData.monthBranch,
      stemElement: getStemElement(sajuData.monthStem),
      branchElement: getBranchElement(sajuData.monthBranch)
    },
    {
      type: '日柱' as const,
      stem: sajuData.dayStem,
      branch: sajuData.dayBranch,
      stemElement: getStemElement(sajuData.dayStem),
      branchElement: getBranchElement(sajuData.dayBranch)
    },
    {
      type: '時柱' as const,
      stem: sajuData.hourStem,
      branch: sajuData.hourBranch,
      stemElement: getStemElement(sajuData.hourStem),
      branchElement: getBranchElement(sajuData.hourBranch)
    }
  ];

  // SajuDetailPageData型に変換
  const pageData: SajuDetailPageData = {
    ...sajuData,
    pillars,
    daeunAnalysis: {
      daeunNumber: sajuData.daeunNumber || 7,
      isForward: sajuData.isForward ?? true,
      afterBirth: {
        years: sajuData.afterBirthYears || 0,
        months: sajuData.afterBirthMonths || 0,
        days: sajuData.afterBirthDays || 0,
      },
      firstDaeunDate: sajuData.firstDaeunDate || '',
      currentAge: currentAge,
      daeunList: sajuData.daeunList || []
    },
    currentFortune: {
      date: today.toISOString().split('T')[0],
      yearFortune: {
        stem: sajuData.yearStem,
        branch: sajuData.yearBranch,
        fortuneLevel: sajuData.fortuneLevel || '平',
        description: '年運',
        element: getStemElement(sajuData.yearStem)
      },
      monthFortune: {
        stem: sajuData.monthStem,
        branch: sajuData.monthBranch,
        fortuneLevel: sajuData.fortuneLevel || '平',
        description: '月運',
        element: getStemElement(sajuData.monthStem)
      },
      dayFortune: {
        stem: sajuData.dayStem,
        branch: sajuData.dayBranch,
        fortuneLevel: sajuData.fortuneLevel || '平',
        description: '日運',
        element: getStemElement(sajuData.dayStem)
      }
    },
    lifeGraph: {
      dataPoints: graphDataPoints,
      currentAge: currentAge,
      maxAge: 100,
      minFortuneLevel: 1,
      maxFortuneLevel: 5,
    },
    currentAge: currentAge,
    currentYear: today.getFullYear(),
    currentMonth: today.getMonth() + 1,
    currentDay: today.getDate(),
  };

  return pageData;
}

/**
 * 命式削除
 * @param id - 命式ID
 * @returns 削除結果
 * @throws ApiError
 */
export async function deleteSaju(id: string): Promise<DeleteResponse> {
  // まずLocalStorageから削除を試みる（ゲストモード優先）
  const localData = localStorage.getItem('saju_data');

  if (localData) {
    try {
      const sajuList: SajuSummary[] = JSON.parse(localData);
      const filteredList = sajuList.filter(item => item.id !== id);

      console.log('[deleteSaju] 削除前:', sajuList.length, '件');
      console.log('[deleteSaju] 削除後:', filteredList.length, '件');
      console.log('[deleteSaju] 削除ID:', id);

      // LocalStorageを更新
      if (filteredList.length > 0) {
        localStorage.setItem('saju_data', JSON.stringify(filteredList));
      } else {
        localStorage.removeItem('saju_data'); // 空になった場合は削除
      }

      return {
        success: true,
        message: '命式を削除しました',
      };
    } catch (parseError) {
      console.error('[deleteSaju] LocalStorageのパースに失敗:', parseError);
      // パースエラーの場合、LocalStorageをクリアして続行
      localStorage.removeItem('saju_data');
    }
  }

  // LocalStorageにデータがない場合、APIから削除を試みる（ログインユーザー用）
  try {
    const response = await apiDelete<DeleteResponse>(`/api/saju/${id}`);

    if (!response.data) {
      throw new Error('命式の削除に失敗しました');
    }

    console.log('[deleteSaju] APIから削除成功');
    return response.data;
  } catch (error: any) {
    console.error('[deleteSaju] API削除エラー:', error);
    // APIエラーでもLocalStorageから削除できていればOK
    return {
      success: true,
      message: '命式を削除しました',
    };
  }
}

/**
 * 今日の運勢を取得
 * @returns 今日の年運・月運・日運
 * @throws ApiError
 */
export async function getCurrentFortune(): Promise<CurrentFortuneResponse> {
  const response = await apiGet<CurrentFortuneResponse>('/api/saju/current-fortune');

  if (!response.data) {
    throw new Error('今日の運勢の取得に失敗しました');
  }

  return response.data;
}

/**
 * 命式を保存（LocalStorageまたはAPI）
 * @param data - 保存する命式データ
 * @returns 保存結果
 */
export async function saveSaju(data: SajuDetailResponse): Promise<{ success: boolean; message: string }> {
  try {
    // LocalStorageから既存データを取得
    const localData = localStorage.getItem('saju_data');
    let sajuList: SajuDetailResponse[] = localData ? JSON.parse(localData) : [];

    console.log('[saveSaju] 保存前のLocalStorage:', sajuList.length, '件');

    // 既存データに追加日時とIDがない場合は生成
    const sajuToSave: SajuDetailResponse = {
      ...data,
      id: data.id || `saju-${Date.now()}`,
      createdAt: data.createdAt || new Date().toISOString(),
    };

    console.log('[saveSaju] 保存データID:', sajuToSave.id);

    // 同じIDが既に存在する場合は更新、なければ追加
    const existingIndex = sajuList.findIndex(item => item.id === sajuToSave.id);
    if (existingIndex >= 0) {
      sajuList[existingIndex] = sajuToSave;
      console.log('[saveSaju] 既存データを更新:', sajuToSave.id);
    } else {
      sajuList.push(sajuToSave);
      console.log('[saveSaju] 新規データを追加:', sajuToSave.id);
    }

    // LocalStorageに保存
    localStorage.setItem('saju_data', JSON.stringify(sajuList));
    console.log('[saveSaju] 保存後のLocalStorage:', sajuList.length, '件');

    return { success: true, message: '命式を保存しました' };
  } catch (error: any) {
    console.error('[saveSaju] 保存エラー:', error);
    return { success: false, message: '命式の保存に失敗しました' };
  }
}
