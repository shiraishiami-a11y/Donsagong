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
  name: string; // プロフィール名
  migrateGuestData?: boolean;
  guestData?: SajuResponse[];
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
  // 大運計算情報
  daeunNumber?: number; // 大運数（例：7）
  isForward?: boolean; // 順行（true）/逆行（false）
  afterBirthYears?: number; // 生後年数
  afterBirthMonths?: number; // 生後月数
  afterBirthDays?: number; // 生後日数
  firstDaeunDate?: string; // 第一大運開始日
}

export interface DaeunInfo {
  id: number;
  sajuId: string;
  startAge: number;
  endAge: number;
  daeunStem: string;
  daeunBranch: string;
  fortuneLevel: FortuneLevel;
  sipsin?: string; // 十神 (正官、偏財、食神、比肩、偏印など)
  isCurrent?: boolean; // 現在の大運期間かどうか
}

export type FortuneLevel = '大吉' | '小吉' | '吉' | '吉凶' | '平' | '凶' | '大凶';

// 吉凶レベルの数値マッピング
export const FortuneLevelMap: Record<FortuneLevel, number> = {
  '大吉': 5,
  '小吉': 4,
  '吉': 4,
  '吉凶': 3,
  '平': 3,
  '凶': 2,
  '大凶': 1
};

// 逆マッピング（数値から吉凶レベル）
export const FortuneLevelReverseMap: Record<number, FortuneLevel> = {
  5: '大吉',
  4: '吉',
  3: '平',
  2: '凶',
  1: '大凶'
};

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

export interface FortuneDetail {
  stem: string;
  branch: string;
  fortuneLevel: FortuneLevel;
  description: string;
  element?: FiveElement | null;
}

export interface CurrentFortuneResponse {
  date: string;
  yearFortune: FortuneDetail;
  monthFortune: FortuneDetail;
  dayFortune: FortuneDetail;
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
  // 四柱プレビュー用
  yearStem: string;
  yearBranch: string;
  monthStem: string;
  monthBranch: string;
  dayStem: string;
  dayBranch: string;
  hourStem: string;
  hourBranch: string;
}

// ==================== ローカルストレージ用型 ====================

export interface LocalStorageSaju {
  id: string;
  data: SajuResponse;
  createdAt: string;
}

// ==================== P-003: 命式詳細ページ用型 ====================

// 五行要素タイプ
export type FiveElement = 'wood' | 'fire' | 'earth' | 'metal' | 'water';

// 四柱（柱）の型
export interface Pillar {
  type: '年柱' | '月柱' | '日柱' | '時柱';
  stem: string; // 天干
  branch: string; // 地支
  stemElement?: FiveElement; // 天干の五行
  branchElement?: FiveElement; // 地支の五行
}

// 大運分析応答
export interface DaeunAnalysisResponse {
  daeunNumber: number; // 大運数
  isForward: boolean; // 順行/逆行
  afterBirth: {
    years: number;
    months: number;
    days: number;
  };
  firstDaeunDate: string; // 第一大運開始日
  currentAge: number; // 現在年齢
  daeunList: DaeunInfo[];
}

// 年運情報（水平スクロール用）
export interface YearFortuneInfo {
  id: number;
  sajuId: string;
  daeunStartAge: number; // この年運が属する大運の開始年齢
  year: number; // 西暦年
  age: number; // その年の年齢
  yearStem: string; // 年天干
  yearBranch: string; // 年地支
  sipsin: string; // 十神
  fortuneLevel: FortuneLevel; // 吉凶レベル
  isCurrent: boolean; // 現在の年かどうか
}

// 月運情報（水平スクロール用）
export interface MonthFortuneInfo {
  id: number;
  sajuId: string;
  year: number; // 所属する年
  month: number; // 月(1-12)
  monthStem: string; // 月天干
  monthBranch: string; // 月地支
  sipsin: string; // 十神
  fortuneLevel: FortuneLevel; // 吉凶レベル
  isCurrent: boolean; // 現在の月かどうか
}

// 日運情報（水平スクロール用）
export interface DayFortuneInfo {
  id: number;
  sajuId: string;
  year: number; // 所属する年
  month: number; // 所属する月
  day: number; // 日(1-31)
  dayStem: string; // 日天干
  dayBranch: string; // 日地支
  sipsin: string; // 十神
  fortuneLevel: FortuneLevel; // 吉凶レベル
  isToday: boolean; // 今日かどうか
}

// 年運リスト取得レスポンス
export interface YearFortuneListResponse {
  daeunStartAge: number;
  daeunEndAge: number;
  years: YearFortuneInfo[];
}

// 月運リスト取得レスポンス
export interface MonthFortuneListResponse {
  year: number;
  months: MonthFortuneInfo[];
}

// 日運リスト取得レスポンス
export interface DayFortuneListResponse {
  year: number;
  month: number;
  days: DayFortuneInfo[];
}

// 現在の運勢詳細応答（拡張版）
export interface CurrentFortuneDetailResponse {
  date: string; // 対象日付
  yearFortune: FortuneDetail;
  monthFortune: FortuneDetail;
  dayFortune: FortuneDetail;
  hourFortune?: FortuneDetail; // 時運（オプション）
}

// 人生グラフ用データ（拡張版）
export interface LifeGraphData {
  dataPoints: GraphDataPoint[];
  currentAge: number;
  maxAge: number; // 表示する最大年齢（通常100歳）
  minFortuneLevel: number; // 最小吉凶レベル（1）
  maxFortuneLevel: number; // 最大吉凶レベル（5）
  averageFortuneLevel?: number; // 平均吉凶レベル
}

// 命式詳細ページ用の完全データ型
export interface SajuDetailPageData extends SajuDetailResponse {
  pillars: Pillar[]; // 四柱配列
  daeunAnalysis: DaeunAnalysisResponse; // 大運分析
  currentFortune: CurrentFortuneDetailResponse; // 現在の運勢
  lifeGraph: LifeGraphData; // 人生グラフデータ
  currentAge: number; // 現在の年齢
  currentYear: number; // 現在の年
  currentMonth: number; // 現在の月
  currentDay: number; // 現在の日
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

// ==================== P-004: 設定ページ用型 ====================

export interface UpdateResponse {
  success: boolean;
  message: string;
}

export interface ImportResponse {
  success: boolean;
  importedCount: number;
  message: string;
}

export interface UserSettings {
  rememberMe: boolean;
  sessionDuration: '7d' | '30d' | 'forever';
}
