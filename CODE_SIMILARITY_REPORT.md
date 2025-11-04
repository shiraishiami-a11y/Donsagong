# コード類似性検出レポート

**プロジェクト:** ゴールデン四柱推命アプリケーション
**作成日:** 2025年11月3日
**分析対象:**
- `/frontend/src` (46 TypeScript/TSXファイル)
- `/backend/app` (20 Pythonファイル)

---

## 📊 検出サマリー

| カテゴリ | 検出数 | 統合可能 | 優先度 |
|---------|--------|----------|--------|
| 重複コンポーネント | 2組 | ✅ 高 | 🔴 高 |
| 類似関数 | 6組 | ✅ 中 | 🟡 中 |
| 重複ロジック | 4組 | ✅ 高 | 🔴 高 |
| 統合可能ユーティリティ | 3組 | ✅ 高 | 🟡 中 |

---

## 🔴 優先度：高（即座に統合推奨）

### 1. 年運・月運スクロールセクション【重複コンポーネント】

**類似度: 95%**

#### 対象ファイル
- `frontend/src/pages/SajuDetailPage/components/YearFortuneScrollSection.tsx` (258行)
- `frontend/src/pages/SajuDetailPage/components/MonthFortuneScrollSection.tsx` (258行)

#### 重複コード量
約240行（全体の93%）

#### 重複内容
```typescript
// 同一の構造（変数名のみ異なる）

// 1. getFortuneColorSolid関数（完全一致）
const getFortuneColorSolid = (fortuneLevel: FortuneLevel): string => {
  const colorMap: Record<FortuneLevel, string> = {
    '大吉': '#FFD700',
    '吉': '#4CAF50',
    '平': '#9E9E9E',
    '凶': '#FF9800',
    '大凶': '#F44336',
  };
  return colorMap[fortuneLevel];
};

// 2. ローディング/エラーUI（完全一致）
if (loading) { /* 同一コード */ }
if (error) { /* 同一コード */ }

// 3. スクロールコンテナスタイル（完全一致）
sx={{
  display: 'flex',
  flexDirection: 'row-reverse',
  gap: 1.5,
  overflowX: 'auto',
  pb: 1.5,
  '&::-webkit-scrollbar': { height: '6px' },
  '&::-webkit-scrollbar-track': { /* 同一 */ },
  '&::-webkit-scrollbar-thumb': { /* 同一 */ },
}}

// 4. カードスタイル（95%一致、widthのみ異なる）
sx={{
  minWidth: { xs: '90px', sm: '100px' }, // 年運
  minWidth: { xs: '85px', sm: '95px' },  // 月運（5pxのみ差）
  // 以下同一...
}}

// 5. 天干地支表示ロジック（完全一致）
<Box sx={{ /* 同一スタイル */ }}>
  <Box data-testid="year-stem">{yearFortune.yearStem}</Box>
  <Box data-testid="year-branch">{yearFortune.yearBranch}</Box>
</Box>
```

#### 統合提案

**推奨アプローチ:** ジェネリック `FortuneScrollSection` コンポーネント作成

```typescript
// frontend/src/pages/SajuDetailPage/components/FortuneScrollSection.tsx

interface FortuneScrollSectionProps<T> {
  title: string;
  items: T[];
  loading: boolean;
  error: string | null;
  selectedId: number | null;
  onSelect: (id: number) => void;
  renderItem: (item: T, isSelected: boolean, isCurrent: boolean) => React.ReactNode;
  getItemId: (item: T) => number;
  getItemCurrent: (item: T) => boolean;
  minCardWidth?: { xs: string; sm: string };
}

export function FortuneScrollSection<T>({
  title,
  items,
  loading,
  error,
  selectedId,
  onSelect,
  renderItem,
  getItemId,
  getItemCurrent,
  minCardWidth = { xs: '90px', sm: '100px' }
}: FortuneScrollSectionProps<T>) {
  // 共通ロジックを実装
}
```

