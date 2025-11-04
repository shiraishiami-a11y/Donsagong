# 単品エンドポイントテスト - 簡潔版まとめ

このドキュメントは、残り6つのAPI種別の単品テスト仕様を簡潔にまとめたものです。

---

## 命式計算・保存API (`saju-calculation-test.md`)

**対応API仕様書**: `docs/api-specs/saju-calculation-api.md`

| エンドポイント | テストケース | 期待結果 |
|--------------|----------|---------|
| POST `/api/saju/calculate` | 正常系 - 男性データ | 200 OK, 四柱・大運リスト返却 |
| | 正常系 - 女性データ | 200 OK, 大運が逆行 |
| | 異常系 - 範囲外日付 | 400 Bad Request |
| | 異常系 - 性別未指定 | 400 Bad Request |
| POST `/api/saju/save` | 正常系 - ゲストモード | 201 Created, LocalStorage保存 |
| | 正常系 - ログインモード | 201 Created, PostgreSQL保存 |
| | 異常系 - 不正データ | 400 Bad Request |

**重要検証項目**:
- ✅ 年柱が正確（1990年 = 庚午）
- ✅ 月柱が節入日基準で計算される
- ✅ 大運の順行/逆行が性別・陰陽干で正しく判定される
- ✅ 吉凶レベルが5段階で判定される

**パフォーマンス**: 計算API 2秒以内、保存API 1秒以内

---

## 命式リスト・削除API (`saju-list-test.md`)

**対応API仕様書**: `docs/api-specs/saju-list-api.md`

| エンドポイント | テストケース | 期待結果 |
|--------------|----------|---------|
| GET `/api/saju/list` | 正常系 - ログインユーザー | 200 OK, 命式一覧返却 |
| | 正常系 - 空一覧 | 200 OK, 空配列 |
| | 異常系 - 未ログイン | 401 Unauthorized |
| DELETE `/api/saju/{id}` | 正常系 - 削除成功 | 200 OK, 削除成功メッセージ |
| | 異常系 - 存在しないID | 404 Not Found |
| | 異常系 - 他ユーザーの命式削除 | 403 Forbidden |

**重要検証項目**:
- ✅ ログインユーザーの命式のみ返却される
- ✅ 削除後に一覧が更新される
- ✅ 他ユーザーのデータにアクセスできない

**パフォーマンス**: 一覧取得 500ms以内、削除 500ms以内

---

## 命式詳細API (`saju-detail-test.md`)

**対応API仕様書**: `docs/api-specs/saju-detail-api.md`

| エンドポイント | テストケース | 期待結果 |
|--------------|----------|---------|
| GET `/api/saju/{id}` | 正常系 - 詳細取得 | 200 OK, 四柱・大運・グラフデータ返却 |
| | 異常系 - 存在しないID | 404 Not Found |
| GET `/api/saju/{id}/daeun` | 正常系 - 大運リスト | 200 OK, 10個前後の大運返却 |
| | 正常系 - 現在の大運ハイライト | `isCurrent: true` が含まれる |
| GET `/api/saju/{id}/current` | 正常系 - 現在の運勢 | 200 OK, 年月日運返却 |

**重要検証項目**:
- ✅ 人生グラフデータが100歳まで生成される
- ✅ 現在の大運が `isCurrent: true` でマークされる
- ✅ 天干・地支マトリックスによる吉凶判定が反映される

**パフォーマンス**: 詳細取得 500ms以内、大運取得 500ms以内

---

## 年月日運API (`saju-fortune-test.md`)

**対応API仕様書**: `docs/api-specs/saju-fortune-api.md`

| エンドポイント | テストケース | 期待結果 |
|--------------|----------|---------|
| GET `/api/saju/{id}/year/{daeun_start_age}` | 正常系 - 年運リスト | 200 OK, 10年分返却 |
| | 正常系 - 現在年ハイライト | `isCurrent: true` が含まれる |
| GET `/api/saju/{id}/month/{year}` | 正常系 - 月運リスト | 200 OK, 12ヶ月分返却 |
| | 正常系 - 現在月ハイライト | `isCurrent: true` が含まれる |
| GET `/api/saju/{id}/day/{year}/{month}` | 正常系 - 日運リスト | 200 OK, 28〜31日分返却 |
| | 正常系 - 今日ハイライト | `isToday: true` が含まれる |
| | 異常系 - 無効な月（13月） | 400 Bad Request |

**重要検証項目**:
- ✅ 年運が大運期間の10年分返却される
- ✅ 月運が12ヶ月分返却される
- ✅ 日運がその月の日数分返却される（2月は28/29日、4月は30日等）

**パフォーマンス**: 年運 500ms以内、月運 500ms以内、日運 1秒以内

---

## 設定・データ管理API (`settings-test.md`)

**対応API仕様書**: `docs/api-specs/settings-api.md`

| エンドポイント | テストケース | 期待結果 |
|--------------|----------|---------|
| PUT `/api/user/password` | 正常系 - パスワード変更 | 200 OK, 変更成功 |
| | 異常系 - 現在のパスワード間違い | 401 Unauthorized |
| GET `/api/saju/export` | 正常系 - JSONエクスポート | 200 OK, JSON返却 |
| | 正常系 - 0件の場合 | 200 OK, 空配列 |
| POST `/api/saju/import` | 正常系 - インポート成功 | 201 Created, 件数返却 |
| | 異常系 - 不正JSON | 400 Bad Request |
| PUT `/api/user/settings` | 正常系 - 設定更新 | 200 OK, 更新成功 |

**重要検証項目**:
- ✅ エクスポートデータに全命式が含まれる
- ✅ インポート時に重複チェックが行われる
- ✅ パスワード変更後に新パスワードでログイン可能

**パフォーマンス**: エクスポート 3秒以内、インポート 5秒以内

---

## データ移行API (`data-migration-test.md`)

**対応API仕様書**: `docs/api-specs/data-migration-api.md`

| エンドポイント | テストケース | 期待結果 |
|--------------|----------|---------|
| POST `/api/saju/migrate` | 正常系 - 移行成功 | 201 Created, 件数返却 |
| | 正常系 - 0件移行 | 201 Created, 件数0 |
| | 異常系 - トランザクションロールバック | 500 Internal Server Error |

**重要検証項目**:
- ✅ 全件成功または全件失敗（All or Nothing）
- ✅ 移行後にLocalStorageがクリアされる
- ✅ ゲストIDがサーバー側UUIDに変換される

**パフォーマンス**: 10件 3秒以内、100件 10秒以内

---

## 全体の品質ゲート

### 成功基準

- ✅ 全19エンドポイントのテストが成功
- ✅ 正常系テストケースが100%成功
- ✅ 異常系テストケースが95%以上成功
- ✅ パフォーマンス要件を満たす
- ✅ セキュリティテストが全項目クリア

### テスト実行

```bash
# すべての単品テストを実行
npx playwright test tests/e2e/unit/

# 並列実行（4ワーカー）
npx playwright test tests/e2e/unit/ --workers=4

# HTMLレポート生成
npx playwright test tests/e2e/unit/ --reporter=html
```

---

**作成日**: 2025年11月2日
**バージョン**: 1.0
**テストツール**: Playwright
**対応API仕様書**: `docs/api-specs/*.md`
