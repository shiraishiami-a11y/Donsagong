// 認証コンテキスト
import React, { createContext, useState, useEffect, useCallback } from 'react';
import type { User, AuthResponse, LoginRequest, RegisterRequest } from '../../../types';
import { authService } from '../services/authService';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (data: LoginRequest) => Promise<void>;
  register: (data: RegisterRequest) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // E2Eテスト用: 認証スキップモード
  // ⚠️ 警告: 本番環境では絶対にVITE_SKIP_AUTHを設定しないこと
  // .env.localに設定されていない場合はundefinedとなり、skipAuthはfalseになります
  const skipAuth = import.meta.env.VITE_SKIP_AUTH === 'true';

  // 初期化時にトークンから現在のユーザー情報を復元
  useEffect(() => {
    const initializeAuth = async () => {
      // E2Eテスト用: 認証スキップモード
      if (skipAuth) {
        // ダミーユーザーを設定
        setUser({
          id: 'test-user-id',
          email: 'test@e2e.local',
          role: 'guest',
          permissions: [],
          profile: {
            name: 'E2Eテストユーザー',
          },
          createdAt: new Date().toISOString(),
        } as User);
        setIsLoading(false);
        return;
      }

      const authData = localStorage.getItem('auth');
      if (authData) {
        try {
          const currentUser = await authService.getCurrentUser();
          setUser(currentUser);
        } catch (error) {
          // トークンが無効な場合はクリア
          localStorage.removeItem('auth');
        }
      }
      setIsLoading(false);
    };

    initializeAuth();
  }, [skipAuth]);

  /**
   * ログイン
   */
  const login = useCallback(async (data: LoginRequest) => {
    console.log('[AuthContext] login called', { email: data.email });

    // E2Eテスト用: 認証スキップモード
    if (skipAuth) {
      console.log('[AuthContext] Skipping auth (E2E mode)');
      return;
    }

    console.log('[AuthContext] Calling authService.login...');
    try {
      const response: AuthResponse = await authService.login(data);
      console.log('[AuthContext] Login response received');

      // ユーザー情報を設定（トークンはauthService内で保存済み）
      setUser(response.user);
    } catch (error) {
      console.error('[AuthContext] Login error:', error);
      throw error;
    }
  }, [skipAuth]);

  /**
   * 新規登録
   */
  const register = useCallback(async (data: RegisterRequest) => {
    // E2Eテスト用: 認証スキップモード
    if (skipAuth) {
      return;
    }

    console.log('[AuthContext] register called', { email: data.email, migrateGuestData: data.migrateGuestData });

    try {
      // 新規登録API呼び出し
      console.log('[AuthContext] Calling authService.register...');
      const response: AuthResponse = await authService.register(data);
      console.log('[AuthContext] Register response received');

      // ユーザー情報を設定（トークンはauthService内で保存済み）
      setUser(response.user);

      // ゲストデータ移行処理
      if (data.migrateGuestData) {
        console.log('[AuthContext] Starting guest data migration...');

        // LocalStorageからゲストデータを取得
        const guestDataStr = localStorage.getItem('saju_data');
        if (guestDataStr) {
          try {
            const guestData = JSON.parse(guestDataStr);

            if (guestData && Array.isArray(guestData) && guestData.length > 0) {
              console.log(`[AuthContext] Found ${guestData.length} guest saju data`);

              // データ移行API呼び出し
              const migrateResponse = await fetch(`${import.meta.env.VITE_API_URL}/api/saju/migrate`, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${response.accessToken}`,
                },
                body: JSON.stringify({ guestData }),
              });

              if (!migrateResponse.ok) {
                throw new Error(`Migration API failed: ${migrateResponse.status}`);
              }

              const migrateResult = await migrateResponse.json();
              console.log('[AuthContext] Migration success:', migrateResult);

              // 移行成功後、LocalStorageをクリア
              localStorage.removeItem('saju_data');
              console.log('[AuthContext] Guest data cleared from LocalStorage');
            } else {
              console.log('[AuthContext] No guest data found in LocalStorage');
            }
          } catch (error) {
            console.error('[AuthContext] Migration error:', error);
            // 移行エラーは登録成功を妨げない（データはLocalStorageに残る）
          }
        } else {
          console.log('[AuthContext] No saju_data in LocalStorage');
        }
      }
    } catch (error) {
      console.error('[AuthContext] Register error:', error);
      throw error;
    }
  }, [skipAuth]);

  /**
   * ログアウト
   */
  const logout = useCallback(async () => {
    // E2Eテスト用: 認証スキップモード
    if (skipAuth) {
      return;
    }

    try {
      await authService.logout();

      // ユーザー情報をクリア（トークンはauthService内でクリア済み）
      setUser(null);
    } catch (error) {
      // ログアウトは失敗してもクリア
      setUser(null);
    }
  }, [skipAuth]);

  /**
   * ユーザー情報を再取得
   */
  const refreshUser = useCallback(async () => {
    // E2Eテスト用: 認証スキップモード
    if (skipAuth) {
      return;
    }

    const authData = localStorage.getItem('auth');
    if (authData) {
      try {
        const currentUser = await authService.getCurrentUser();
        setUser(currentUser);
      } catch (error) {
        setUser(null);
      }
    }
  }, [skipAuth]);

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    register,
    logout,
    refreshUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthProvider;