**使用例:**
```typescript
// YearFortuneScrollSection.tsx（20行に短縮）
<FortuneScrollSection
  title={`年運（${daeunStartAge}-${daeunStartAge + 9}歳）`}
  items={years}
  loading={loading}
  error={error}
  selectedId={selectedYear}
  onSelect={onYearSelect}
  getItemId={(y) => y.year}
  getItemCurrent={(y) => y.isCurrent}
  renderItem={(item, isSelected, isCurrent) => (
    <YearFortuneCard fortune={item} isSelected={isSelected} isCurrent={isCurrent} />
  )}
/>

// MonthFortuneScrollSection.tsx（20行に短縮）
<FortuneScrollSection
  title={`月運（${year}年）`}
  items={months}
  minCardWidth={{ xs: '85px', sm: '95px' }}
  // 同様のパターン
/>
```

**削減効果:**
- **削減行数:** 約480行 → 約120行（75%削減）
- **保守性:** 1箇所修正で両方に適用
- **テスト:** 共通ロジックのテストは1回のみ

---

### 2. API Client HTTPメソッド【重複ロジック】

**類似度: 98%**

#### 対象ファイル
`frontend/src/services/api/client.ts`

#### 重複内容
```typescript
// apiGet, apiPost, apiPut, apiDelete（構造が98%一致）

export async function apiGet<T>(endpoint: string, options?: RequestInit) {
  const token = getAuthToken();
  const headers = { /* 同一 */ };
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), API_TIMEOUT);

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'GET', // ← ここだけ異なる
      headers,
      signal: controller.signal,
      ...options,
    });

    clearTimeout(timeoutId);
    const data = await response.json();

    if (!response.ok) { /* 同一エラー処理 */ }

    return { data, status: response.status };
  } catch (error) {
    clearTimeout(timeoutId);
    // 同一エラーハンドリング
  }
}

// apiPost, apiPut, apiDeleteも同様の構造（95%一致）
```

#### 統合提案

```typescript
// frontend/src/services/api/client.ts

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';

/**
 * 汎用HTTPリクエスト関数
 */
async function request<T = any>(
  method: HttpMethod,
  endpoint: string,
  options?: {
    body?: any;
    headers?: HeadersInit;
    timeout?: number;
  }
): Promise<ApiResponse<T>> {
  const token = getAuthToken();
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
    ...options?.headers,
  };

  const controller = new AbortController();
  const timeoutMs = options?.timeout || API_TIMEOUT;
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const fetchOptions: RequestInit = {
      method,
      headers,
      signal: controller.signal,
    };

    // POSTやPUTの場合のみbodyを追加
    if (options?.body && ['POST', 'PUT', 'PATCH'].includes(method)) {
      fetchOptions.body = JSON.stringify(options.body);
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, fetchOptions);
    clearTimeout(timeoutId);

    const data = await response.json();

    if (!response.ok) {
      throw new ApiError(
        data.message || data.detail || 'API request failed',
        response.status,
        data.detail
      );
    }

    return { data, status: response.status };
  } catch (error) {
    clearTimeout(timeoutId);

    if (error instanceof ApiError) throw error;
    if (error instanceof Error && error.name === 'AbortError') {
      throw new ApiError('Request timeout', 408);
    }
    throw new ApiError('Network error', 0, (error as Error).message);
  }
}

// 簡潔なラッパー関数
export const apiGet = <T>(endpoint: string, options?: RequestInit) =>
  request<T>('GET', endpoint, options);

export const apiPost = <T>(endpoint: string, body?: any, options?: RequestInit) =>
  request<T>('POST', endpoint, { ...options, body });

export const apiPut = <T>(endpoint: string, body?: any, options?: RequestInit) =>
  request<T>('PUT', endpoint, { ...options, body });

export const apiDelete = <T>(endpoint: string, options?: RequestInit) =>
  request<T>('DELETE', endpoint, options);
```

