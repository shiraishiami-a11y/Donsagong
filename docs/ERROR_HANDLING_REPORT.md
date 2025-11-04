# エラーハンドリング調査レポート

**調査日**: 2025-11-03
**プロジェクト**: ゴールデン四柱推命アプリケーション
**対象**: `/frontend/src` および `/backend/app`

---

## 📋 調査概要

CLAUDE.mdの要件「エラーハンドリング必須」に基づき、フロントエンド（TypeScript/React）とバックエンド（Python/FastAPI）のエラーハンドリングの有無を調査しました。

---

## ✅ 適切にエラーハンドリングされている箇所

### フロントエンド

#### 1. **APIクライアント (`/frontend/src/services/api/client.ts`)**
- **評価**: ✅ 優れたエラーハンドリング
- **詳細**:
  - 全HTTPメソッド（GET, POST, PUT, DELETE）でtry-catchによる包括的なエラーハンドリング
  - カスタムエラークラス `ApiError` による構造化されたエラー管理
  - タイムアウト処理（AbortController）
  - ネットワークエラーの明確な分類
  ```typescript
  catch (error) {
    if (error instanceof ApiError) throw error;
    if (error instanceof Error && error.name === 'AbortError') {
      throw new ApiError('Request timeout', 408);
    }
    throw new ApiError('Network error', 0, (error as Error).message);
  }
  ```

#### 2. **命式リスト取得 (`/frontend/src/services/api/sajuListService.ts`)**
- **評価**: ✅ 良好なエラーハンドリング
- **詳細**:
  - `getSajuList()`: try-catchで401/ネットワークエラーをキャッチし、LocalStorageフォールバック
  - `getSajuDetail()`: try-catchで401/404をキャッチし、LocalStorageフォールバック
  - `deleteSaju()`: APIエラーはそのまま再スローし、上位で処理
  ```typescript
  try {
    const response = await apiGet<PaginatedResponse<SajuSummary>>('/api/saju/list');
    // ...
  } catch (error: any) {
    if (error.status === 401 || error.status === 0) {
      const localData = localStorage.getItem('saju_data');
      // フォールバック処理
    }
    throw error;
  }
  ```

#### 3. **年月日運取得 (`/frontend/src/services/api/sajuFortuneService.ts`)**
- **評価**: ✅ 良好なエラーハンドリング
- **詳細**:
  - `getDaeunList()`: try-catchでエラーをキャッチし、カスタムメッセージで再スロー
  - `getYearFortuneList()`, `getMonthFortuneList()`, `getDayFortuneList()`:
    - 401/404/0エラー時にモックデータを生成してフォールバック
    - その他のエラーは明確なメッセージで再スロー
  ```typescript
  catch (error: any) {
    if (error.status === 401 || error.status === 404 || error.status === 0) {
      // モックデータ生成
      return { years };
    }
    throw new Error('年運情報の取得に失敗しました');
  }
  ```

#### 4. **設定サービス (`/frontend/src/services/api/settingsService.ts`)**
- **評価**: ✅ 良好なエラーハンドリング
- **詳細**:
  - `exportData()`: fetchエラーをキャッチし、エラー詳細をスロー
  - `importData()`: fetchエラーをキャッチし、エラー詳細をスロー
  - `getUserSettings()`: JSON.parseのtry-catchでデフォルト値を返す
  ```typescript
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || error.message || 'エクスポートに失敗しました');
  }
  ```

#### 5. **認証コンテキスト (`/frontend/src/features/auth/contexts/AuthContext.tsx`)**
- **評価**: ✅ 良好なエラーハンドリング
- **詳細**:
  - `initializeAuth()`: try-catchでトークン復元時のエラーをキャッチし、LocalStorageをクリア
  - `login()`: try-catchでエラーをキャッチし、上位に再スロー
  - `register()`: try-catchで登録エラーをキャッチ、移行エラーは登録を妨げない設計
  - `logout()`: try-finallyでAPIエラーでもLocalStorageをクリア
  ```typescript
  try {
    await authService.logout();
    setUser(null);
  } catch (error) {
    // ログアウトは失敗してもクリア
    setUser(null);
  }
  ```

