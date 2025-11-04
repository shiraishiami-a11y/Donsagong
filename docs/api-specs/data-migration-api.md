# データ移行API仕様書

生成日: 2025年11月2日
収集元: frontend/src/features/auth/contexts/AuthContext.tsx, frontend/src/pages/RegisterPage.tsx
@MOCK_TO_APIマーク数: 1

## エンドポイント一覧

### 1. ゲストデータ移行

- **エンドポイント**: `POST /api/saju/migrate`
- **認証**: 必須（JWT Bearer Token）
- **説明**: 新規登録時にLocalStorageに保存されたゲストデータをクラウド（PostgreSQL）に移行する

#### Request

**Headers**:
```
Authorization: Bearer {access_token}
```

**リクエストボディ**:
```typescript
{
  guestData: Array<{
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
  }>;
}
```

**例**:
```json
{
  "guestData": [
    {
      "id": "guest-001",
      "name": "テスト太郎",
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
      "daeunList": [
        {
          "id": 1,
          "sajuId": "guest-001",
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
      "createdAt": "2025-11-01T10:00:00+09:00",
      "daeunNumber": 7,
      "isForward": true,
      "afterBirthYears": 7,
      "afterBirthMonths": 5,
      "afterBirthDays": 2,
      "firstDaeunDate": "1997-08-17"
    },
    {
      "id": "guest-002",
      "name": "テスト花子",
      "birthDatetime": "1985-06-20T10:00:00+09:00",
      "gender": "female",
      "yearStem": "乙",
      "yearBranch": "丑",
      "monthStem": "壬",
      "monthBranch": "午",
      "dayStem": "丁",
      "dayBranch": "巳",
      "hourStem": "乙",
      "hourBranch": "巳",
      "daeunList": [...],
      "fortuneLevel": "大吉",
      "createdAt": "2025-10-30T15:30:00+09:00",
      "daeunNumber": 5,
      "isForward": false,
      "afterBirthYears": 5,
      "afterBirthMonths": 3,
      "afterBirthDays": 10,
      "firstDaeunDate": "1990-09-30"
    }
  ]
}
```

#### Response

**成功時（200 OK）**:
```typescript
{
  success: boolean;      // true
  migratedCount: number; // 移行された件数
  message: string;       // "2件のデータを移行しました"
}
```

**例**:
```json
{
  "success": true,
  "migratedCount": 2,
  "message": "2件のデータを移行しました"
}
```

**エラー時（400 Bad Request）**:
```typescript
{
  success: boolean;      // false
  migratedCount: number; // 0
  message: string;       // "移行データが不正です"
                         // "guestDataは配列である必要があります"
}
```

**エラー時（401 Unauthorized）**:
```typescript
{
  error: string;  // "認証が必要です"
}
```

**エラー時（409 Conflict）**:
```typescript
{
  success: boolean;      // false
  migratedCount: number; // 部分的に成功した件数
  message: string;       // "一部のデータが既に存在します（2件中1件移行）"
}
```

**エラー時（500 Internal Server Error）**:
```typescript
{
  success: boolean;      // false
  migratedCount: number; // 0
  message: string;       // "移行中にエラーが発生しました"
}
```

---

## モックサービス参照

実装時はこのモックサービスの挙動を参考にする:
```
frontend/src/features/auth/contexts/AuthContext.tsx
frontend/src/pages/RegisterPage.tsx
```

関連機能:
- `RegisterRequest.migrateGuestData` - 新規登録時の移行フラグ
- `AuthContext.register()` - 登録処理内での移行呼び出し

## データ型定義

実装時はこの型定義を使用する:
```
frontend/src/types/index.ts
```

主要な型:
- `MigrateResponse` - 移行成功レスポンス
- `SajuResponse` - 命式データ
- `DaeunInfo` - 大運情報
- `FortuneLevel` - 吉凶レベル（'大吉' | '吉' | '平' | '凶' | '大凶'）

---

## 実装時の注意事項

### 1. 移行処理フロー

**新規登録時の統合処理**:

1. クライアント側（RegisterPage）:
   - `migrateGuestData` チェックボックスが ON の場合
   - LocalStorage から `golden-saju-list` を取得
   - `RegisterRequest` に含める（または登録後に `/api/saju/migrate` を呼び出す）

2. サーバー側（新規登録API）:
   - ユーザーアカウントを作成
   - `migrateGuestData: true` の場合は移行処理を実行
   - トランザクション管理（ユーザー作成と移行は同一トランザクション）

**実装例**:
```python
from sqlalchemy.exc import SQLAlchemyError

@app.post("/api/auth/register")
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    try:
        # ユーザー作成
        user = User(
            email=request.email,
            hashed_password=hash_password(request.password),
            role='user',
            ...
        )
        db.add(user)
        db.flush()  # user.id を取得

        # ゲストデータ移行
        if request.migrateGuestData and request.guestData:
            migrate_count = 0
            for guest_saju in request.guestData:
                # 新しいIDを生成（ゲストIDは使用しない）
                new_saju = Saju(
                    id=generate_uuid(),
                    user_id=user.id,
                    name=guest_saju.get('name'),
                    birth_datetime=guest_saju['birthDatetime'],
                    gender=guest_saju['gender'],
                    ...
                )
                db.add(new_saju)
                migrate_count += 1

        db.commit()

        # JWT トークン生成
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        return AuthResponse(
            accessToken=access_token,
            refreshToken=refresh_token,
            user=user.to_dict()
        )

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(500, "登録中にエラーが発生しました")
```

### 2. トランザクション管理