**削減効果:**
- **削減行数:** 293行 → 約120行（59%削減）
- **保守性:** エラーハンドリング修正が1箇所のみ
- **拡張性:** PATCHメソッド追加が簡単

---

### 3. ゲストモードフォールバック【重複ロジック】

**類似度: 85%**

#### 対象ファイル
- `frontend/src/services/api/sajuListService.ts`
- `frontend/src/services/api/sajuFortuneService.ts`

#### 重複内容
```typescript
// sajuListService.ts
export async function getSajuList(): Promise<SajuSummary[]> {
  try {
    const response = await apiGet<PaginatedResponse<SajuSummary>>('/api/saju/list');
    if (!response.data) throw new Error('命式一覧の取得に失敗');
    return response.data.items;
  } catch (error: any) {
    // ↓ 重複パターン
    if (error.status === 401 || error.status === 0) {
      const localData = localStorage.getItem('saju_data');
      if (!localData) return [];
      const sajuList: SajuSummary[] = JSON.parse(localData);
      return sajuList;
    }
    throw error;
  }
}

// sajuFortuneService.ts（年運・月運・日運で同様のパターン）
export const getYearFortuneList = async (...) => {
  try {
    const response = await apiGet<YearFortuneListResponse>(...);
    if (!response.data) throw new Error('年運データの取得に失敗');
    return response.data;
  } catch (error: any) {
    // ↓ 同じパターン
    if (error.status === 401 || error.status === 404 || error.status === 0) {
      // モックデータ生成（年運用）
      const years = [];
      for (let i = 0; i < 10; i++) { /* ... */ }
      return { years };
    }
    throw new Error('年運情報の取得に失敗');
  }
};

// getMonthFortuneList、getDayFortuneListも同様
```

#### 統合提案

```typescript
// frontend/src/services/api/guestModeHelper.ts

/**
 * ゲストモードフォールバックヘルパー
 */
export async function withGuestFallback<T>(
  apiCall: () => Promise<T>,
  fallback: {
    storageKey?: string;
    defaultValue?: T;
    mockGenerator?: () => T;
  }
): Promise<T> {
  try {
    return await apiCall();
  } catch (error: any) {
    // 401 (未認証) または 0 (ネットワークエラー) の場合のみフォールバック
    if (error.status === 401 || error.status === 0 || error.status === 404) {
      // 1. LocalStorageから取得
      if (fallback.storageKey) {
        const localData = localStorage.getItem(fallback.storageKey);
        if (localData) {
          return JSON.parse(localData) as T;
        }
      }

      // 2. モックジェネレーター使用
      if (fallback.mockGenerator) {
        return fallback.mockGenerator();
      }

      // 3. デフォルト値返却
      if (fallback.defaultValue !== undefined) {
        return fallback.defaultValue;
      }
    }

    // その他のエラーは再スロー
    throw error;
  }
}
```

**使用例:**
```typescript
// sajuListService.ts（簡潔化）
export async function getSajuList(): Promise<SajuSummary[]> {
  return withGuestFallback(
    () => apiGet<PaginatedResponse<SajuSummary>>('/api/saju/list')
           .then(res => res.data?.items || []),
    {
      storageKey: 'saju_data',
      defaultValue: []
    }
  );
}

// sajuFortuneService.ts（簡潔化）
export const getYearFortuneList = async (
  sajuId: string,
  daeunStartAge: number
): Promise<YearFortuneListResponse> => {
  return withGuestFallback(
    () => apiGet<YearFortuneListResponse>(`/api/saju/${sajuId}/year/${daeunStartAge}`)
           .then(res => res.data!),
    {
      mockGenerator: () => generateMockYearFortune(daeunStartAge)
    }
  );
};

// モックジェネレーター分離
function generateMockYearFortune(daeunStartAge: number): YearFortuneListResponse {
  const years = [];
  const currentYear = new Date().getFullYear();
  for (let i = 0; i < 10; i++) {
    years.push({ /* モックデータ */ });
  }
  return { years };
}
```

