// モック認証サービス（開発用）
import type { AuthResponse, LoginRequest, RegisterRequest, User } from '../../../types';

// モックユーザーデータ
const MOCK_USERS = [
  {
    id: '1',
    email: 'demo@goldensaju.local',
    password: 'demo123',
    role: 'user' as const,
    permissions: ['read', 'write'],
    profile: { name: 'デモユーザー', avatar: '/avatars/user.png' },
  },
  {
    id: '2',
    email: 'admin@goldensaju.local',
    password: 'admin123',
    role: 'admin' as const,
    permissions: ['read', 'write', 'delete', 'admin'],
    profile: { name: '管理者', avatar: '/avatars/admin.png' },
  },
  {
    id: '3',
    email: 'test@goldensaju.local',
    password: 'TestGoldenSaju2025!',
    role: 'user' as const,
    permissions: ['read', 'write'],
    profile: { name: 'テスト太郎' },
  },
];

// トークン生成（簡易版）
const generateToken = (userId: string): string => {
  return btoa(`${userId}:${Date.now()}`);
};

// ユーザーデータからAuthResponseを生成
const createAuthResponse = (email: string, password: string): AuthResponse => {
  const user = MOCK_USERS.find((u) => u.email === email && u.password === password);
  if (!user) {
    throw new Error('Invalid email or password');
  }

  const { password: _, ...userWithoutPassword } = user;

  return {
    accessToken: generateToken(user.id),
    refreshToken: generateToken(`${user.id}-refresh`),
    user: {
      ...userWithoutPassword,
      createdAt: new Date().toISOString(),
    },
  };
};

export const mockAuthService = {
  /**
   * ログイン（モック）
   */
  async login(data: LoginRequest): Promise<AuthResponse> {
    // 実際のAPIを模倣した遅延
    await new Promise((resolve) => setTimeout(resolve, 800));

    try {
      return createAuthResponse(data.email, data.password);
    } catch (error) {
      throw new Error('メールアドレスまたはパスワードが正しくありません');
    }
  },

  /**
   * 新規登録（モック）
   */
  async register(data: RegisterRequest): Promise<AuthResponse> {
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // 既存ユーザーチェック
    if (MOCK_USERS.some((u) => u.email === data.email)) {
      throw new Error('このメールアドレスは既に登録されています');
    }

    // 新規ユーザー作成
    const newUser = {
      id: String(MOCK_USERS.length + 1),
      email: data.email,
      password: data.password,
      role: 'user' as const,
      permissions: ['read', 'write'],
      profile: { name: data.email.split('@')[0] },
    };

    MOCK_USERS.push(newUser);

    const { password, ...userWithoutPassword } = newUser;

    return {
      accessToken: generateToken(newUser.id),
      refreshToken: generateToken(`${newUser.id}-refresh`),
      user: {
        ...userWithoutPassword,
        createdAt: new Date().toISOString(),
      },
    };
  },

  /**
   * ログアウト（モック）
   */
  async logout(): Promise<void> {
    await new Promise((resolve) => setTimeout(resolve, 300));
    // モックなので何もしない
  },

  /**
   * 現在のユーザー情報取得（モック）
   */
  async getCurrentUser(accessToken: string): Promise<User> {
    await new Promise((resolve) => setTimeout(resolve, 300));

    // トークンからユーザーIDを取得（簡易版）
    const userId = atob(accessToken).split(':')[0];
    const user = MOCK_USERS.find((u) => u.id === userId);

    if (!user) {
      throw new Error('ユーザーが見つかりません');
    }

    const { password: _, ...userWithoutPassword } = user;

    return {
      ...userWithoutPassword,
      createdAt: new Date().toISOString(),
    };
  },
};

export default mockAuthService;
