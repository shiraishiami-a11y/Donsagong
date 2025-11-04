# 設定・データ管理API仕様書

生成日: 2025年11月2日
収集元: frontend/src/services/mock/SettingsService.ts
@MOCK_TO_APIマーク数: 4

## エンドポイント一覧

### 1. パスワード変更

- **エンドポイント**: `PUT /api/user/password`
- **認証**: 必須（JWT Bearer Token）
- **説明**: ログインユーザーのパスワードを変更

#### Request

**Headers**:
```
Authorization: Bearer {access_token}
```

**リクエストボディ**:
```typescript
{
  oldPassword: string;  // 現在のパスワード
  newPassword: string;  // 新しいパスワード（8文字以上）
}
```

**例**:
```json
{
  "oldPassword": "OldPassword123!",
  "newPassword": "NewSecurePassword2025!"
}
```

#### Response

**成功時（200 OK）**:
```typescript
{
  success: boolean;  // true
  message: string;   // "パスワードを変更しました"
}
```

**例**:
```json
{
  "success": true,
  "message": "パスワードを変更しました"
}
```

**エラー時（400 Bad Request）**:
```typescript
{
  success: boolean;  // false
  message: string;   // "パスワードを入力してください"
                     // "パスワードは8文字以上である必要があります"
}
```

**エラー時（401 Unauthorized）**:
```typescript
{
  success: boolean;  // false
  message: string;   // "現在のパスワードが正しくありません"
}
```

---

### 2. データエクスポート

- **エンドポイント**: `GET /api/saju/export`
- **認証**: 必須（JWT Bearer Token）
- **説明**: ログインユーザーの全命式データをJSON形式でエクスポート

#### Request

**Headers**:
```
Authorization: Bearer {access_token}
```

**クエリパラメータ**（オプション）:
```typescript
{
  format?: 'json' | 'csv';  // エクスポート形式（デフォルト: 'json'）
}
```

**例**:
```
GET /api/saju/export?format=json
```

#### Response

**成功時（200 OK）**:

**Content-Type**: `application/json` または `text/csv`

**JSON形式の例**:
```json
{
  "version": "1.0.0",
  "exportDate": "2025-11-02T10:00:00+09:00",
  "data": [
    {
      "id": "001",
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
      "createdAt": "2025-11-01T10:00:00+09:00",
      "daeunNumber": 7,
      "isForward": true,
      "afterBirthYears": 7,
      "afterBirthMonths": 5,
      "afterBirthDays": 2,
      "firstDaeunDate": "1997-08-17"
    }
  ]
}
```

**エラー時（401 Unauthorized）**:
```typescript
{
  error: string;  // "認証が必要です"
}
```

---

### 3. データインポート

- **エンドポイント**: `POST /api/saju/import`
- **認証**: 必須（JWT Bearer Token）
- **説明**: JSON形式の命式データをインポート。重複チェック後にマージ

#### Request

**Headers**:
```
Authorization: Bearer {access_token}
Content-Type: multipart/form-data
```

**リクエストボディ**（multipart/form-data）:
```typescript
{
  file: File;  // JSONファイル（application/json）
}
```

**JSONファイル形式**:
```json
{
  "version": "1.0.0",
  "exportDate": "2025-11-02T10:00:00+09:00",
  "data": [
    {
      "id": "001",
      "name": "山田 太郎",
      "birthDatetime": "1990-03-15T14:30:00+09:00",
      "gender": "male",
      ...
    }
  ]
}
```

#### Response

**成功時（200 OK）**:
```typescript
{
  success: boolean;      // true
  importedCount: number; // インポートされた件数
  message: string;       // "3件のデータをインポートしました"
}
```

**例**:
```json
{
  "success": true,
  "importedCount": 3,
  "message": "3件のデータをインポートしました"
}
```

**エラー時（400 Bad Request）**:
```typescript
{
  success: boolean;      // false
  importedCount: number; // 0
  message: string;       // "ファイル形式が正しくありません"
                         // "ファイルの読み込みに失敗しました"
}
```

**エラー時（401 Unauthorized）**:
```typescript
{
  error: string;  // "認証が必要です"
}
```

---

### 4. ユーザー設定更新

- **エンドポイント**: `PUT /api/user/settings`
- **認証**: 必須（JWT Bearer Token）
- **説明**: ユーザーの設定（ログイン保持、セッション期間等）を更新

#### Request

**Headers**:
```
Authorization: Bearer {access_token}
```

**リクエストボディ**:
```typescript
{
  rememberMe: boolean;                      // ログイン状態を保持
  sessionDuration: '7d' | '30d' | 'forever'; // セッション期間
}
```

**例**:
```json
{
  "rememberMe": true,
  "sessionDuration": "30d"
}
```

#### Response

**成功時（200 OK）**:
```typescript
{
  success: boolean;  // true
  message: string;   // "設定を更新しました"
}
```

**例**:
```json
{
  "success": true,
  "message": "設定を更新しました"
}
```

**エラー時（400 Bad Request）**:
```typescript
{
  success: boolean;  // false
  message: string;   // "不正な設定値です"
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
frontend/src/services/mock/SettingsService.ts
```

主要な関数:
- `mockChangePassword()` - パスワード変更
- `mockExportData()` - データエクスポート
- `mockImportData()` - データインポート
- `mockUpdateSettings()` - 設定更新
- `mockGetSettings()` - 設定取得（補助関数）