**削減効果:**
- **削減行数:** 約150行（重複コード）
- **保守性:** ゲストモード判定ロジックが1箇所に集約
- **可読性:** ビジネスロジックとエラーハンドリングが分離

---

### 4. 吉凶カラー取得関数【重複ロジック】

**類似度: 100%**

#### 対象ファイル
- `frontend/src/pages/SajuDetailPage/components/YearFortuneScrollSection.tsx`（16-25行）
- `frontend/src/pages/SajuDetailPage/components/MonthFortuneScrollSection.tsx`（16-25行）
- `frontend/src/utils/sajuHelpers.ts`（21-31行）

#### 重複内容
```typescript
// YearFortuneScrollSection.tsx、MonthFortuneScrollSection.tsx（完全一致）
const getFortuneColorSolid = (fortuneLevel: FortuneLevel): string => {
  const colorMap: Record<FortuneLevel, string> = {
    '大吉': '#FFD700',
    '吉': '#4CAF50',
    '平': '#9E9E9E',
    '凶': '#FF9800',
    '大凶': '#F44336',
  };
  return colorMap[fortuneLevel];
};

// sajuHelpers.ts（同様のロジック、gradient版）
export const getFortuneColor = (fortuneLevel: FortuneLevel): string => {
  const colorMap: Record<FortuneLevel, string> = {
    '大吉': 'linear-gradient(45deg, #FFD700, #FFA500)',
    '吉': 'linear-gradient(45deg, #4CAF50, #66bb6a)',
    '平': 'linear-gradient(45deg, #9E9E9E, #BDBDBD)',
    '凶': 'linear-gradient(45deg, #FF9800, #ffb74d)',
    '大凶': 'linear-gradient(45deg, #F44336, #ef5350)',
  };
  return colorMap[fortuneLevel];
};
```

#### 統合提案

```typescript
// frontend/src/utils/sajuHelpers.ts（統合版）

/**
 * 吉凶レベルからカラーを取得
 * @param fortuneLevel 吉凶レベル
 * @param variant 'gradient' (デフォルト) | 'solid'
 */
export const getFortuneColor = (
  fortuneLevel: FortuneLevel,
  variant: 'gradient' | 'solid' = 'gradient'
): string => {
  const baseColors: Record<FortuneLevel, { from: string; to: string }> = {
    '大吉': { from: '#FFD700', to: '#FFA500' },
    '吉': { from: '#4CAF50', to: '#66bb6a' },
    '平': { from: '#9E9E9E', to: '#BDBDBD' },
    '凶': { from: '#FF9800', to: '#ffb74d' },
    '大凶': { from: '#F44336', to: '#ef5350' },
  };

  const colors = baseColors[fortuneLevel];

  if (variant === 'solid') {
    return colors.from;
  }

  return `linear-gradient(45deg, ${colors.from}, ${colors.to})`;
};
```

**使用例:**
```typescript
// YearFortuneScrollSection.tsx（削除）
// const getFortuneColorSolid = ... // ← 削除

// 代わりにインポートして使用
import { getFortuneColor } from '../../../utils/sajuHelpers';

borderLeft: `4px solid ${getFortuneColor(yearFortune.fortuneLevel, 'solid')}`
```

**削減効果:**
- **削減行数:** 約30行（重複2箇所 + 統合）
- **保守性:** カラー変更が1箇所のみ
- **一貫性:** グラデーション/ソリッド両対応

---

## 🟡 優先度：中（リファクタリング推奨）

### 5. 天干・地支から五行要素取得【類似関数】

**類似度: 90%**

#### 対象ファイル
- `frontend/src/utils/sajuHelpers.ts`（47-70行）
- `backend/app/services/fortune_service.py`（346-379行）

