# 年月日運API仕様書

生成日: 2025年11月2日
収集元: frontend/src/services/mock/SajuDetailService.ts
@MOCK_TO_APIマーク数: 3

## エンドポイント一覧

### 1. 年運リスト取得

- **エンドポイント**: `GET /api/saju/{id}/year/{daeun_start_age}`
- **認証**: 必須（JWT Bearer Token）
- **説明**: 指定された大運期間（10年分）の年運リストを取得。水平スクロール表示用

#### Request

**パスパラメータ**:
```typescript
{
  id: string;              // 命式ID
  daeun_start_age: number; // 大運開始年齢（例: 28）
}
```

**Headers**:
```
Authorization: Bearer {access_token}
```

**例**:
```
GET /api/saju/001/year/28
```

#### Response

**成功時（200 OK）**:
```typescript
{
  daeunStartAge: number;  // 大運開始年齢
  daeunEndAge: number;    // 大運終了年齢（開始年齢 + 9）
  years: Array<{
    id: number;
    sajuId: string;
    daeunStartAge: number; // この年運が属する大運の開始年齢
    year: number;          // 西暦年（例: 2025）
    age: number;           // その年の年齢
    yearStem: string;      // 年天干
    yearBranch: string;    // 年地支
    sipsin: string;        // 十神（例: "正官"）
    fortuneLevel: '大吉' | '吉' | '平' | '凶' | '大凶';
    isCurrent: boolean;    // 現在の年かどうか
  }>;
}
```

