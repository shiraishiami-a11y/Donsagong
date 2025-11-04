# 命式リスト・削除API仕様書

生成日: 2025年11月2日
収集元: frontend/src/services/mock/SajuListService.ts
@MOCK_TO_APIマーク数: 2

## エンドポイント一覧

### 1. 命式リスト取得

- **エンドポイント**: `GET /api/saju/list`
- **認証**: オプション（ゲストモード時は不要、ログイン時はJWT Bearer Token）
- **説明**: 保存された命式の一覧を取得。ゲストモードではLocalStorageから、ログインモードではDBから取得

#### Request

**Headers**（ログイン時のみ）:
```
Authorization: Bearer {access_token}
```

**クエリパラメータ**（オプション）:
```typescript
{
  page?: number;      // ページ番号（デフォルト: 1）
  limit?: number;     // 1ページあたりの件数（デフォルト: 20、最大: 100）
  sortBy?: 'createdAt' | 'birthDatetime' | 'fortuneLevel';  // ソート基準
  order?: 'asc' | 'desc';  // ソート順序（デフォルト: 'desc'）
}
```

**例**:
```
GET /api/saju/list?page=1&limit=20&sortBy=createdAt&order=desc
```

#### Response

**成功時（200 OK）**:
```typescript
{
  items: Array<{
    id: string;              // 命式ID
    name?: string;           // 名前（オプション）
    birthDatetime: string;   // ISO 8601形式
    gender: string;          // 'male' | 'female'
    fortuneLevel: '大吉' | '吉' | '平' | '凶' | '大凶';
    createdAt: string;       // ISO 8601形式

    // 四柱プレビュー用
    yearStem: string;
    yearBranch: string;
    monthStem: string;
    monthBranch: string;
    dayStem: string;
    dayBranch: string;
    hourStem: string;
    hourBranch: string;
  }>;
  total: number;    // 総件数
  page: number;     // 現在のページ番号
  limit: number;    // 1ページあたりの件数
  hasNext: boolean; // 次のページが存在するか
}
```

**例**:
```json
{
  "items": [
    {
      "id": "001",
      "name": "山田 太郎",
      "birthDatetime": "1990-03-15T14:30:00+09:00",
      "gender": "male",
      "fortuneLevel": "吉",
      "yearStem": "庚",
      "yearBranch": "午",
      "monthStem": "己",
      "monthBranch": "卯",
      "dayStem": "丙",
      "dayBranch": "午",
      "hourStem": "乙",
      "hourBranch": "未",
      "createdAt": "2025-11-01T10:00:00+09:00"
    },
    {
      "id": "002",
      "name": "田中 花子",
      "birthDatetime": "1985-06-20T10:00:00+09:00",
      "gender": "female",
      "fortuneLevel": "大吉",
      "yearStem": "乙",
      "yearBranch": "丑",
      "monthStem": "壬",
      "monthBranch": "午",
      "dayStem": "丁",
      "dayBranch": "巳",
      "hourStem": "乙",
      "hourBranch": "巳",
      "createdAt": "2025-10-30T15:30:00+09:00"
    },
    {
      "id": "003",
      "name": null,
      "birthDatetime": "1995-12-05T08:30:00+09:00",
      "gender": "male",
      "fortuneLevel": "凶",
      "yearStem": "乙",
      "yearBranch": "亥",
      "monthStem": "丁",
      "monthBranch": "亥",
      "dayStem": "癸",
      "dayBranch": "亥",
      "hourStem": "甲",
      "hourBranch": "辰",
      "createdAt": "2025-10-28T08:00:00+09:00"
    }
  ],
  "total": 3,
  "page": 1,
  "limit": 20,
  "hasNext": false
}
```

**エラー時（401 Unauthorized）**（ログインモードのみ）:
```typescript
{
  error: string;  // "認証が必要です"
}
```

---

### 2. 命式削除

- **エンドポイント**: `DELETE /api/saju/{id}`
- **認証**: オプション（ゲストモード時は不要、ログイン時はJWT Bearer Token）
- **説明**: 指定された命式IDのデータを削除

#### Request

**パスパラメータ**:
```typescript
{
  id: string;  // 命式ID
}
```

**Headers**（ログイン時のみ）:
```
Authorization: Bearer {access_token}
```

