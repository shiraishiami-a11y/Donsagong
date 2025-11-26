// sajuUpdateService - 命式更新APIサービス
import type { SajuUpdateRequest, SajuResponse } from '../../types';
import { apiClient, ApiError } from './client';

/**
 * 命式を更新する
 * PUT /api/saju/{id}
 *
 * 生年月日時・性別が変更された場合は四柱推命を自動で再計算
 * 認証必須、自分の命式のみ更新可能
 */
export const updateSaju = async (id: string, data: SajuUpdateRequest): Promise<SajuResponse> => {
  try {
    const response = await apiClient.put<SajuResponse>(`/api/saju/${id}`, data);

    if (!response.data) {
      throw new Error('命式更新に失敗しました');
    }

    return response.data;
  } catch (error) {
    // APIエラーの場合、詳細なエラーメッセージを提供
    if (error instanceof ApiError) {
      // 権限エラー
      if (error.status === 403) {
        throw new Error('この命式にアクセスする権限がありません');
      }
      // 見つからないエラー
      if (error.status === 404) {
        throw new Error('指定された命式が見つかりません');
      }
      // バリデーションエラー
      if (error.status === 400) {
        throw new Error(`入力データが正しくありません: ${error.detail || error.message}`);
      }
      // その他のAPIエラー
      throw new Error(error.message);
    }

    // ネットワークエラーなど
    throw new Error('命式の更新中にエラーが発生しました');
  }
};