#### 6. **ページコンポーネント**
- **LoginPage (`/frontend/src/pages/LoginPage.tsx`)**: try-catchでログインエラーをキャッチし、ユーザーにエラーメッセージ表示
- **RegisterPage (`/frontend/src/pages/RegisterPage.tsx`)**: try-catchで登録エラーをキャッチし、エラー状態を管理
- **TopPage (`/frontend/src/pages/TopPage/index.tsx`)**: try-catchで計算エラーをキャッチし、ネットワークエラーメッセージを表示

### バックエンド

#### 1. **認証API (`/backend/app/api/auth.py`)**
- **評価**: ✅ 優れたエラーハンドリング
- **詳細**:
  - 全エンドポイントでHTTPExceptionによる明確なエラーレスポンス
  - パスワードバリデーション（400 BAD_REQUEST）
  - メール重複チェック（409 CONFLICT）
  - 認証エラー（401 UNAUTHORIZED）
  - アカウント無効化チェック（401 UNAUTHORIZED）
  ```python
  if not user:
      raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="メールアドレスまたはパスワードが正しくありません",
      )
  ```

#### 2. **命式API (`/backend/app/api/saju.py`)**
- **評価**: ✅ 優れたエラーハンドリング
- **詳細**:
  - `/calculate`: try-except-elseで ValueError（400）と一般例外（500）を分離
  - `/save`: try-exceptでDB保存エラーをキャッチし、ロールバック
  - `/list`: try-exceptで一般例外を500エラーとして返す
  - `/export`: try-exceptでエクスポートエラーを500エラーとして返す
  - `/import`: try-exceptでJSONDecodeError、ValueError、一般例外を分離してハンドリング、常にロールバック
  - `/{id}` (詳細取得): try-exceptでHTTPExceptionを再スロー、一般例外は500エラー
  - `/delete/{id}`: try-exceptでHTTPExceptionを再スロー、一般例外は500エラーでロールバック
  - `/migrate`: try-exceptで複数の例外タイプを分離し、常にロールバック
  ```python
  try:
      # 処理
  except ValueError as e:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
  except Exception as e:
      raise HTTPException(
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          detail=f"命式計算中にエラーが発生しました: {str(e)}"
      )
  ```

#### 3. **命式計算サービス (`/backend/app/services/saju_calculator.py`)**
- **評価**: ✅ 良好なエラーハンドリング
- **詳細**:
  - `SolarTermsDB.__init__()`: try-exceptでFileNotFoundError、一般例外を分離
  - `get_jieqi_datetime()`: 年範囲チェックでValueError
  - `_validate_input()`: 年範囲チェック、性別チェックでValueError
  ```python
  try:
      with open(self.db_path, "r", encoding="utf-8") as f:
          # ...
  except FileNotFoundError:
      raise FileNotFoundError(f"210年節気DBが見つかりません: {self.db_path}")
  except Exception as e:
      raise Exception(f"210年節気DB読み込みエラー: {e}")
  ```

---

## ⚠️ エラーハンドリングが不足している箇所

### フロントエンド

#### 1. **認証サービス (`/frontend/src/features/auth/services/authService.ts`)**

**問題**: 全メソッドでtry-catchが存在しない

**影響**: APIエラーが直接上位に伝播し、予期しないエラーメッセージがユーザーに表示される可能性

**修正すべき箇所**:

1. **`login()`** (14-34行目)
   ```typescript
   async login(data: LoginRequest): Promise<AuthResponse> {
     // try-catchなし
     const response = await apiClient.post<AuthResponse>('/api/auth/login', data);
     // ...
   }
   ```
   **推奨修正**:
   ```typescript
   async login(data: LoginRequest): Promise<AuthResponse> {
     try {
       const response = await apiClient.post<AuthResponse>('/api/auth/login', data);
       if (!response.data) {
         throw new Error('ログインに失敗しました');
       }
       // トークン保存処理
       return response.data;
     } catch (error) {
       console.error('[authService] Login error:', error);
       throw error; // または適切なエラーメッセージで再スロー
     }
   }
   ```

