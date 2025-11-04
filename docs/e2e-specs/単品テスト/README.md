# 単品エンドポイントテスト仕様書 - 概要

## 目的

連鎖テストとは別に、個別のAPIエンドポイントの動作を単体でテストするための仕様書です。

## テスト種別

| ファイル名 | 対象API | エンドポイント数 | 説明 |
|----------|--------|----------------|------|
| `auth-endpoints-test.md` | 認証API | 4 | login, register, logout, me |
| `saju-calculation-test.md` | 命式計算・保存API | 2 | calculate, save |
| `saju-list-test.md` | 命式リスト・削除API | 2 | list, delete |
| `saju-detail-test.md` | 命式詳細API | 3 | detail, daeun, current |
| `saju-fortune-test.md` | 年月日運API | 3 | year, month, day |
| `settings-test.md` | 設定・データ管理API | 4 | password, export, import, settings |
| `data-migration-test.md` | データ移行API | 1 | migrate |

**合計**: 19エンドポイント

## テスト方針

### 単品テストの目的

- 各エンドポイントが正しいレスポンスを返すことを確認
- エラーハンドリングが正しく動作することを確認
- バリデーションが正しく機能することを確認
- パフォーマンス要件を満たすことを確認

### 連鎖テストとの違い

| 項目 | 連鎖テスト | 単品テスト |
|------|----------|----------|
| 目的 | ユーザーフロー全体の動作確認 | 個別エンドポイントの動作確認 |
| テスト範囲 | 複数エンドポイント | 単一エンドポイント |
| 依存関係 | あり（前のAPIの結果を使用） | なし（独立） |
| テストデータ | フロー全体で共有 | エンドポイントごとに独立 |
| 実行順序 | 順序依存 | 順序非依存（並列実行可能） |

## テスト実装優先順位

### Phase 1（最高優先度）
1. `saju-calculation-test.md` - 命式計算・保存API
2. `saju-detail-test.md` - 命式詳細API

### Phase 2（高優先度）
3. `auth-endpoints-test.md` - 認証API
4. `saju-fortune-test.md` - 年月日運API

### Phase 3（中優先度）
5. `saju-list-test.md` - 命式リスト・削除API
6. `settings-test.md` - 設定・データ管理API
7. `data-migration-test.md` - データ移行API

## テスト実行方法

### すべての単品テストを実行

```bash
cd frontend
npx playwright test tests/e2e/unit/
```

### 特定のAPI種別のみ実行

```bash
# 認証APIのみ
npx playwright test tests/e2e/unit/auth-endpoints.spec.ts

# 命式計算APIのみ
npx playwright test tests/e2e/unit/saju-calculation.spec.ts
```

### 並列実行

```bash
# 4つのワーカーで並列実行
npx playwright test tests/e2e/unit/ --workers=4
```

## テストデータ管理

### 固定テストデータ

各単品テストで使用する固定テストデータは `tests/fixtures/` に配置します。

```
tests/
├── fixtures/
│   ├── auth-test-data.ts
│   ├── saju-test-data.ts
│   └── fortune-test-data.ts
└── e2e/
    └── unit/
        ├── auth-endpoints.spec.ts
        ├── saju-calculation.spec.ts
        └── ...
```

### テストデータ例

```typescript
// tests/fixtures/saju-test-data.ts
export const testBirthData = {
  male1990: {
    birthDatetime: '1990-03-15T14:30:00+09:00',
    gender: 'male',
    name: 'テスト太郎',
    expected: {
      yearStem: '庚',
      yearBranch: '午',
      monthStem: '己',
      monthBranch: '卯',
    }
  },
  female1995: {
    birthDatetime: '1995-06-20T10:15:00+09:00',
    gender: 'female',
    name: 'テスト花子',
    expected: {
      yearStem: '乙',
      yearBranch: '亥',
      monthStem: '壬',
      monthBranch: '午',
    }
  }
};
```

## 品質ゲート

### 単品テスト全体の成功基準

- ✅ 全19エンドポイントのテストが成功
- ✅ 正常系テストケースが100%成功
- ✅ 異常系テストケースが95%以上成功
- ✅ パフォーマンス要件を満たす

---

**作成日**: 2025年11月2日
**バージョン**: 1.0
**対応API仕様書**: `docs/api-specs/*.md`