**全成功または全失敗**:
- ユーザー作成とデータ移行は同一トランザクション
- 移行中にエラーが発生した場合、ユーザー作成もロールバック
- 部分的な成功は許可しない（一貫性を保つ）

**例外処理**:
```python
try:
    # ユーザー作成
    user = create_user(...)
    db.add(user)
    db.flush()

    # データ移行
    for guest_data in request.guestData:
        saju = create_saju(user.id, guest_data)
        db.add(saju)

    # 全て成功したらコミット
    db.commit()
except Exception as e:
    # エラー時はロールバック
    db.rollback()
    raise HTTPException(500, "移行中にエラーが発生しました")
```

### 3. ID 変換

**ゲストIDからユーザーIDへ**:
- ゲストモードの ID（例: `guest-001`）は使用しない
- 新しい UUID を生成して割り当て
- 大運リストの `sajuId` も新しい ID に更新

**実装例**:
```python
import uuid

def migrate_saju(user_id: str, guest_saju: dict) -> Saju:
    # 新しいIDを生成
    new_id = str(uuid.uuid4())

    # 大運リストのsajuIdを更新
    daeun_list = guest_saju.get('daeunList', [])
    for daeun in daeun_list:
        daeun['sajuId'] = new_id

    # Saju オブジェクト作成
    return Saju(
        id=new_id,
        user_id=user_id,
        name=guest_saju.get('name'),
        birth_datetime=guest_saju['birthDatetime'],
        ...
    )
```

### 4. データバリデーション

**必須フィールドチェック**:
```python
required_fields = ['birthDatetime', 'gender', 'yearStem', 'yearBranch', ...]

for guest_saju in request.guestData:
    for field in required_fields:
        if field not in guest_saju:
            raise HTTPException(400, f"移行データに{field}が不足しています")
```

**型チェック**:
```python
from pydantic import ValidationError

try:
    validated_data = [SajuResponse(**item) for item in request.guestData]
except ValidationError as e:
    raise HTTPException(400, "移行データの形式が不正です")
```

### 5. 重複チェック

**同一データの検出**:
- `birthDatetime` + `gender` の組み合わせで判定
- 既に同じデータが存在する場合はスキップ（エラーにしない）

**実装例**:
```python
existing_keys = {
    (saju.birth_datetime, saju.gender)
    for saju in db.query(Saju).filter(Saju.user_id == user.id).all()
}

unique_data = [
    item for item in request.guestData
    if (item['birthDatetime'], item['gender']) not in existing_keys
]
```

### 6. クライアント側の処理

**移行完了後の LocalStorage クリア**:
```typescript
// 新規登録成功後
if (migrateGuestData) {
  localStorage.removeItem('golden-saju-list');
  localStorage.removeItem('saju_list');
}
```

**移行データの収集**:
```typescript
const guestData = JSON.parse(localStorage.getItem('golden-saju-list') || '[]');
const registerRequest: RegisterRequest = {
  email,
  password,
  migrateGuestData: true,
  guestData  // 追加フィールド
};
```

### 7. セキュリティ

**認証必須**:
- 新規登録直後のユーザーのみ実行可能
- JWT トークンで user_id を検証

**データサニタイゼーション**:
- SQL インジェクション対策（ORM使用）
- XSS 対策（name フィールドのサニタイズ）

**データサイズ制限**:
- 最大100件まで（大量データの移行を防ぐ）
- リクエストサイズ: 最大10MB

### 8. エラーハンドリング

**400 Bad Request**:
```json
{
  "success": false,
  "migratedCount": 0,
  "message": "移行データが不正です"
}
```

**401 Unauthorized**:
```json
{
  "error": "認証が必要です"
}
```

**500 Internal Server Error**:
```json
{
  "success": false,
  "migratedCount": 0,
  "message": "移行中にエラーが発生しました"
}
```

---

## 使用例

### 新規登録時の完全フロー

**1. クライアント側（RegisterPage）**:
```typescript
const handleRegister = async (e: React.FormEvent) => {
  e.preventDefault();

  // LocalStorageからゲストデータ取得
  const guestData = migrateData
    ? JSON.parse(localStorage.getItem('golden-saju-list') || '[]')
    : [];

  try {
    // 新規登録 + 移行
    await register({
      email,
      password,
      migrateGuestData: migrateData,
      guestData
    });

    // 成功後、LocalStorageクリア
    if (migrateData) {
      localStorage.removeItem('golden-saju-list');
    }

    navigate('/list');
  } catch (err) {
    setError('登録に失敗しました');
  }
};
```

**2. サーバー側（FastAPI）**:
```python
@app.post("/api/auth/register", response_model=AuthResponse)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    # メール重複チェック
    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(409, "このメールアドレスは既に登録されています")

    try:
        # ユーザー作成
        user = User(
            email=request.email,
            hashed_password=hash_password(request.password),
            role='user',
            permissions=['read', 'write'],
            profile={'name': request.email.split('@')[0]}
        )
        db.add(user)
        db.flush()

        # ゲストデータ移行
        migrate_count = 0
        if request.migrateGuestData and request.guestData:
            for guest_saju in request.guestData:
                new_saju = Saju(
                    id=str(uuid.uuid4()),
                    user_id=user.id,
                    **guest_saju
                )
                db.add(new_saju)
                migrate_count += 1

        db.commit()

        # トークン生成
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        return AuthResponse(
            accessToken=access_token,
            refreshToken=refresh_token,
            user=user.to_dict()
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(500, "登録中にエラーが発生しました")
```

---

**作成日**: 2025年11月2日
**バージョン**: 1.0
**対応ページ**: P-006（新規登録ページ）