#### 重複内容
```typescript
// frontend: sajuHelpers.ts
export const getStemElement = (stem: string): FiveElement => {
  const stemMap: Record<string, FiveElement> = {
    '甲': 'wood', '乙': 'wood',
    '丙': 'fire', '丁': 'fire',
    '戊': 'earth', '己': 'earth',
    '庚': 'metal', '辛': 'metal',
    '壬': 'water', '癸': 'water',
  };
  return stemMap[stem] || 'earth';
};

export const getBranchElement = (branch: string): FiveElement => {
  const branchMap: Record<string, FiveElement> = {
    '寅': 'wood', '卯': 'wood',
    '巳': 'fire', '午': 'fire',
    '辰': 'earth', '戌': 'earth', '丑': 'earth', '未': 'earth',
    '申': 'metal', '酉': 'metal',
    '亥': 'water', '子': 'water',
  };
  return branchMap[branch] || 'earth';
};
```

```python
# backend: fortune_service.py
def get_element_from_stem(self, stem: str) -> FiveElement:
    element_map: Dict[str, FiveElement] = {
        "甲": "wood", "乙": "wood",
        "丙": "fire", "丁": "fire",
        "戊": "earth", "己": "earth",
        "庚": "metal", "辛": "metal",
        "壬": "water", "癸": "water",
    }
    return element_map.get(stem, "earth")

def get_element_from_branch(self, branch: str) -> FiveElement:
    element_map: Dict[str, FiveElement] = {
        "寅": "wood", "卯": "wood",
        "巳": "fire", "午": "fire",
        "辰": "earth", "戌": "earth", "丑": "earth", "未": "earth",
        "申": "metal", "酉": "metal",
        "亥": "water", "子": "water",
    }
    return element_map.get(branch, "earth")
```

#### 統合提案

**推奨:** 定数ファイルに集約し、フロントエンド・バックエンド両方で参照

```typescript
// shared/constants/wuxing.ts (フロントエンド・バックエンド共通)

export const STEM_ELEMENT_MAP = {
  '甲': 'wood', '乙': 'wood',
  '丙': 'fire', '丁': 'fire',
  '戊': 'earth', '己': 'earth',
  '庚': 'metal', '辛': 'metal',
  '壬': 'water', '癸': 'water',
} as const;

export const BRANCH_ELEMENT_MAP = {
  '寅': 'wood', '卯': 'wood',
  '巳': 'fire', '午': 'fire',
  '辰': 'earth', '戌': 'earth', '丑': 'earth', '未': 'earth',
  '申': 'metal', '酉': 'metal',
  '亥': 'water', '子': 'water',
} as const;
```

```typescript
// frontend/src/utils/sajuHelpers.ts
import { STEM_ELEMENT_MAP, BRANCH_ELEMENT_MAP } from '@/shared/constants/wuxing';

export const getStemElement = (stem: string): FiveElement =>
  STEM_ELEMENT_MAP[stem] || 'earth';

export const getBranchElement = (branch: string): FiveElement =>
  BRANCH_ELEMENT_MAP[branch] || 'earth';
```

```python
# backend/app/constants/wuxing.py
STEM_ELEMENT_MAP = {
    "甲": "wood", "乙": "wood",
    # ...
}

BRANCH_ELEMENT_MAP = {
    "寅": "wood", "卯": "wood",
    # ...
}
```

**削減効果:**
- **保守性:** マッピング変更が1箇所のみ
- **一貫性:** フロントエンド/バックエンドで同一ロジック保証
- **ドキュメント:** 定数ファイルに五行理論の解説を集約可能

---

### 6. 吉凶レベル相互変換【重複ロジック】

**類似度: 100%**

#### 対象ファイル
- `backend/app/api/saju.py`（156-157行、250-251行、501-502行）
- `backend/app/services/saju_calculator.py`（23-26行）

#### 重複内容
```python
# saju.py（3箇所で同じマッピング）
fortune_level_map = {"大凶": 1, "凶": 2, "平": 3, "吉": 4, "大吉": 5}
fortune_level_reverse_map = {1: "大凶", 2: "凶", 3: "平", 4: "吉", 5: "大吉"}

# saju_calculator.py
FORTUNE_LEVEL_MAP = {1: "大凶", 2: "凶", 3: "平", 4: "吉", 5: "大吉"}
FORTUNE_LEVEL_REVERSE_MAP = {"大凶": 1, "凶": 2, "平": 3, "吉": 4, "大吉": 5}
```