2. **`register()`** (40-60行目)
   ```typescript
   async register(data: RegisterRequest): Promise<AuthResponse> {
     // try-catchなし
     const response = await apiClient.post<AuthResponse>('/api/auth/register', data);
     // ...
   }
   ```

3. **`getCurrentUser()`** (79-87行目)
   ```typescript
   async getCurrentUser(): Promise<User> {
     // try-catchなし
     const response = await apiClient.get<User>('/api/auth/me');
     // ...
   }
   ```

**注**: `logout()`はtry-finallyで適切にハンドリングされているため問題なし。

---

#### 2. **命式計算サービス (`/frontend/src/services/api/sajuCalculationService.ts`)**

**問題**: 全メソッドでtry-catchが存在しない

**影響**: APIエラーが直接上位に伝播

**修正すべき箇所**:

1. **`calculateSaju()`** (16-22行目)
   ```typescript
   export async function calculateSaju(data: BirthDataRequest): Promise<SajuResponse> {
     // try-catchなし
     const response = await apiClient.post<SajuResponse>('/api/saju/calculate', data);
     if (!response.data) {
       throw new Error('命式計算に失敗しました');
     }
     return response.data;
   }
   ```
   **推奨修正**:
   ```typescript
   export async function calculateSaju(data: BirthDataRequest): Promise<SajuResponse> {
     try {
       const response = await apiClient.post<SajuResponse>('/api/saju/calculate', data);
       if (!response.data) {
         throw new Error('命式計算に失敗しました');
       }
       return response.data;
     } catch (error) {
       console.error('Failed to calculate saju:', error);
       throw new Error('命式計算中にエラーが発生しました');
     }
   }
   ```

2. **`saveSaju()`** (28-34行目)
   ```typescript
   export async function saveSaju(data: SajuResponse): Promise<SaveResponse> {
     // try-catchなし
     const response = await apiClient.post<SaveResponse>('/api/saju/save', data);
     if (!response.data) {
       throw new Error('命式保存に失敗しました');
     }
     return response.data;
   }
   ```

---

### バックエンド

#### 1. **年月日運計算サービス (`/backend/app/services/fortune_service.py`)**

**問題**: 全メソッドでtry-exceptが存在しない

**影響**: lunar-pythonのエラーや計算エラーが上位API層に直接伝播

**修正すべき箇所**:

1. **`calculate_year_fortune()`** (33-67行目)
   ```python
   def calculate_year_fortune(
       self, birth_year: int, birth_month: int, birth_day: int,
       day_stem: str, target_year: int
   ) -> Tuple[str, str, FortuneLevel, str]:
       # try-exceptなし
       solar = Solar.fromYmd(target_year, 1, 1)
       lunar = solar.getLunar()
       # ...
   ```
   **推奨修正**:
   ```python
   def calculate_year_fortune(
       self, birth_year: int, birth_month: int, birth_day: int,
       day_stem: str, target_year: int
   ) -> Tuple[str, str, FortuneLevel, str]:
       try:
           solar = Solar.fromYmd(target_year, 1, 1)
           lunar = solar.getLunar()
           # ...
           return year_stem, year_branch, fortune_level, sipsin
       except Exception as e:
           raise ValueError(f"年運計算中にエラーが発生しました: {str(e)}")
   ```

2. **`calculate_month_fortune()`** (69-99行目)
3. **`calculate_day_fortune()`** (101-133行目)
4. **`calculate_year_list()`** (135-179行目)
5. **`calculate_month_list()`** (181-218行目)
6. **`calculate_day_list()`** (220-266行目)

---

#### 2. **ドンサゴン分析サービス (`/backend/app/services/fortune_analyzer.py`)**

**問題**: 全メソッドでtry-exceptが存在しない

**影響**: マトリックスデータ参照エラーやNoneチェック不足によるエラーが上位に伝播

**修正すべき箇所**:

1. **`analyze_daeun_fortune()`** (42-96行目)
   ```python
   def analyze_daeun_fortune(
       self, day_stem: str, day_branch: str, hour_stem: str,
       hour_branch: str, month_branch: str, daeun_stem: str, daeun_branch: str
   ) -> FortuneLevel:
       # try-exceptなし
       point1_fortune = self._check_tengan_relation(day_stem, daeun_stem)
       # ...
   ```
   **推奨修正**:
   ```python
   def analyze_daeun_fortune(
       self, day_stem: str, day_branch: str, hour_stem: str,
       hour_branch: str, month_branch: str, daeun_stem: str, daeun_branch: str
   ) -> FortuneLevel:
       try:
           # 入力バリデーション
           if not all([day_stem, day_branch, hour_stem, hour_branch, month_branch, daeun_stem, daeun_branch]):
               raise ValueError("全てのパラメータが必須です")

           point1_fortune = self._check_tengan_relation(day_stem, daeun_stem)
           # ...
           return self._score_to_fortune(total_score)
       except Exception as e:
           raise ValueError(f"大運分析中にエラーが発生しました: {str(e)}")
   ```

2. **`_check_johoo()`** (144-172行目)
   - マトリックスデータが存在しない場合のエラー処理が不足

---

## 📊 統計サマリー

| 項目 | フロントエンド | バックエンド |
|------|--------------|------------|
| **調査ファイル数** | 9ファイル | 6ファイル |
| **✅ 適切にハンドリング** | 6ファイル | 4ファイル |
| **⚠️ ハンドリング不足** | 2ファイル | 2ファイル |
| **エラーハンドリング率** | **66.7%** | **66.7%** |

---

## 🎯 優先度別修正推奨リスト

### 🔴 **高優先度**（ユーザー影響大）

1. **`/frontend/src/features/auth/services/authService.ts`**
   - 全メソッド（login, register, getCurrentUser）にtry-catchを追加
   - 理由: 認証失敗時のエラーメッセージが不明確だとユーザー体験が悪化

2. **`/frontend/src/services/api/sajuCalculationService.ts`**
   - calculateSaju, saveSajuにtry-catchを追加
   - 理由: 命式計算はアプリの中核機能であり、エラー時の適切なメッセージが必須

### 🟡 **中優先度**（安定性向上）

3. **`/backend/app/services/fortune_service.py`**
   - 全計算メソッドにtry-exceptを追加
   - 理由: lunar-pythonのエラーを明確にキャッチし、上位APIに適切なエラーを返す

4. **`/backend/app/services/fortune_analyzer.py`**
   - analyze_daeun_fortuneにtry-exceptを追加
   - 理由: マトリックスデータの参照エラーを防ぐ

---

## 📝 推奨コーディング標準

今後の開発では以下の標準に従うことを推奨します:

### フロントエンド（TypeScript）

```typescript
// ✅ Good
export async function apiMethod(data: RequestType): Promise<ResponseType> {
  try {
    const response = await apiClient.post<ResponseType>('/endpoint', data);
    if (!response.data) {
      throw new Error('データ取得に失敗しました');
    }
    return response.data;
  } catch (error) {
    console.error('[apiMethod] Error:', error);
    throw error; // または適切なエラーメッセージで再スロー
  }
}

// ❌ Bad
export async function apiMethod(data: RequestType): Promise<ResponseType> {
  const response = await apiClient.post<ResponseType>('/endpoint', data);
  return response.data;
}
```

### バックエンド（Python）

```python
# ✅ Good
def service_method(param: str) -> ResultType:
    try:
        # 処理
        result = some_calculation(param)
        return result
    except ValueError as e:
        raise ValueError(f"バリデーションエラー: {str(e)}")
    except Exception as e:
        raise Exception(f"予期しないエラー: {str(e)}")

# ❌ Bad
def service_method(param: str) -> ResultType:
    result = some_calculation(param)
    return result
```

---

## ✅ 結論

**エラーハンドリング実装率**: **66.7%**

- **フロントエンド**: APIクライアント層は優れているが、一部のサービス層でtry-catchが不足
- **バックエンド**: API層は優れているが、サービス層（計算エンジン）でtry-exceptが不足

**推奨アクション**:
1. 高優先度の4ファイルを修正（認証サービス、命式計算サービス）
2. 中優先度の2ファイルを修正（年月日運計算、ドンサゴン分析）
3. 今後の新規コード作成時は必ずtry-catch/try-exceptを実装

---

**レポート作成日**: 2025-11-03
**作成者**: Claude (Anthropic AI)
