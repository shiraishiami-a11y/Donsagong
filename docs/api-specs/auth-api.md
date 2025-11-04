# 認証API仕様書

生成日: 2025年11月2日
収集元: frontend/src/features/auth/services/mockAuthService.ts
@MOCK_TO_APIマーク数: 4

## エンドポイント一覧

### 1. ログイン

- **エンドポイント**: `POST /api/auth/login`
- **認証**: 不要
- **説明**: メールアドレスとパスワードでログインし、アクセストークンとリフレッシュトークンを取得

#### Request

**リクエストボディ**:
```typescript
{
  email: string;
  password: string;
  rememberMe?: boolean;  // オプション: ログイン状態を保持
}
```

**例**:
```json
{
  "email": "test@goldensaju.local",
  "password": "TestGoldenSaju2025!",
  "rememberMe": true
}
```

#### Response

**成功時（200 OK）**:
```typescript
{
  accessToken: string;   // JWT アクセストークン（15分有効）
  refreshToken: string;  // JWT リフレッシュトークン（30日有効）
  user: {
    id: string;
    email: string;
    role: 'guest' | 'user' | 'admin';
    permissions: string[];  // 例: ["read", "write"]
    profile: {
      name: string;
      avatar?: string;     // オプション: プロフィール画像URL
    };
    createdAt: string;     // ISO 8601形式
  };
}
```

**例**:
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "3",
    "email": "test@goldensaju.local",
    "role": "user",
    "permissions": ["read", "write"],
    "profile": {
      "name": "テスト太郎"
    },
    "createdAt": "2025-11-02T10:00:00+09:00"
  }
}
```

**エラー時（401 Unauthorized）**:
```typescript
{
  error: string;  // "メールアドレスまたはパスワードが正しくありません"
}
```

---

### 2. 新規登録

- **エンドポイント**: `POST /api/auth/register`
- **認証**: 不要
- **説明**: 新規ユーザーを登録し、自動的にログイン状態にする。オプションでゲストデータを移行可能

#### Request

**リクエストボディ**:
```typescript
{
  email: string;
  password: string;
  migrateGuestData?: boolean;  // オプション: LocalStorageのゲストデータを移行
}
```

**例**:
```json
{
  "email": "newuser@goldensaju.local",
  "password": "SecurePass2025!",
  "migrateGuestData": true
}
```

#### Response

**成功時（201 Created）**:
```typescript
{
  accessToken: string;
  refreshToken: string;
  user: {
    id: string;
    email: string;
    role: 'user';  // 新規登録時は必ず'user'
    permissions: string[];  // ["read", "write"]
    profile: {
      name: string;  // メールアドレスのローカル部分（@の前）
      avatar?: string;
    };
    createdAt: string;
  };
}
```

**エラー時（409 Conflict）**:
```typescript
{
  error: string;  // "このメールアドレスは既に登録されています"
}
```

**エラー時（400 Bad Request）**:
```typescript
{
  error: string;  // "パスワードは8文字以上である必要があります"
}
```

---

### 3. ログアウト

- **エンドポイント**: `POST /api/auth/logout`
- **認証**: 必須（JWT Bearer Token）
- **説明**: 現在のセッションをログアウトし、リフレッシュトークンを無効化

#### Request

**Headers**:
```
Authorization: Bearer {access_token}
```

#### Response

**成功時（200 OK）**:
```typescript
{
  success: boolean;  // true
  message: string;   // "ログアウトしました"
}
```

**エラー時（401 Unauthorized）**:
```typescript
{
  error: string;  // "認証が必要です"
}
```

---

### 4. 現在のユーザー情報取得

- **エンドポイント**: `GET /api/auth/me`
- **認証**: 必須（JWT Bearer Token）
- **説明**: アクセストークンから現在のユーザー情報を取得

#### Request

**Headers**:
```
Authorization: Bearer {access_token}
```

#### Response

**成功時（200 OK）**:
```typescript
{
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
```

**例**:
```json
{
  "id": "3",
  "email": "test@goldensaju.local",
  "role": "user",
  "permissions": ["read", "write"],
  "profile": {
    "name": "テスト太郎"
  },
  "createdAt": "2025-11-02T10:00:00+09:00"
}
```

**エラー時（401 Unauthorized）**:
```typescript
{
  error: string;  // "ユーザーが見つかりません"
}
```

---

## モックサービス参照

実装時はこのモックサービスの挙動を参考にする:
```
frontend/src/features/auth/services/mockAuthService.ts
```

## データ型定義

実装時はこの型定義を使用する:
```
frontend/src/types/index.ts
```

主要な型:
- `User` - ユーザー情報
- `AuthResponse` - 認証レスポンス（トークン + ユーザー）
- `LoginRequest` - ログインリクエスト
- `RegisterRequest` - 新規登録リクエスト

---

## 実装時の注意事項

### 1. JWT トークン管理

**アクセストークン**:
- 有効期限: 15分（`ACCESS_TOKEN_EXPIRE_MINUTES=15`）
- ペイロード: `{ user_id, email, role, exp, iat }`
- アルゴリズム: HS256
- SECRET_KEY は環境変数で管理

**リフレッシュトークン**:
- 有効期限: 30日（`REFRESH_TOKEN_EXPIRE_DAYS=30`）
- PostgreSQL の `refresh_tokens` テーブルで管理
- ログアウト時に無効化必須

### 2. パスワードセキュリティ

- bcrypt または Argon2 でハッシュ化
- ソルトラウンド: 12以上
- パスワードポリシー: 8文字以上
- 生パスワードをログに残さない

### 3. バリデーション

**メールアドレス**:
- RFC 5322 準拠の正規表現
- 既存ユーザーとの重複チェック

**パスワード**:
- 最小長: 8文字
- 推奨: 大文字・小文字・数字を含む

### 4. ゲストデータ移行

新規登録時に `migrateGuestData: true` が送信された場合:
1. リクエストボディに `guestData` フィールドを追加可能
2. サーバー側でトランザクション処理（全成功または全失敗）
3. 移行完了後、クライアント側で LocalStorage をクリア

**拡張リクエスト例**:
```json
{
  "email": "newuser@goldensaju.local",
  "password": "SecurePass2025!",
  "migrateGuestData": true,
  "guestData": [
    {
      "id": "guest-001",
      "birthDatetime": "1990-03-15T14:30:00+09:00",
      "gender": "male",
      "name": "テスト太郎",
      ...
    }
  ]
}
```

### 5. セキュリティ

- HTTPS 必須（本番環境）
- CORS 設定: 許可するオリジンを環境変数で管理
- レート制限: ログイン試行は IP ごとに制限（5回/分）
- セッション管理: リフレッシュトークンを DB で管理し、ログアウト時に削除

### 6. エラーハンドリング

すべてのエラーレスポンスは以下の形式:
```json
{
  "error": "エラーメッセージ"
}
```

HTTPステータスコード:
- 200: 成功（ログイン、ログアウト、ユーザー情報取得）
- 201: 成功（新規登録）
- 400: バリデーションエラー
- 401: 認証エラー
- 409: 重複エラー（メールアドレス既存）
- 500: サーバーエラー

---

**作成日**: 2025年11月2日
**バージョン**: 1.0
**対応ページ**: P-005（ログインページ）、P-006（新規登録ページ）