**例**:
```json
{
  "daeunStartAge": 28,
  "daeunEndAge": 37,
  "years": [
    {
      "id": 1,
      "sajuId": "001",
      "daeunStartAge": 28,
      "year": 2018,
      "age": 28,
      "yearStem": "戊",
      "yearBranch": "戌",
      "sipsin": "正官",
      "fortuneLevel": "吉",
      "isCurrent": false
    },
    {
      "id": 2,
      "sajuId": "001",
      "daeunStartAge": 28,
      "year": 2019,
      "age": 29,
      "yearStem": "己",
      "yearBranch": "亥",
      "sipsin": "偏財",
      "fortuneLevel": "平",
      "isCurrent": false
    },
    {
      "id": 3,
      "sajuId": "001",
      "daeunStartAge": 28,
      "year": 2025,
      "age": 35,
      "yearStem": "乙",
      "yearBranch": "巳",
      "sipsin": "食神",
      "fortuneLevel": "大吉",
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

### 2. 月運リスト取得

- **エンドポイント**: `GET /api/saju/{id}/month/{year}`
- **認証**: 必須（JWT Bearer Token）
- **説明**: 指定された年の月運リスト（12ヶ月分）を取得。水平スクロール表示用

#### Request

**パスパラメータ**:
```typescript
{
  id: string;    // 命式ID
  year: number;  // 西暦年（例: 2025）
}
```

**Headers**:
```
Authorization: Bearer {access_token}
```

**例**:
```
GET /api/saju/001/month/2025
```

#### Response

**成功時（200 OK）**:
```typescript
{
  year: number;  // 対象年
  months: Array<{
    id: number;
    sajuId: string;
    year: number;          // 所属する年
    month: number;         // 月（1-12）
    monthStem: string;     // 月天干
    monthBranch: string;   // 月地支
    sipsin: string;        // 十神（例: "正官"）
    fortuneLevel: '大吉' | '吉' | '平' | '凶' | '大凶';
    isCurrent: boolean;    // 現在の月かどうか
  }>;
}
```

**例**:
```json
{
  "year": 2025,
  "months": [
    {
      "id": 1,
      "sajuId": "001",
      "year": 2025,
      "month": 1,
      "monthStem": "戊",
      "monthBranch": "寅",
      "sipsin": "正官",
      "fortuneLevel": "吉",
      "isCurrent": false
    },
    {
      "id": 2,
      "sajuId": "001",
      "year": 2025,
      "month": 2,
      "monthStem": "己",
      "monthBranch": "卯",
      "sipsin": "偏財",
      "fortuneLevel": "平",
      "isCurrent": false
    },
    {
      "id": 11,
      "sajuId": "001",
      "year": 2025,
      "month": 11,
      "monthStem": "戊",
      "monthBranch": "子",
      "sipsin": "食神",
      "fortuneLevel": "大吉",
      "isCurrent": true
    },
    {
      "id": 12,
      "sajuId": "001",
      "year": 2025,
      "month": 12,
      "monthStem": "己",
      "monthBranch": "丑",
      "sipsin": "比肩",
      "fortuneLevel": "吉",
      "isCurrent": false
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

### 3. 日運リスト取得

- **エンドポイント**: `GET /api/saju/{id}/day/{year}/{month}`
- **認証**: 必須（JWT Bearer Token）
- **説明**: 指定された年月の日運リスト（28-31日分）を取得。水平スクロール表示用

#### Request

**パスパラメータ**:
```typescript
{
  id: string;     // 命式ID
  year: number;   // 西暦年（例: 2025）
  month: number;  // 月（1-12）
}
```

**Headers**:
```
Authorization: Bearer {access_token}
```

**例**:
```
GET /api/saju/001/day/2025/11
```

#### Response

**成功時（200 OK）**:
```typescript
{
  year: number;   // 対象年
  month: number;  // 対象月
  days: Array<{
    id: number;
    sajuId: string;
    year: number;          // 所属する年
    month: number;         // 所属する月
    day: number;           // 日（1-31）
    dayStem: string;       // 日天干
    dayBranch: string;     // 日地支
    sipsin: string;        // 十神（例: "正官"）
    fortuneLevel: '大吉' | '吉' | '平' | '凶' | '大凶';
    isToday: boolean;      // 今日かどうか
  }>;
}
```

**例**:
```json
{
  "year": 2025,
  "month": 11,
  "days": [
    {
      "id": 1,
      "sajuId": "001",
      "year": 2025,
      "month": 11,
      "day": 1,
      "dayStem": "甲",
      "dayBranch": "子",
      "sipsin": "正官",
      "fortuneLevel": "吉",
      "isToday": true
    },
    {
      "id": 2,
      "sajuId": "001",
      "year": 2025,
      "month": 11,
      "day": 2,
      "dayStem": "乙",
      "dayBranch": "丑",
      "sipsin": "偏財",
      "fortuneLevel": "平",
      "isToday": false
    },
    {
      "id": 30,
      "sajuId": "001",
      "year": 2025,
      "month": 11,
      "day": 30,
      "dayStem": "癸",
      "dayBranch": "巳",
      "sipsin": "食神",
      "fortuneLevel": "大凶",
      "isToday": false
    }
  ]
}
```

**エラー時（400 Bad Request）**:
```typescript
{
  error: string;  // "不正な年月指定です"
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

## モックサービス参照

実装時はこのモックサービスの挙動を参考にする:
```
frontend/src/services/mock/SajuDetailService.ts
```

主要な関数:
- `getMockYearFortuneList()` - 年運リスト生成
- `getMockMonthFortuneList()` - 月運リスト生成
- `getMockDayFortuneList()` - 日運リスト生成

## データ型定義

実装時はこの型定義を使用する:
```
frontend/src/types/index.ts
```

主要な型:
- `YearFortuneInfo` - 年運情報
- `YearFortuneListResponse` - 年運リストレスポンス
- `MonthFortuneInfo` - 月運情報
- `MonthFortuneListResponse` - 月運リストレスポンス
- `DayFortuneInfo` - 日運情報
- `DayFortuneListResponse` - 日運リストレスポンス
- `FortuneLevel` - 吉凶レベル（'大吉' | '吉' | '平' | '凶' | '大凶'）

---

## 実装時の注意事項

### 1. 年運計算

**年の干支計算**:
- lunar-python の `EightChar` クラスまたは `Solar` クラスを使用
- 年は1月1日〜12月31日（グレゴリオ暦）
- 節入日は考慮しない（年運は太陽年基準）

**計算手順**:
1. 生年月日から生まれた年の西暦を取得
2. 指定された年齢の西暦年を計算: `birth_year + age`
3. その年の干支を取得
4. 日干との関係から十神を判定
5. 天干・地支マトリックスで吉凶判定

**現在の年判定**:
```python
from datetime import datetime
current_year = datetime.now().year
is_current = (year == current_year)
```

### 2. 月運計算

**月の干支計算**:
- 月建法（げっけんほう）を使用
- 1月 = 寅月、2月 = 卯月、...、12月 = 丑月
- 月天干は年天干と月地支から算出

**月天干算出表**（年干×月支）:
```
年干が甲・己: 1月=丙寅、2月=丁卯、3月=戊辰、...
年干が乙・庚: 1月=戊寅、2月=己卯、3月=庚辰、...
年干が丙・辛: 1月=庚寅、2月=辛卯、3月=壬辰、...
年干が丁・壬: 1月=壬寅、2月=癸卯、3月=甲辰、...
年干が戊・癸: 1月=甲寅、2月=乙卯、3月=丙辰、...
```

**現在の月判定**:
```python
from datetime import datetime
now = datetime.now()
is_current = (year == now.year and month == now.month)
```

### 3. 日運計算

**日の干支計算**:
- lunar-python の `Solar` クラスで指定日の干支を取得
- グレゴリオ暦の日付から直接計算

**計算例**:
```python
from lunar_python import Solar

solar = Solar.fromYmd(year, month, day)
day_stem = solar.getDayGan()       # 日天干
day_branch = solar.getDayZhi()     # 日地支
```

**月の日数取得**:
```python
import calendar
days_in_month = calendar.monthrange(year, month)[1]
```

**今日判定**:
```python
from datetime import datetime
now = datetime.now()
is_today = (year == now.year and month == now.month and day == now.day)
```

### 4. 十神（sipsin）計算

**計算方法**:
- 日干を基準（我）とする
- 年運: 年天干と日干の関係
- 月運: 月天干と日干の関係
- 日運: 他の日天干と日干の関係

**十神一覧**:
- 比肩（ひけん）: 同じ天干（陰陽同じ）
- 劫財（ごうざい）: 同じ五行（陰陽異なる）
- 食神（しょくじん）: 我が生じる（陰陽同じ）
- 傷官（しょうかん）: 我が生じる（陰陽異なる）
- 偏財（へんざい）: 我が剋する（陰陽同じ）
- 正財（せいざい）: 我が剋する（陰陽異なる）
- 偏官（へんかん）: 我を剋する（陰陽同じ）
- 正官（せいかん）: 我を剋する（陰陽異なる）
- 偏印（へんいん）: 我を生じる（陰陽同じ）
- 印綬（いんじゅ）: 我を生じる（陰陽異なる）

### 5. 吉凶判定

**ドンサゴン分析法**:
- 天干100マトリックス（10×10）を使用
- 地支144マトリックス（12×12）を使用
- 調候用神80%:原局20%の比重

**判定手順**:
1. 日干×年天干（または月天干・日天干）の組み合わせを取得
2. マトリックスから基本吉凶レベルを取得（1-5）
3. 調候用神を考慮して最終レベルを決定

### 6. パフォーマンス最適化

**キャッシュ戦略**:
- 年運・月運・日運は計算結果をRedisにキャッシュ
- キャッシュキー: `saju:{id}:year:{daeun_start_age}`, `saju:{id}:month:{year}`, `saju:{id}:day:{year}:{month}`
- TTL: 1時間（日運）、1日（月運）、7日（年運）

**バッチ計算**:
- 大運期間の年運10件を一度に計算
- 月運12件、日運28-31件を一度に計算
- データベース問い合わせは1回のみ

### 7. セキュリティ

- JWT トークンで user_id を取得
- 命式の ownership を検証（user_id と saju.user_id が一致）
- 他人の命式データへのアクセスを禁止

### 8. エラーハンドリング

**400 Bad Request**:
```json
{
  "error": "不正な年月指定です"
}
```

**404 Not Found**:
```json
{
  "error": "命式が見つかりません"
}
```

**401 Unauthorized**:
```json
{
  "error": "認証が必要です"
}
```

---

**作成日**: 2025年11月2日
**バージョン**: 1.0
**対応ページ**: P-003（命式詳細・年月日運表示）
