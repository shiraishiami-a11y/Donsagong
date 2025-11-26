# E2Eテスト ベストプラクティス

**プロジェクト名**: ゴールデン四柱推命アプリケーション
**作成日**: 2025-11-11
**最終更新**: 2025-11-11

---

## 📌 このドキュメントについて

このファイルは、E2Eテスト実装時に成功したパターンを自動的に蓄積する場所です。

**目的**:
- 成功パターンを記録し、後続テストの試行錯誤を削減
- デバッグマスターが解決した問題を組織的知識として保存
- プロジェクト全体のテスト品質を向上

**更新ルール**:
- デバッグマスターが問題解決時に自動更新
- E2Eテスト実装エージェントが新しいパターン発見時に追記
- オーケストレーターは参照のみ（編集しない）

---

## 1. サーバー起動パターン

### 1.1 フロントエンドサーバー起動

**成功パターン**:
- ポート: 3247（CLAUDE.mdで定義）
- コマンド: `npm run dev` または `cd frontend && npm run dev`
- 起動確認: `http://localhost:3247` でレスポンスを確認

**注意事項**:
- バックグラウンド実行時は `&` を使用
- 起動完了まで5-10秒待機
- ポート競合時は既存プロセスをkill

---

### 1.2 バックエンドサーバー起動

**成功パターン**:
- ポート: 8432（CLAUDE.mdで定義）
- コマンド: `cd backend && uvicorn app.main:app --reload --port 8432`
- 起動確認: `http://localhost:8432/docs` でSwagger UIにアクセス

**注意事項**:
- Python仮想環境の有効化が必須
- データベース接続設定を事前確認
- 環境変数（.env.local）の読み込みを確認

---

## 2. ページアクセスパターン

### 2.1 トップページ（/）

**成功パターン**:
```typescript
await page.goto('http://localhost:3247/');
await page.waitForSelector('input[name="birthDate"]', { timeout: 10000 });
```

**注意事項**:
- 初回アクセスは読み込みに時間がかかる場合あり
- waitForSelector でDOM要素の表示を確認

---

### 2.2 命式詳細ページ（/saju/:id）

**成功パターン**:
```typescript
// LocalStorageに保存されたIDを取得
const savedData = await page.evaluate(() => {
  const data = localStorage.getItem('sajuData');
  return data ? JSON.parse(data) : null;
});
const sajuId = savedData[0]?.id;
await page.goto(`http://localhost:3247/saju/${sajuId}`);
```

**注意事項**:
- IDの存在確認を事前に実施
- 存在しないIDでアクセスするとエラーページへ遷移

---

## 3. 認証処理パターン

### 3.1 ログイン処理

**成功パターン**:
```typescript
await page.goto('http://localhost:3247/login');
await page.fill('input[name="email"]', 'test@goldensaju.local');
await page.fill('input[name="password"]', 'TestGoldenSaju2025!');
await page.click('button[type="submit"]');
await page.waitForURL('**/list', { timeout: 10000 });
```

**注意事項**:
- テストアカウントはCLAUDE.mdで定義
- ログイン成功後は /list へ自動遷移
- JWT トークンはLocalStorageに保存

---

### 3.2 ログアウト処理

**成功パターン**:
```typescript
await page.click('[data-testid="logout-button"]');
await page.waitForURL('**/', { timeout: 5000 });
```

**注意事項**:
- ログアウト後、LocalStorageからトークンが削除される
- トップページ（/）へリダイレクト

---

## 4. UI操作パターン

### 4.1 フォーム入力

**成功パターン**:
```typescript
// 生年月日入力
await page.fill('input[name="birthDate"]', '1990-03-15');
await page.fill('input[name="birthTime"]', '14:30');

// 性別選択
await page.click('[data-testid="gender-male"]');

// 送信
await page.click('button[type="submit"]');
```

**注意事項**:
- 日時入力は ISO 8601 形式（YYYY-MM-DD, HH:mm）
- ボタンは data-testid 属性で特定するのが確実

---

### 4.2 スクロール操作

**成功パターン**:
```typescript
const scrollContainer = await page.locator('[data-testid="year-scroll-section"]');
await scrollContainer.scrollIntoViewIfNeeded();
await scrollContainer.evaluate(el => el.scrollLeft = 200);
```

**注意事項**:
- 横スクロールは scrollLeft を使用
- スクロール後、少し待機してレンダリング完了を確認

---

### 4.3 削除ボタンのクリック

**成功パターン**:
```typescript
const deleteButton = await page.locator('[data-testid="delete-button"]').first();
await deleteButton.click();
await page.click('button:has-text("削除")'); // 確認ダイアログ
await page.waitForResponse(response =>
  response.url().includes('/api/saju/') && response.request().method() === 'DELETE'
);
```

**注意事項**:
- 確認ダイアログの表示を待機
- API応答を確認してから次のステップへ

---

## 5. API応答確認パターン

### 5.1 POST /api/saju/calculate

**成功パターン**:
```typescript
const response = await page.waitForResponse(
  response => response.url().includes('/api/saju/calculate') && response.status() === 200,
  { timeout: 30000 }
);
const data = await response.json();
expect(data).toHaveProperty('pillars');
```

**注意事項**:
- 計算APIは応答に時間がかかる場合あり（timeout 30秒推奨）
- レスポンスの構造を事前確認

---

### 5.2 GET /api/saju/list

**成功パターン**:
```typescript
const response = await page.waitForResponse(
  response => response.url().includes('/api/saju/list') && response.status() === 200
);
const data = await response.json();
expect(Array.isArray(data)).toBe(true);
```

**注意事項**:
- 認証が必要（Authorizationヘッダー）
- 空配列が返る場合もあり

---

## 6. トラブルシューティング

### 6.1 TimeoutError: page.waitForResponse

**原因**:
- APIエンドポイントが未実装
- ネットワークエラー
- フロントエンドでAPIが呼び出されていない

**解決策**:
1. バックエンドのエンドポイント存在確認（curl）
2. ブラウザのネットワークタブで実際のリクエストを確認
3. フロントエンドのコードで API呼び出し箇所を確認

---

### 6.2 Locator not found: [data-testid="..."]

**原因**:
- data-testid 属性が未実装
- 要素のレンダリング前にアクセス
- 条件付きレンダリングで非表示

**解決策**:
1. 該当コンポーネントに data-testid を追加
2. waitForSelector でDOM表示を待機
3. 条件を満たすようにテストデータを調整

---

### 6.3 スクロール操作が効かない

**原因**:
- 親コンテナに `maxWidth: '100%'` が設定され、子要素が横にはみ出せない
- overflow-x が hidden になっている

**解決策**:
1. 親コンテナの maxWidth 制限を削除（xs ブレークポイント）
2. overflow-x: auto を設定
3. webkit-overflow-scrolling: touch を追加（iOS対応）

---

## 7. 成功事例

（デバッグマスターが問題解決時に自動で追記されます）

---

**次回更新**: デバッグマスター実行時に自動更新