## データ型定義

実装時はこの型定義を使用する:
```
frontend/src/types/index.ts
```

主要な型:
- `UpdateResponse` - 更新成功レスポンス
- `ImportResponse` - インポート成功レスポンス
- `UserSettings` - ユーザー設定
- `SajuResponse` - 命式データ（エクスポート/インポート用）

---

## 実装時の注意事項

### 1. パスワード変更

**セキュリティ要件**:
- 現在のパスワードを必ず検証
- bcrypt または Argon2 でハッシュ化
- パスワード履歴チェック（過去3回分と同じは禁止）
- パスワード変更後は全トークンを無効化（再ログイン必須）

**バリデーション**:
```python
# 現在のパスワード検証
if not verify_password(old_password, user.hashed_password):
    return {"success": False, "message": "現在のパスワードが正しくありません"}

# 新しいパスワードのバリデーション
if len(new_password) < 8:
    return {"success": False, "message": "パスワードは8文字以上である必要があります"}

# パスワードハッシュ化
hashed_password = hash_password(new_password)
```

**トークン無効化**:
```python
# すべてのリフレッシュトークンを削除
db.query(RefreshToken).filter(RefreshToken.user_id == user.id).delete()
db.commit()
```

### 2. データエクスポート

**エクスポート形式**:

**JSON**:
- すべてのフィールドを含む完全なデータ
- バージョン情報とエクスポート日時を付加
- `Content-Type: application/json`
- `Content-Disposition: attachment; filename="saju_export_YYYYMMDD.json"`

**CSV（オプション）**:
- 基本情報のみ（id, name, birthDatetime, gender, fortuneLevel, createdAt）
- 四柱情報（8列）
- `Content-Type: text/csv; charset=utf-8`
- `Content-Disposition: attachment; filename="saju_export_YYYYMMDD.csv"`

**実装例**:
```python
from datetime import datetime
from fastapi.responses import StreamingResponse
import json

@app.get("/api/saju/export")
async def export_data(user_id: str = Depends(get_current_user_id)):
    # ユーザーの全命式データを取得
    saju_list = db.query(Saju).filter(Saju.user_id == user_id).all()

    export_data = {
        "version": "1.0.0",
        "exportDate": datetime.now().isoformat(),
        "data": [saju.to_dict() for saju in saju_list]
    }

    json_str = json.dumps(export_data, ensure_ascii=False, indent=2)

    return StreamingResponse(
        iter([json_str]),
        media_type="application/json",
        headers={
            "Content-Disposition": f"attachment; filename=saju_export_{datetime.now().strftime('%Y%m%d')}.json"
        }
    )
```

### 3. データインポート

**インポート処理フロー**:
1. ファイルアップロード受信
2. JSON形式バリデーション
3. バージョン互換性チェック
4. データ構造バリデーション（SajuResponse 型に準拠）
5. 重複チェック（ID または birthDatetime + gender）
6. トランザクション開始
7. データベース挿入
8. トランザクションコミット（全成功または全失敗）

**重複チェック**:
```python
existing_ids = {saju.id for saju in db.query(Saju.id).filter(Saju.user_id == user_id).all()}
new_data = [item for item in import_data["data"] if item["id"] not in existing_ids]
```

**トランザクション管理**:
```python
from sqlalchemy.exc import SQLAlchemyError

try:
    for item in new_data:
        saju = Saju(
            id=item["id"],
            user_id=user_id,
            name=item.get("name"),
            birth_datetime=item["birthDatetime"],
            gender=item["gender"],
            ...
        )
        db.add(saju)

    db.commit()
    return {
        "success": True,
        "importedCount": len(new_data),
        "message": f"{len(new_data)}件のデータをインポートしました"
    }
except SQLAlchemyError as e:
    db.rollback()
    return {
        "success": False,
        "importedCount": 0,
        "message": "インポート中にエラーが発生しました"
    }
```

### 4. ユーザー設定更新

**設定項目**:

**rememberMe**:
- `true`: リフレッシュトークンの有効期限を延長
- `false`: リフレッシュトークンの有効期限を短縮（7日）

**sessionDuration**:
- `'7d'`: 7日間
- `'30d'`: 30日間
- `'forever'`: 無期限（実際は365日）

**実装例**:
```python
@app.put("/api/user/settings")
async def update_settings(
    settings: UserSettings,
    user_id: str = Depends(get_current_user_id)
):
    # バリデーション
    if settings.sessionDuration not in ['7d', '30d', 'forever']:
        return {"success": False, "message": "不正な設定値です"}

    # 設定を保存
    user = db.query(User).filter(User.id == user_id).first()
    user.settings = settings.dict()
    db.commit()

    return {"success": True, "message": "設定を更新しました"}
```

### 5. セキュリティ

**認証必須**:
- すべてのエンドポイントで JWT トークン検証
- user_id でデータをフィルタリング（他人のデータへのアクセス禁止）

**ファイルアップロード制限**:
- 最大ファイルサイズ: 10MB
- 許可する MIME タイプ: `application/json` のみ
- ファイル名のサニタイズ

### 6. エラーハンドリング

**400 Bad Request**:
```json
{
  "success": false,
  "message": "ファイル形式が正しくありません"
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
  "message": "サーバーエラーが発生しました"
}
```

---

**作成日**: 2025年11月2日
**バージョン**: 1.0
**対応ページ**: P-004（設定ページ）
