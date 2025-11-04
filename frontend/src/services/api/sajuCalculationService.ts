/**
 * 命式計算・保存 実APIサービス
 *
 * エンドポイント:
 * - POST /api/saju/calculate: 命式計算（lunar-python + 210年節気DB）
 * - POST /api/saju/save: 命式保存
 */

import type { BirthDataRequest, SajuResponse, SaveResponse } from '../../types';
import { apiClient } from './client';

/**
 * 命式計算
 * POST /api/saju/calculate
 */
export async function calculateSaju(data: BirthDataRequest): Promise<SajuResponse> {
  const response = await apiClient.post<SajuResponse>('/api/saju/calculate', data);
  if (!response.data) {
    throw new Error('命式計算に失敗しました');
  }
  return response.data;
}

/**
 * 命式保存
 * POST /api/saju/save
 */
export async function saveSaju(data: SajuResponse): Promise<SaveResponse> {
  const response = await apiClient.post<SaveResponse>('/api/saju/save', data);
  if (!response.data) {
    throw new Error('命式保存に失敗しました');
  }
  return response.data;
}