#### 統合提案

```python
# backend/app/constants/fortune_levels.py

from typing import Dict, Literal

FortuneLevel = Literal["大凶", "凶", "平", "吉", "大吉"]
FortuneLevelInt = Literal[1, 2, 3, 4, 5]

# 文字列 → 数値
FORTUNE_LEVEL_TO_INT: Dict[FortuneLevel, FortuneLevelInt] = {
    "大凶": 1,
    "凶": 2,
    "平": 3,
    "吉": 4,
    "大吉": 5,
}

# 数値 → 文字列
FORTUNE_LEVEL_TO_STR: Dict[FortuneLevelInt, FortuneLevel] = {
    1: "大凶",
    2: "凶",
    3: "平",
    4: "吉",
    5: "大吉",
}

# ヘルパー関数
def fortune_to_int(level: FortuneLevel, default: int = 3) -> int:
    """吉凶レベル文字列を数値に変換"""
    return FORTUNE_LEVEL_TO_INT.get(level, default)

def fortune_to_str(level: int, default: FortuneLevel = "平") -> FortuneLevel:
    """数値を吉凶レベル文字列に変換"""
    return FORTUNE_LEVEL_TO_STR.get(level, default)
```

**使用例:**
```python
# backend/app/api/saju.py
from app.constants.fortune_levels import fortune_to_int, fortune_to_str

# 保存時
fortune_level_int = fortune_to_int(saju.fortuneLevel)

# 取得時
fortune_level_str = fortune_to_str(saju_db.fortune_level)
```

**削減効果:**
- **削減行数:** 約20行（重複3箇所）
- **型安全性:** Literal型で間違ったレベル値を防止
- **保守性:** レベル追加・変更が1箇所のみ

---

### 7. LocalStorageから認証トークン取得【類似関数】

**類似度: 100%**

#### 対象ファイル
- `frontend/src/services/api/client.ts`（43-53行）
- `frontend/src/services/api/settingsService.ts`（143-153行）

#### 重複内容
```typescript
// client.ts
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

// settingsService.ts
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
```

#### 統合提案

```typescript
// frontend/src/services/auth/storage.ts

/**
 * 認証情報のLocalStorage管理
 */
export interface AuthStorage {
  token: string;
  refreshToken: string;
  user: User;
}

/**
 * 認証トークンを取得
 */
export function getAuthToken(): string | null {
  const authData = localStorage.getItem('auth');
  if (!authData) return null;

  try {
    const parsed: AuthStorage = JSON.parse(authData);
    return parsed.token || null;
  } catch {
    return null;
  }
}

/**
 * 認証情報を保存
 */
export function setAuthData(data: AuthStorage): void {
  localStorage.setItem('auth', JSON.stringify(data));
}

/**
 * 認証情報を削除
 */
export function clearAuthData(): void {
  localStorage.removeItem('auth');
}

/**
 * 認証情報を取得
 */
export function getAuthData(): AuthStorage | null {
  const authData = localStorage.getItem('auth');
  if (!authData) return null;

  try {
    return JSON.parse(authData);
  } catch {
    return null;
  }
}
```

**使用例:**
```typescript
// client.ts
import { getAuthToken } from '../auth/storage';

// settingsService.ts
import { getAuthToken } from '../auth/storage';

// authService.ts
import { setAuthData, clearAuthData } from '../auth/storage';
```

**削減効果:**
- **削減行数:** 約20行（重複2箇所）
- **型安全性:** AuthStorage型で構造を保証
- **拡張性:** setAuthData、clearAuthDataなど関連機能も集約

---

## 🟢 優先度：低（将来的に検討）

### 8. ログイン・登録ページのヘッダー部分【類似コード】

**類似度: 80%**