**例**:
```
DELETE /api/saju/001
```

#### Response

**成功時（200 OK）**:
```typescript
{
  success: boolean;  // true
  message: string;   // "命式を削除しました"
}
```

**例**:
```json
{
  "success": true,
  "message": "命式を削除しました"
}
```

**エラー時（404 Not Found）**:
```typescript
{
  success: boolean;  // false
  message: string;   // "命式ID: {id} が見つかりませんでした"
}
```

**エラー時（401 Unauthorized）**（ログインモードのみ）:
```typescript
{
  error: string;  // "認証が必要です"
}
```

**エラー時（403 Forbidden）**（ログインモードのみ）:
```typescript
{
  error: string;  // "この命式を削除する権限がありません"
}
```

---

## モックサービス参照

実装時はこのモックサービスの挙動を参考にする:
```
frontend/src/services/mock/SajuListService.ts
```

## データ型定義

実装時はこの型定義を使用する:
```
frontend/src/types/index.ts
```

主要な型:
- `SajuSummary` - 命式サマリー（リスト表示用）
- `DeleteResponse` - 削除成功レスポンス
- `FortuneLevel` - 吉凶レベル（'大吉' | '吉' | '平' | '凶' | '大凶'）

---

## 実装時の注意事項

### 1. ゲスト/ログインモード対応

**ゲストモード**:
- 認証不要
- LocalStorage からデータ取得（フロントエンド側処理）
- モックサービスでは `localStorage.getItem('golden-saju-list')` を使用

**ログインモード**:
- JWT トークンで認証
- PostgreSQL から取得
- user_id でフィルタリング必須（他人のデータは取得不可）

### 2. ページネーション

**デフォルト値**:
- `page`: 1
- `limit`: 20
- `sortBy`: 'createdAt'
- `order`: 'desc'

**実装例**（SQLAlchemy）:
```python
offset = (page - 1) * limit
query = db.query(Saju).filter(Saju.user_id == user_id)
query = query.order_by(desc(Saju.created_at))
items = query.offset(offset).limit(limit).all()
total = db.query(func.count(Saju.id)).filter(Saju.user_id == user_id).scalar()
```

### 3. ソート機能

**対応フィールド**:
- `createdAt`: 作成日時順
- `birthDatetime`: 生年月日順
- `fortuneLevel`: 吉凶レベル順（5→1 または 1→5）

**fortuneLevel のソート**:
```python
# 吉凶レベルを数値に変換してソート
fortune_map = {'大吉': 5, '吉': 4, '平': 3, '凶': 2, '大凶': 1}
query = query.order_by(
    desc(case(fortune_map, value=Saju.fortune_level))
)
```

### 4. セキュリティ

**ログインモード時**:
- JWT トークンで user_id を取得
- 必ず `WHERE user_id = ?` でフィルタリング
- 他人のデータへのアクセスを禁止

**削除時の権限確認**:
```python
saju = db.query(Saju).filter(Saju.id == id).first()
if not saju:
    return {"success": False, "message": f"命式ID: {id} が見つかりませんでした"}
if saju.user_id != current_user_id:
    raise HTTPException(403, "この命式を削除する権限がありません")
```

### 5. パフォーマンス最適化

**インデックス作成**:
```sql
CREATE INDEX idx_saju_user_id ON saju(user_id);
CREATE INDEX idx_saju_created_at ON saju(created_at DESC);
CREATE INDEX idx_saju_birth_datetime ON saju(birth_datetime);
```

**N+1問題回避**:
- リスト取得時は必要最小限のフィールドのみSELECT
- 詳細情報（daeunList等）は含めない

### 6. 名前が未設定の場合

- `name` フィールドが `null` または空文字の場合
- フロントエンド側で「無題」と表示
- バックエンドは `null` をそのまま返す

### 7. エラーハンドリング

**401 Unauthorized**:
```json
{
  "error": "認証が必要です"
}
```

**403 Forbidden**:
```json
{
  "error": "この命式を削除する権限がありません"
}
```

**404 Not Found**:
```json
{
  "success": false,
  "message": "命式ID: 001 が見つかりませんでした"
}
```

---

**作成日**: 2025年11月2日
**バージョン**: 1.0
**対応ページ**: P-002（命式一覧ページ）
