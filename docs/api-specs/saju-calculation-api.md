# 命式計算・保存API仕様書

生成日: 2025年11月2日
収集元: frontend/src/services/mock/SajuCalculationService.ts
@MOCK_TO_APIマーク数: 2

## エンドポイント一覧

### 1. 命式計算

- **エンドポイント**: `POST /api/saju/calculate`
- **認証**: 不要（ゲストモード対応）
- **説明**: 生年月日時と性別から四柱推命の命式を計算し、大運リスト・吉凶レベルを返す

#### Request

**リクエストボディ**:
```typescript
{
  birthDatetime: string;   // ISO 8601形式（例: "1990-03-15T14:30:00+09:00"）
  gender: 'male' | 'female';  // 必須: 大運の順行/逆行判定に使用
  name?: string;           // オプション: 命式の名前
  timezoneOffset?: number; // オプション: タイムゾーンオフセット（KST = 9）
}
```

**例**:
```json
{
  "birthDatetime": "1990-03-15T14:30:00+09:00",
  "gender": "male",
  "name": "山田 太郎",
  "timezoneOffset": 9
}
```

#### Response

**成功時（200 OK）**:
```typescript
{
  id: string;              // 命式ID（UUID）
  name?: string;           // 入力された名前
  birthDatetime: string;   // ISO 8601形式
  gender: string;          // 'male' | 'female'

  // 四柱（年・月・日・時）
  yearStem: string;        // 年天干（例: "甲"）
  yearBranch: string;      // 年地支（例: "子"）
  monthStem: string;       // 月天干
  monthBranch: string;     // 月地支
  dayStem: string;         // 日天干
  dayBranch: string;       // 日地支
  hourStem: string;        // 時天干
  hourBranch: string;      // 時地支

  // 大運計算情報
  daeunNumber: number;     // 大運数（例: 7）
  isForward: boolean;      // 順行: true, 逆行: false
  afterBirthYears: number; // 生後年数（第一大運までの年数）
  afterBirthMonths: number;// 生後月数
  afterBirthDays: number;  // 生後日数
  firstDaeunDate: string;  // 第一大運開始日（YYYY-MM-DD形式）

  // 大運リスト（通常10個、100歳まで）
  daeunList: Array<{
    id: number;
    sajuId: string;
    startAge: number;      // 開始年齢（例: 8）
    endAge: number;        // 終了年齢（例: 17）
    daeunStem: string;     // 大運天干
    daeunBranch: string;   // 大運地支
    fortuneLevel: '大吉' | '吉' | '平' | '凶' | '大凶';
    sipsin?: string;       // 十神（例: "正官"）
    isCurrent?: boolean;   // 現在の大運期間かどうか
  }>;

  // 吉凶レベル（全体の総合評価）
  fortuneLevel: '大吉' | '吉' | '平' | '凶' | '大凶';

  createdAt: string;       // ISO 8601形式
}
```

**例**:
```json
{
  "id": "saju-1730505600000",
  "name": "山田 太郎",
  "birthDatetime": "1990-03-15T14:30:00+09:00",
  "gender": "male",
  "yearStem": "庚",
  "yearBranch": "午",
  "monthStem": "己",
  "monthBranch": "卯",
  "dayStem": "丙",
  "dayBranch": "午",
  "hourStem": "乙",
  "hourBranch": "未",
  "daeunNumber": 7,
  "isForward": true,
  "afterBirthYears": 7,
  "afterBirthMonths": 5,
  "afterBirthDays": 2,
  "firstDaeunDate": "1997-08-17",
  "daeunList": [
    {
      "id": 1,
      "sajuId": "saju-1730505600000",
      "startAge": 8,
      "endAge": 17,
      "daeunStem": "乙",
      "daeunBranch": "卯",
      "fortuneLevel": "平",
      "sipsin": "偏印",
      "isCurrent": false
    }
  ],
  "fortuneLevel": "吉",
  "createdAt": "2025-11-02T10:00:00+09:00"
}
```

**エラー時（400 Bad Request）**:
```typescript
{
  error: string;  // "birthDatetimeとgenderは必須です"
                  // "対応範囲外の日付です（1900-2109年のみ）"
                  // "genderは'male'または'female'である必要があります"
}
```

---

### 2. 命式保存

- **エンドポイント**: `POST /api/saju/save`
- **認証**: オプション（ゲストモード時は不要、ログイン時はJWT Bearer Token）
- **説明**: 計算済みの命式をデータベース（またはLocalStorage）に保存

#### Request

**Headers**（ログイン時のみ）:
```
Authorization: Bearer {access_token}
```

**リクエストボディ**:
```typescript
{
  // SajuResponse 型の全フィールド
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
  daeunList: Array<DaeunInfo>;
  fortuneLevel: FortuneLevel;
  createdAt: string;
  daeunNumber?: number;
  isForward?: boolean;
  afterBirthYears?: number;
  afterBirthMonths?: number;
  afterBirthDays?: number;
  firstDaeunDate?: string;
}
```

