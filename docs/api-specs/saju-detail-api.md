# 命式詳細ページ API仕様書

生成日: 2025年11月2日（更新）
収集元: frontend/src/services/mock/SajuDetailService.ts
@MOCK_TO_APIマーク数: 3

## エンドポイント一覧

### 1. 命式詳細取得

- **エンドポイント**: `GET /api/saju/{id}`
- **APIパス定数**: `API_PATHS.SAJU.DETAIL(id)`
- **認証**: 必須（JWT Bearer Token）
- **説明**: 指定された命式IDの詳細情報を取得

#### Request

**パスパラメータ**:
```typescript
{
  id: string;  // 命式ID
}
```

**Headers**:
```
Authorization: Bearer {access_token}
```

#### Response

**成功時（200 OK）**:
```typescript
{
  // 基本情報
  id: string;
  name: string;
  birthDatetime: string;  // ISO 8601形式 (例: "1990-03-15T14:30:00+09:00")
  gender: 'male' | 'female';
  createdAt: string;  // ISO 8601形式

  // 四柱
  yearStem: string;   // 年干 (例: "甲")
  yearBranch: string;   // 年支 (例: "寅")
  monthStem: string;  // 月干
  monthBranch: string;  // 月支
  dayStem: string;    // 日干
  dayBranch: string;    // 日支
  hourStem: string;   // 時干
  hourBranch: string;   // 時支

  // 大運情報
  daeunNumber: number;  // 大運数 (例: 7)
  isForward: boolean;   // 順行: true, 逆行: false
  afterBirthYears: number;   // 生後年数
  afterBirthMonths: number;  // 生後月数
  afterBirthDays: number;    // 生後日数
  firstDaeunDate: string;    // 第一大運開始日 (YYYY-MM-DD)

  // 大運リスト
  daeunList: Array<{
    id: number;
    sajuId: string;
    startAge: number;   // 開始年齢 (例: 8)
    endAge: number;     // 終了年齢 (例: 17)
    daeunStem: string;  // 大運天干
    daeunBranch: string;  // 大運地支
    fortuneLevel: '大吉' | '吉' | '平' | '凶' | '大凶';
    sipsin: string;     // 十神 (例: "正官", "偏財")
    isCurrent: boolean;  // 現在の大運かどうか
  }>;

  // 人生グラフデータ
  lifeGraphData: Array<{
    age: number;        // 年齢（大運期間の中間年齢）
    fortuneLevel: number;  // 吉凶レベル (1-5)
    daeunStem: string;
    daeunBranch: string;
    label: string;      // グラフラベル (例: "8-17歳: 乙卯")
  }>;

  // 吉凶レベル
  fortuneLevel: '大吉' | '吉' | '平' | '凶' | '大凶';
}
```

**エラー時（404 Not Found）**:
```typescript
{
  error: "命式が見つかりません"
}
```

**エラー時（401 Unauthorized）**:
```typescript
{
  error: "認証が必要です"
}
```

---

### 2. 大運分析取得

- **エンドポイント**: `GET /api/saju/{id}/daeun`
- **認証**: 必須（JWT Bearer Token）
- **説明**: 指定された命式IDの大運分析情報を取得

#### Request

**パスパラメータ**:
```typescript
{
  id: string;  // 命式ID
}
```

**Headers**:
```
Authorization: Bearer {access_token}
```

#### Response

**成功時（200 OK）**:
```typescript
{
  daeunNumber: number;       // 大運数（例: 7）
  isForward: boolean;        // 順行: true, 逆行: false
  afterBirth: {
    years: number;           // 生後年数
    months: number;          // 生後月数
    days: number;            // 生後日数
  };
  firstDaeunDate: string;    // 第一大運開始日（YYYY-MM-DD形式）
  currentAge: number;        // 現在年齢
  daeunList: Array<{
    id: number;
    sajuId: string;
    startAge: number;        // 開始年齢（例: 8）
    endAge: number;          // 終了年齢（例: 17）
    daeunStem: string;       // 大運天干
    daeunBranch: string;     // 大運地支
    fortuneLevel: '大吉' | '吉' | '平' | '凶' | '大凶';
    sipsin: string;          // 十神（例: "正官"）
    isCurrent: boolean;      // 現在の大運期間かどうか
  }>;
}
```

