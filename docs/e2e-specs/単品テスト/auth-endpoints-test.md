# 認証API - 単品エンドポイントテスト仕様書

## 概要

| 項目 | 内容 |
|-----|------|
| テスト対象 | 認証API（4エンドポイント） |
| 対応API仕様書 | `docs/api-specs/auth-api.md` |
| テストツール | Playwright |
| 実装優先度 | 高 |
| 作成日 | 2025年11月2日 |

## テスト対象エンドポイント

| No. | エンドポイント | HTTPメソッド | 説明 | 認証 |
|-----|--------------|-------------|------|------|
| 5.1 | `/api/auth/login` | POST | ログイン | 不要 |
| 5.2 | `/api/auth/register` | POST | 新規登録 | 不要 |
| 4.4 | `/api/auth/logout` | POST | ログアウト | 必要 |
| - | `/api/auth/me` | GET | 現在のユーザー情報取得 | 必要 |

## テストシナリオ

### 5.1: POST /api/auth/login

#### 正常系 - ログイン成功

**リクエスト**:
```json
{
  "email": "test@goldensaju.local",
  "password": "TestGoldenSaju2025!",
  "rememberMe": true
}
```

**期待レスポンス** (`200 OK`):
```typescript
{
  accessToken: string,   // JWT形式
  refreshToken: string,  // JWT形式
  user: {
    id: string,
    email: "test@goldensaju.local",
    role: "user",
    permissions: string[],
    profile: {
      name: string,
      avatar?: string
    },
    createdAt: string
  }
}
```

**Playwrightテストコード**:
```typescript
test('POST /api/auth/login - 正常系', async ({ request }) => {
  const response = await request.post('/api/auth/login', {
    data: {
      email: 'test@goldensaju.local',
      password: 'TestGoldenSaju2025!',
      rememberMe: true
    }
  });

  expect(response.status()).toBe(200);
  const data = await response.json();
  expect(data.accessToken).toBeTruthy();
  expect(data.refreshToken).toBeTruthy();
  expect(data.user.email).toBe('test@goldensaju.local');
  expect(data.user.role).toBe('user');
});
```

#### 異常系 - メールアドレスまたはパスワードが間違っている

**リクエスト**:
```json
{
  "email": "test@goldensaju.local",
  "password": "WrongPassword123!"
}
```

**期待レスポンス** (`401 Unauthorized`):
```json
{
  "error": "メールアドレスまたはパスワードが正しくありません"
}
```

**Playwrightテストコード**:
```typescript
test('POST /api/auth/login - 異常系（パスワード間違い）', async ({ request }) => {
  const response = await request.post('/api/auth/login', {
    data: {
      email: 'test@goldensaju.local',
      password: 'WrongPassword123!'
    }
  });

  expect(response.status()).toBe(401);
  const data = await response.json();
  expect(data.error).toContain('正しくありません');
});
```

#### 異常系 - 未入力フィールド

**リクエスト**:
```json
{
  "email": "test@goldensaju.local"
}
```

**期待レスポンス** (`400 Bad Request`):
```json
{
  "error": "メールアドレスとパスワードは必須です"
}
```

---

### 5.2: POST /api/auth/register

#### 正常系 - 新規登録成功

**リクエスト**:
```json
{
  "email": "newuser@goldensaju.local",
  "password": "NewUser123!",
  "migrateGuestData": false
}
```

**期待レスポンス** (`201 Created`):
```typescript
{
  accessToken: string,
  refreshToken: string,
  user: {
    id: string,
    email: "newuser@goldensaju.local",
    role: "user",
    // ...
  }
}
```

**Playwrightテストコード**:
```typescript
test('POST /api/auth/register - 正常系', async ({ request }) => {
  const response = await request.post('/api/auth/register', {
    data: {
      email: `test-${Date.now()}@goldensaju.local`,  // ユニークなメール
      password: 'NewUser123!',
      migrateGuestData: false
    }
  });

  expect(response.status()).toBe(201);
  const data = await response.json();
  expect(data.accessToken).toBeTruthy();
  expect(data.user.role).toBe('user');
});
```

