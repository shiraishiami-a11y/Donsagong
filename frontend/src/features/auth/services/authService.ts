/**
 * 認証サービス（実API版）
 * バックエンドAPI統合完了後の本番サービス
 * プロジェクト標準のapiClient（fetch-based）を使用
 */
import { apiClient } from '../../../services/api/client';
import type { AuthResponse, LoginRequest, RegisterRequest, User } from '../../../types';

export const authService = {
  /**
   * POST /api/auth/login
   * ログイン処理
   */
  async login(data: LoginRequest): Promise<AuthResponse> {
    console.log('[authService] login called', { email: data.email });
    console.log('[authService] Sending POST /api/auth/login');

    const response = await apiClient.post<AuthResponse>('/api/auth/login', data);
    console.log('[authService] Response received', { status: response.status });

    if (!response.data) {
      throw new Error('ログインに失敗しました');
    }

    // トークンをLocalStorageに保存（apiClientのgetAuthTokenで使用）
    localStorage.setItem('auth', JSON.stringify({
      token: response.data.accessToken,
      refreshToken: response.data.refreshToken,
      user: response.data.user,
    }));

    console.log('[authService] Login success, token saved');
    return response.data;
  },

  /**
   * POST /api/auth/register
   * 新規登録処理
   */
  async register(data: RegisterRequest): Promise<AuthResponse> {
    console.log('[authService] register called', { email: data.email });
    console.log('[authService] Sending POST /api/auth/register');

    const response = await apiClient.post<AuthResponse>('/api/auth/register', data);
    console.log('[authService] Response received', { status: response.status });

    if (!response.data) {
      throw new Error('登録に失敗しました');
    }

    // トークンをLocalStorageに保存
    localStorage.setItem('auth', JSON.stringify({
      token: response.data.accessToken,
      refreshToken: response.data.refreshToken,
      user: response.data.user,
    }));

    console.log('[authService] Register success, token saved');
    return response.data;
  },

  /**
   * POST /api/auth/logout
   * ログアウト処理
   */
  async logout(): Promise<void> {
    try {
      await apiClient.post('/api/auth/logout');
    } finally {
      // APIエラーでもLocalStorageはクリア
      localStorage.removeItem('auth');
    }
  },

  /**
   * GET /api/auth/me
   * 現在のユーザー情報取得
   */
  async getCurrentUser(): Promise<User> {
    const response = await apiClient.get<User>('/api/auth/me');

    if (!response.data) {
      throw new Error('ユーザー情報の取得に失敗しました');
    }

    return response.data;
  },
};

export default authService;
