/**
 * 設定関連 APIサービス
 *
 * バックエンドAPI統合版
 * - パスワード変更: PUT /api/user/password
 * - データエクスポート: GET /api/saju/export
 * - データインポート: POST /api/saju/import
 * - ユーザー設定更新: PUT /api/user/settings
 */

import { apiPut } from './client';
import type { UpdateResponse, ImportResponse, UserSettings } from '../../types';

/**
 * パスワード変更
 * PUT /api/user/password
 */
export async function changePassword(
  oldPassword: string,
  newPassword: string
): Promise<UpdateResponse> {
  const response = await apiPut<UpdateResponse>('/api/user/password', {
    old_password: oldPassword,
    new_password: newPassword,
  });

  return response.data!;
}

/**
 * データエクスポート
 * GET /api/saju/export
 *
 * 注: バックエンドからJSON形式でダウンロードします
 */
export async function exportData(): Promise<Blob> {
  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8432';
  const token = getAuthToken();

  const headers: HeadersInit = {
    ...(token && { Authorization: `Bearer ${token}` }),
  };

  const response = await fetch(`${API_BASE_URL}/api/saju/export`, {
    method: 'GET',
    headers,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || error.message || 'エクスポートに失敗しました');
  }

  // Blobとして返す
  return await response.blob();
}

/**
 * データインポート
 * POST /api/saju/import
 *
 * multipart/form-data形式でファイルをアップロード
 */
export async function importData(file: File): Promise<ImportResponse> {
  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8432';
  const token = getAuthToken();

  const formData = new FormData();
  formData.append('file', file);

  const headers: HeadersInit = {
    ...(token && { Authorization: `Bearer ${token}` }),
    // Content-Typeはブラウザが自動設定するため省略
  };

  const response = await fetch(`${API_BASE_URL}/api/saju/import`, {
    method: 'POST',
    headers,
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || error.message || 'インポートに失敗しました');
  }

  const data = await response.json();
  return data;
}

/**
 * ユーザー設定更新
 * PUT /api/user/settings
 */
export async function updateUserSettings(settings: UserSettings): Promise<UpdateResponse> {
  // LocalStorageに保存
  localStorage.setItem('userSettings', JSON.stringify(settings));

  const response = await apiPut<UpdateResponse>('/api/user/settings', {
    remember_me: settings.rememberMe,
    session_duration: settings.sessionDuration,
  });

  return response.data!;
}

/**
 * ユーザー設定を取得
 * LocalStorageから読み込み（クライアント側のみ）
 */
export function getUserSettings(): UserSettings {
  const settingsData = localStorage.getItem('userSettings');
  if (!settingsData) {
    // デフォルト設定
    return {
      rememberMe: true,
      sessionDuration: '30d',
    };
  }

  try {
    return JSON.parse(settingsData);
  } catch {
    return {
      rememberMe: true,
      sessionDuration: '30d',
    };
  }
}

/**
 * ログアウト
 * LocalStorageの認証情報をクリア
 */
export function logout(): void {
  localStorage.removeItem('auth');
  // ユーザー設定は保持
}

/**
 * LocalStorageから認証トークンを取得（ヘルパー関数）
 */
function getAuthToken(): string | null {
  const authData = localStorage.getItem('auth');
  if (!authData) return null;

  try {
    const parsed = JSON.parse(authData);
    return parsed.token || null;
  } catch {
    return null;
  }
}