**例**:
```json
{
  "daeunNumber": 7,
  "isForward": true,
  "afterBirth": {
    "years": 7,
    "months": 5,
    "days": 2
  },
  "firstDaeunDate": "1993-11-16",
  "currentAge": 35,
  "daeunList": [
    {
      "id": 1,
      "sajuId": "001",
      "startAge": 8,
      "endAge": 17,
      "daeunStem": "乙",
      "daeunBranch": "卯",
      "fortuneLevel": "平",
      "sipsin": "偏印",
      "isCurrent": false
    },
    {
      "id": 2,
      "sajuId": "001",
      "startAge": 18,
      "endAge": 27,
      "daeunStem": "甲",
      "daeunBranch": "寅",
      "fortuneLevel": "吉",
      "sipsin": "比肩",
      "isCurrent": false
    },
    {
      "id": 3,
      "sajuId": "001",
      "startAge": 28,
      "endAge": 37,
      "daeunStem": "丙",
      "daeunBranch": "午",
      "fortuneLevel": "大吉",
      "sipsin": "正官",
      "isCurrent": true
    }
  ]
}
```

**エラー時（404 Not Found）**:
```typescript
{
  error: string;  // "命式が見つかりません"
}
```

**エラー時（401 Unauthorized）**:
```typescript
{
  error: string;  // "認証が必要です"
}
```

---

### 3. 現在の運勢取得

- **エンドポイント**: `GET /api/saju/{id}/current`
- **APIパス定数**: `API_PATHS.SAJU.CURRENT(id)`
- **認証**: 必須（JWT Bearer Token）
- **説明**: 指定された命式IDの現在の年運・月運・日運を取得

#### Request

**パスパラメータ**:
```typescript
{
  id: string;  // 命式ID
}
```

**クエリパラメータ**（オプション）:
```typescript
{
  date?: string;  // 特定日の運勢を取得 (YYYY-MM-DD形式、省略時は今日)
}
```

**Headers**:
```
Authorization: Bearer {access_token}
```

#### Response

**成功時（200 OK）**:
```typescript
{
  date: string;  // 運勢の基準日 (YYYY-MM-DD)

  // 年運
  yearFortune: {
    stem: string;       // 天干
    branch: string;     // 地支
    fortuneLevel: '大吉' | '吉' | '平' | '凶' | '大凶';
    description: string;  // 解説文
    element: 'wood' | 'fire' | 'earth' | 'metal' | 'water';  // 五行要素
  };

  // 月運
  monthFortune: {
    stem: string;
    branch: string;
    fortuneLevel: '大吉' | '吉' | '平' | '凶' | '大凶';
    description: string;
    element: 'wood' | 'fire' | 'earth' | 'metal' | 'water';
  };

  // 日運
  dayFortune: {
    stem: string;
    branch: string;
    fortuneLevel: '大吉' | '吉' | '平' | '凶' | '大凶';
    description: string;
    element: 'wood' | 'fire' | 'earth' | 'metal' | 'water';
  };
}
```

---

## モックサービス参照

実装時はこのモックサービスの挙動を参考にする:
```
frontend/src/services/mock/SajuDetailService.ts
```

## データ型定義

実装時はこの型定義を使用する:
```
frontend/src/types/index.ts
```

主要な型:
- `SajuDetailPageData` - 命式詳細ページ用データ
- `DaeunInfo` - 大運情報
- `DaeunAnalysisResponse` - 大運分析レスポンス
- `CurrentFortuneDetailResponse` - 現在の運勢
- `LifeGraphData` - 人生グラフデータ
- `FortuneLevel` - 吉凶レベル（'大吉' | '吉' | '平' | '凶' | '大凶'）
- `FiveElement` - 五行要素（'wood' | 'fire' | 'earth' | 'metal' | 'water'）

---

## 実装時の注意事項

### 1. 大運計算
- 性別（gender）に基づいて順行/逆行を決定
- 節入日ベースで正確な大運開始日を計算
- lunar-pythonライブラリと210年節気DBを使用

### 2. 年月日運計算
- lunar-pythonを使用して現在日時の干支を計算
- 天干・地支マトリックスで吉凶判定（1-5段階）
- 調候用神80%:原局20%の比重で総合評価

### 3. 十神（sipsin）計算
- 日干を基準に各大運期の天干・地支から十神を判定
- 比肩、劫財、食神、傷官、偏財、正財、偏官、正官、偏印、印綬の10種

### 4. 人生グラフデータ
- 大運期間の中間年齢をグラフのX座標とする
- 吉凶レベルを1-5の数値に変換してY座標とする
- 10年刻みのグリッドに対応

### 5. セキュリティ
- JWTトークンによる認証必須
- user_idと命式のownershipを検証
- 他人の命式データへのアクセスを禁止

---

**作成日**: 2025年11月1日
**更新日**: 2025年11月2日
**バージョン**: 1.1（大運分析エンドポイント追加）
**対応ページ**: P-003（命式詳細・グラフ表示ページ）
