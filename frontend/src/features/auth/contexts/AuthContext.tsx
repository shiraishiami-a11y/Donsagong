// 認証コンテキスト
import React, { createContext, useState, useEffect, useCallback } from 'react';
import type { User, AuthResponse, LoginRequest, RegisterRequest } from '../../../types';
import { mockAuthService } from '../services/mockAuthService';

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

  // 初期化時にトークンから現在のユーザー情報を復元
  useEffect(() => {
    const initializeAuth = async () => {
      const accessToken = localStorage.getItem('accessToken');
      if (accessToken) {
        try {
          const currentUser = await mockAuthService.getCurrentUser(accessToken);
          setUser(currentUser);
        } catch (error) {
          // トークンが無効な場合はクリア
          localStorage.removeItem('accessToken');
          localStorage.removeItem('refreshToken');
        }
      }
      setIsLoading(false);
    };

    initializeAuth();
  }, []);

  /**
   * ログイン
   */
  const login = useCallback(async (data: LoginRequest) => {
    try {
      const response: AuthResponse = await mockAuthService.login(data);

      // トークンをローカルストレージに保存
      localStorage.setItem('accessToken', response.accessToken);
      localStorage.setItem('refreshToken', response.refreshToken);

      // ユーザー情報を設定
      setUser(response.user);
    } catch (error) {
      throw error;
    }
  }, []);

  /**
   * 新規登録
   */
  const register = useCallback(async (data: RegisterRequest) => {
    try {
      const response: AuthResponse = await mockAuthService.register(data);

      // トークンをローカルストレージに保存
      localStorage.setItem('accessToken', response.accessToken);
      localStorage.setItem('refreshToken', response.refreshToken);

      // ユーザー情報を設定
      setUser(response.user);

      // ゲストデータ移行（オプション）
      if (data.migrateGuestData) {
        // TODO: 将来実装
        console.log('ゲストデータ移行処理をここに実装');
      }
    } catch (error) {
      throw error;
    }
  }, []);

  /**
   * ログアウト
   */
  const logout = useCallback(async () => {
    try {
      await mockAuthService.logout();

      // トークンとユーザー情報をクリア
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      setUser(null);
    } catch (error) {
      // ログアウトは失敗してもクリア
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      setUser(null);
    }
  }, []);

  /**
   * ユーザー情報を再取得
   */
  const refreshUser = useCallback(async () => {
    const accessToken = localStorage.getItem('accessToken');
    if (accessToken) {
      try {
        const currentUser = await mockAuthService.getCurrentUser(accessToken);
        setUser(currentUser);
      } catch (error) {
        setUser(null);
      }
    }
  }, []);

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
