// ゴールデン四柱推命アプリケーション - 型定義
// バックエンドと完全同期する単一真実源

// ==================== ユーザー・認証関連 ====================

export interface User {
  id: string;
  email: string;
  role: 'guest' | 'user' | 'admin';
  permissions: string[];
  profile: {
    name: string;
    avatar?: string;
  };
  createdAt: string;
}

export interface AuthResponse {
  accessToken: string;
  refreshToken: string;
  user: User;
}

export interface LoginRequest {
  email: string;
  password: string;
  rememberMe?: boolean;
}

export interface RegisterRequest {
  email: string;
  password: string;
  migrateGuestData?: boolean;
}

// ==================== 命式データ関連 ====================

export interface BirthDataRequest {
  birthDatetime: string; // ISO 8601 format
  gender: 'male' | 'female';
  name?: string;
  timezoneOffset?: number; // KST = 9
}

export interface SajuResponse {
  id: string;
  name?: string;
  birthDatetime: string;
  gender: string;
  yearStem: string;
  yearBranch: string;
  monthStem: string;
  monthBranch: string;
  dayStem: string;
  dayBranch: string;
  hourStem: string;
  hourBranch: string;
  daeunList: DaeunInfo[];
  fortuneLevel: FortuneLevel;
  createdAt: string;
}

export interface DaeunInfo {
  id: number;
  sajuId: string;
  startAge: number;
  endAge: number;
  daeunStem: string;
  daeunBranch: string;
  fortuneLevel: FortuneLevel;
}

export type FortuneLevel = '大吉' | '吉' | '平' | '凶' | '大凶';

export interface GraphDataPoint {
  age: number;
  fortuneLevel: number; // 1-5
  daeunStem: string;
  daeunBranch: string;
  label: string; // "8-17歳: 甲子"
}

export interface SajuDetailResponse extends SajuResponse {
  lifeGraphData: GraphDataPoint[];
  tenganAnalysis: Record<string, string>;
  jijiAnalysis: Record<string, string>;
  interpretation: string;
}

export interface CurrentFortuneResponse {
  yearStem: string;
  yearBranch: string;
  yearFortuneLevel: FortuneLevel;
  monthStem: string;
  monthBranch: string;
  monthFortuneLevel: FortuneLevel;
  dayStem: string;
  dayBranch: string;
  dayFortuneLevel: FortuneLevel;
  currentDate: string;
}

// ==================== API応答関連 ====================

export interface ApiError {
  message: string;
  code: string;
  details?: Record<string, any>;
}

export interface SaveResponse {
  success: boolean;
  id: string;
  message: string;
}

export interface DeleteResponse {
  success: boolean;
  message: string;
}

export interface MigrateResponse {
  success: boolean;
  migratedCount: number;
  message: string;
}

export interface SajuSummary {
  id: string;
  name?: string;
  birthDatetime: string;
  gender: string;
  fortuneLevel: FortuneLevel;
  createdAt: string;
}

// ==================== ローカルストレージ用型 ====================

export interface LocalStorageSaju {
  id: string;
  data: SajuResponse;
  createdAt: string;
}

// ==================== コンポーネントProps型 ====================

export interface LayoutProps {
  children: React.ReactNode;
  maxWidth?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
}

export interface ProtectedRouteProps {
  children: React.ReactNode;
  roles?: Array<'guest' | 'user' | 'admin'>;
}