#### 対象ファイル
- `frontend/src/pages/LoginPage.tsx`（81-125行）
- `frontend/src/pages/RegisterPage.tsx`（180-213行）

#### 類似内容
両ページで同様の「戻るボタン + ゴールデンロゴ」ヘッダー

#### 統合提案
`<AuthPageHeader />` コンポーネント抽出（優先度低：ページ固有デザインの可能性あり）

---

### 9. パスワード表示切り替えUI【類似コード】

**類似度: 85%**

#### 対象ファイル
- `frontend/src/pages/LoginPage.tsx`（229-268行）
- `frontend/src/pages/RegisterPage.tsx`（293-324行、350-383行）

#### 類似内容
Visibility/VisibilityOff アイコン付きパスワードフィールド

#### 統合提案
`<PasswordTextField />` コンポーネント抽出（優先度低：MUI標準パターン）

---

## 📈 統合後の期待効果

### コード削減量
| カテゴリ | 統合前 | 統合後 | 削減率 |
|---------|--------|--------|--------|
| 運勢スクロール | 516行 | 140行 | **73%削減** |
| API Client | 293行 | 120行 | **59%削減** |
| ゲストフォールバック | 180行 | 60行 | **67%削減** |
| **合計** | **989行** | **320行** | **68%削減** |

### 品質向上
- **保守性:** 修正箇所が1/3に削減
- **テスト:** 重複テストを削除可能
- **一貫性:** ロジックの統一により予期しないバグを防止
- **可読性:** DRY原則により理解しやすいコード

---

## 🛠️ 実装ロードマップ

### Phase 1: 高優先度（即座に実施）
1. **吉凶カラー関数統合**（30分）
   - `getFortuneColor` 統合
   - 既存コード削除

2. **LocalStorage認証ヘルパー統合**（30分）
   - `auth/storage.ts` 作成
   - 既存関数をリプレース

3. **API Client統合**（2時間）
   - `request()` 共通関数作成
   - 既存HTTPメソッドをリプレース
   - テスト実施

### Phase 2: 中優先度（1週間以内）
4. **運勢スクロールコンポーネント統合**（4時間）
   - `FortuneScrollSection` ジェネリック作成
   - 年運・月運をリプレース
   - E2Eテスト更新

5. **ゲストモードヘルパー統合**（2時間）
   - `withGuestFallback` 関数作成
   - 各サービスをリプレース

6. **吉凶レベル定数統合**（1時間）
   - `constants/fortune_levels.py` 作成
   - 既存マッピングをリプレース

### Phase 3: 低優先度（余裕があれば）
7. **五行要素マッピング統合**（1時間）
8. **AuthPageHeader抽出**（2時間）
9. **PasswordTextField抽出**（1時間）

---

## ✅ 実装時の注意点

### 1. 段階的リファクタリング
- **一度に全て変更しない**（リスク高）
- 1つずつ統合 → テスト → コミット
- Git featureブランチで作業

### 2. テストの更新
- 統合前に既存テストが通ることを確認
- 統合後にテストが引き続き通ることを確認
- data-testid属性の変更に注意

### 3. 後方互換性
- 既存のコンポーネントは一時的に共存させる
- 段階的に新APIに移行
- 完全移行後に旧コード削除

### 4. ドキュメント更新
- 統合後のAPIドキュメント更新
- SCOPE_PROGRESS.mdに進捗記録
- コード内コメント充実

---

## 📝 まとめ

**検出された重複コード総量:** 約1000行
**統合後の削減見込み:** 約680行（68%削減）
**最優先統合対象:** 運勢スクロールコンポーネント、API Client
**推定作業時間:** 約12時間（Phase 1-2完了まで）

**次のアクション:**
1. このレポートをチームで確認
2. Phase 1から段階的に実装開始
3. 各統合完了後にSCOPE_PROGRESS.mdを更新

---

**作成者:** Claude Code（ブルーランプエージェント）
**レポートバージョン:** 1.0