**例**:
```json
{
  "id": "saju-1730505600000",
  "name": "山田 太郎",
  "birthDatetime": "1990-03-15T14:30:00+09:00",
  "gender": "male",
  "yearStem": "庚",
  "yearBranch": "午",
  "monthStem": "己",
  "monthBranch": "卯",
  "dayStem": "丙",
  "dayBranch": "午",
  "hourStem": "乙",
  "hourBranch": "未",
  "daeunList": [...],
  "fortuneLevel": "吉",
  "createdAt": "2025-11-02T10:00:00+09:00",
  "daeunNumber": 7,
  "isForward": true,
  "afterBirthYears": 7,
  "afterBirthMonths": 5,
  "afterBirthDays": 2,
  "firstDaeunDate": "1997-08-17"
}
```

#### Response

**成功時（201 Created）**:
```typescript
{
  success: boolean;  // true
  id: string;        // 保存された命式ID
  message: string;   // "命式を保存しました"
}
```

**例**:
```json
{
  "success": true,
  "id": "saju-1730505600000",
  "message": "命式を保存しました"
}
```

**エラー時（400 Bad Request）**:
```typescript
{
  error: string;  // "命式データが不正です"
}
```

**エラー時（401 Unauthorized）**（ログインモードのみ）:
```typescript
{
  error: string;  // "認証が必要です"
}
```

---

## モックサービス参照

実装時はこのモックサービスの挙動を参考にする:
```
frontend/src/services/mock/SajuCalculationService.ts
```

## データ型定義

実装時はこの型定義を使用する:
```
frontend/src/types/index.ts
```

主要な型:
- `BirthDataRequest` - 生年月日時入力リクエスト
- `SajuResponse` - 命式計算結果
- `DaeunInfo` - 大運情報
- `FortuneLevel` - 吉凶レベル（'大吉' | '吉' | '平' | '凶' | '大凶'）
- `SaveResponse` - 保存成功レスポンス

---

## 実装時の注意事項

### 1. 四柱推命計算ロジック（最重要）

**必須原則**:
- ✅ `lunar-python` ライブラリの `EightChar` クラスを使用
- ✅ 210年節気データベース（`solar_terms_1900_2109_JIEQI_ONLY.json`）で節入日を確認
- ✅ タイムゾーンを KST (UTC+9) に統一
- ✅ 性別パラメータ必須（大運の順行/逆行判定に使用）
- ✅ 入力バリデーション: 1900-2109年範囲内

**絶対禁止**:
- ❌ 計算ロジックの自作
- ❌ タイムゾーンの混在
- ❌ 節気データの推定・補間
- ❌ 性別パラメータの省略

### 2. 大運計算

**計算手順**:
1. 性別 × 年柱天干の陰陽 → 順行/逆行を決定
   - 男性 + 陽干（甲・丙・戊・庚・壬）→ 順行
   - 男性 + 陰干（乙・丁・己・辛・癸）→ 逆行
   - 女性 + 陽干 → 逆行
   - 女性 + 陰干 → 順行

2. 生まれた日から次の節入日までの日数を計算
   - 順行: 次の節入日まで
   - 逆行: 前の節入日まで

3. 大運数 = (日数 ÷ 3) を四捨五入

4. 第一大運開始日 = 生年月日 + 大運数（年）

5. 大運期間: 各10年（例: 8-17歳、18-27歳...）

### 3. 吉凶判定

**ドンサゴン分析法を使用**:
- 用神 = 武器（不足を補うものではない）
- 日支の合は無条件吉
- 調候用神 80% : 原局 20%
- 天干の合は基本的に凶
- 月地支は用神不可

**マトリックスデータベース活用**:
- 天干100マトリックス（10×10）: `docs/DONSAGONG_MASTER_DATABASE.md`
- 地支144マトリックス（12×12）: 同上
- 調候用神表（季節別）: 同上

**吉凶レベル**:
- 5段階: 大吉（5）、吉（4）、平（3）、凶（2）、大凶（1）
- 数値マッピング: `FortuneLevelMap` を使用

### 4. データ範囲制約

- サポート範囲: 1900年1月1日 〜 2109年12月31日
- 範囲外の日付は `400 Bad Request` でエラーを返す

### 5. タイムゾーン処理

- すべての日時を KST (UTC+9) に変換
- 210年節気DB は UTC+8（北京時間）なので1時間加算が必要
- ISO 8601 形式で返却（例: "1990-03-15T14:30:00+09:00"）

### 6. ゲスト/ログインモード対応

**ゲストモード**:
- 認証不要
- 命式計算は誰でも可能
- 保存時は LocalStorage に保存（フロントエンド側処理）

**ログインモード**:
- JWT トークンで認証
- PostgreSQL に保存
- user_id と命式を紐付け

### 7. パフォーマンス最適化

- 命式計算は CPU 負荷が高いため、キャッシュ検討
- 同一の生年月日時+性別の計算結果をRedis にキャッシュ（TTL: 1時間）
- キャッシュキー: `saju:calc:{birthDatetime}:{gender}`

### 8. エラーハンドリング

**バリデーションエラー**:
```json
{
  "error": "birthDatetimeとgenderは必須です"
}
```

**範囲外エラー**:
```json
{
  "error": "対応範囲外の日付です（1900-2109年のみ）"
}
```

**計算エラー**:
```json
{
  "error": "命式計算中にエラーが発生しました"
}
```

---

**作成日**: 2025年11月2日
**バージョン**: 1.0
**対応ページ**: P-001（トップページ・命式記入ページ）