#### 異常系 - 重複メールアドレス

**期待レスポンス** (`400 Bad Request`):
```json
{
  "error": "このメールアドレスは既に登録されています"
}
```

#### 異常系 - パスワードが弱い

**リクエスト**:
```json
{
  "email": "newuser2@goldensaju.local",
  "password": "123"
}
```

**期待レスポンス** (`400 Bad Request`):
```json
{
  "error": "パスワードは8文字以上で、英大文字・小文字・数字を含む必要があります"
}
```

---

### 4.4: POST /api/auth/logout

#### 正常系 - ログアウト成功

**Headers**:
```
Authorization: Bearer {access_token}
```

**期待レスポンス** (`200 OK`):
```json
{
  "success": true,
  "message": "ログアウトしました"
}
```

**Playwrightテストコード**:
```typescript
test('POST /api/auth/logout - 正常系', async ({ request }) => {
  // 事前にログイン
  const loginRes = await request.post('/api/auth/login', {
    data: {
      email: 'test@goldensaju.local',
      password: 'TestGoldenSaju2025!'
    }
  });
  const { accessToken } = await loginRes.json();

  // ログアウト
  const response = await request.post('/api/auth/logout', {
    headers: {
      Authorization: `Bearer ${accessToken}`
    }
  });

  expect(response.status()).toBe(200);
  const data = await response.json();
  expect(data.success).toBe(true);
  expect(data.message).toContain('ログアウト');
});
```

#### 異常系 - トークンなし

**期待レスポンス** (`401 Unauthorized`):
```json
{
  "error": "認証が必要です"
}
```

---

### GET /api/auth/me

#### 正常系 - ユーザー情報取得成功

**Headers**:
```
Authorization: Bearer {access_token}
```

**期待レスポンス** (`200 OK`):
```typescript
{
  id: string,
  email: "test@goldensaju.local",
  role: "user",
  permissions: string[],
  profile: {
    name: string,
    avatar?: string
  },
  createdAt: string
}
```

**Playwrightテストコード**:
```typescript
test('GET /api/auth/me - 正常系', async ({ request }) => {
  // 事前にログイン
  const loginRes = await request.post('/api/auth/login', {
    data: {
      email: 'test@goldensaju.local',
      password: 'TestGoldenSaju2025!'
    }
  });
  const { accessToken } = await loginRes.json();

  // ユーザー情報取得
  const response = await request.get('/api/auth/me', {
    headers: {
      Authorization: `Bearer ${accessToken}`
    }
  });

  expect(response.status()).toBe(200);
  const data = await response.json();
  expect(data.email).toBe('test@goldensaju.local');
  expect(data.role).toBe('user');
});
```

#### 異常系 - 無効なトークン

**期待レスポンス** (`401 Unauthorized`):
```json
{
  "error": "無効な認証トークンです"
}
```

---

## パフォーマンス要件

| エンドポイント | 閾値 | 理想値 |
|--------------|-----|-------|
| POST /api/auth/login | 500ms | 300ms |
| POST /api/auth/register | 1秒 | 500ms |
| POST /api/auth/logout | 300ms | 200ms |
| GET /api/auth/me | 300ms | 200ms |

---

## セキュリティテスト

### パスワードハッシュ化確認

- ✅ データベースに平文パスワードが保存されていないことを確認
- ✅ bcrypt等の安全なハッシュアルゴリズムを使用していることを確認

### JWT検証

- ✅ トークンが正しい署名アルゴリズムを使用していることを確認
- ✅ トークンに有効期限が設定されていることを確認
- ✅ リフレッシュトークンが正しく機能することを確認

---

## 品質ゲート

- ✅ すべての正常系テストケースが100%成功
- ✅ すべての異常系テストケースが100%成功
- ✅ パフォーマンス要件を満たす
- ✅ セキュリティテスト全項目クリア

---

**作成日**: 2025年11月2日
**バージョン**: 1.0
**テストツール**: Playwright
**対応API仕様書**: `docs/api-specs/auth-api.md`
