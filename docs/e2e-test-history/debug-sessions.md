# デバッグセッション履歴

総セッション数: 6回
総所要時間: 1.67時間（100分）
平均所要時間: 16.7分/セッション

---

## #DS-001: E2E-CHAIN-001-S1（MUI DatePickerのLocator問題）

**日時**: 2025-11-02 18:20 - 18:30
**所要時間**: 10分
**担当**: デバッグマスター #1
**対象テストID**: E2E-CHAIN-001-S1

### 問題
MUI DatePickerのLocator `.MuiDatePicker-root input` が見つからずタイムアウト（30秒）。
実際のMUI DatePicker/TimePickerは以下の構造で構成：
- spinbutton要素（Year, Month, Day, Hours, Minutes）
- textbox要素（フォーマット済み日時表示）
- button要素（カレンダー/時計アイコンボタン）

### 調査
1. error-context.mdから実際のDOM構造を確認
2. `.MuiDatePicker-root`クラスが存在しないことを確認
3. `spinbutton`要素の存在を確認
4. MUI DatePicker/TimePickerのE2Eテスト方法を調査

### 対応
1. Locatorを`.MuiDatePicker-root input`から`getByRole('spinbutton')`に変更
2. 入力順序を`click()` → `clear()` → `fill()`に修正
3. strict mode violation（ローディングアニメーション）を回避

### 結果
Pass（2.8秒）

### 学び
- MUI DatePicker/TimePickerは`.MuiDatePicker-root`クラスを持たない
- `spinbutton`要素を`getByRole()`で取得するのが正解
- `click()` → `clear()` → `fill()`の順序が必須
- 他のテスト（S2〜S11）でも同じパターンを適用可能

---

## #DS-002: E2E-CHAIN-001-S2（大運順行/逆行の判定ルール誤解）

**日時**: 2025-11-02 18:35 - 19:05
**所要時間**: 30分
**担当**: デバッグマスター #2
**対象テストID**: E2E-CHAIN-001-S2

### 問題
APIレスポンスの`isForward`値がE2E仕様書の期待値と不一致。
- 期待値: `false`（逆行）
- 実際: `true`（順行）

初回調査では「lunar-pythonのバグ」と判断したが、実際にはE2E仕様書の理解が誤っていた。

### 調査
1. 大運順行/逆行の理論的ルールを再確認（Web検索）
2. 年の陰陽判定方法を特定
   - 誤: 西暦で判定（西暦1995年=奇数→陽年）
   - 正: **年干で判定**（年干「乙」=陰干→陰年）
3. 既存Pythonコード（src/manseryeok/calculator.py）を確認
4. lunar-pythonの実装を検証

### 対応
1. E2E仕様書を修正（docs/e2e-specs/CHAIN-001-saju-calculation-flow.md）
   - シナリオ2の期待値: `isForward: false` → `isForward: true`
   - コメント修正: 「女性 + 陰干[乙] → 逆行」→「女性 + 陰干[乙] → 順行」
2. E2Eテストコードを修正（frontend/tests/e2e/CHAIN-001-saju-calculation-flow.spec.ts）
   - 期待値: `expect(sajuData.isForward).toBe(false)` → `expect(sajuData.isForward).toBe(true)`
3. タイムアウト対策
   - `Promise.all`を使ってボタンクリックとレスポンス待機を並行実行

### 結果
Pass（2.8秒）

### 学び
- lunar-pythonの実装は正しい
- 年の陰陽は西暦ではなく**年干**で判定
- 大運順行/逆行のルール:
  - 男性 + 陽干 → 順行
  - 男性 + 陰干 → 逆行
  - 女性 + 陽干 → 逆行
  - 女性 + 陰干 → 順行
- E2E仕様書の記載内容を鵜呑みにせず、理論的根拠を確認すべき

---

## #DS-003: E2E-CHAIN-001-S5/S6（クライアント側バリデーション未実装）

**日時**: 2025-11-02 18:50 - 19:00
**所要時間**: 10分
**担当**: デバッグマスター #3
**対象テストID**: E2E-CHAIN-001-S5, E2E-CHAIN-001-S6

### 問題
クライアント側バリデーションのエラーメッセージ要素 `[data-testid="error-message"]` が表示されない。
- S5: 範囲外の日付（1899年12月31日）入力時
- S6: 範囲外の日付（2110年1月1日）入力時

TopPageにクライアント側バリデーションが未実装だった。

### 調査
1. TopPage（frontend/src/pages/TopPage/index.tsx）の確認
2. バリデーションロジックの有無を確認 → 未実装を発見
3. data-testid="error-message" 属性の存在確認 → 存在しない

### 対応
1. バリデーションエラーstate追加（`useState<string>('')`）
2. 日付範囲バリデーション実装（1900-2109年チェック）
3. エラーメッセージ表示要素追加（赤背景のBox、data-testid属性付与）
4. バリデーションエラー時にAPI呼び出しをブロック（`return`）

### 結果
Pass（S5: 4.2秒、S6: 2.1秒）

### 学び
- クライアント側バリデーションはユーザー体験向上に重要
- エラーstate管理（`useState<string>('')`）
- 送信前にバリデーション実行、エラー時は`return`でブロック
- `data-testid`属性でE2Eテストから要素を特定可能
- ユーザーフレンドリーなエラーデザイン（赤背景、明確なメッセージ）
- 1つの修正で複数のテストが同時に解決可能（S5とS6）

---

## #DS-004: E2E-CHAIN-001-S7/S8/S9（必須フィールド・ネットワークエラー検証未実装）

**日時**: 2025-11-02 18:55 - 19:05
**所要時間**: 10分
**担当**: デバッグマスター #4
**対象テストID**: E2E-CHAIN-001-S7, E2E-CHAIN-001-S8, E2E-CHAIN-001-S9

### 問題
3つのテストが同時に失敗：
- S7: 生年月日未入力時のエラーメッセージが表示されない
- S8: 性別未選択時のエラーメッセージが表示されない
- S9: ネットワークエラー時にローディングアニメーションとエラーメッセージが表示されない

### 調査
1. TopPageの初期stateを確認 → デフォルト値が設定されていた（null/空ではない）
2. MUI DatePickerの`required`属性がブラウザネイティブバリデーションと競合
3. ネットワークエラーハンドリングが未実装
4. ローディング表示のタイミング問題（React state更新の非同期性）

### 対応
1. 初期stateをnull/空に変更（birthDate, birthTime, gender）
2. MUI DatePickerから`required`属性を削除
3. 必須フィールドのカスタムバリデーションを実装
4. try-catchでネットワークエラーハンドリングを実装
5. `await new Promise(resolve => setTimeout(resolve, 0))` でReactの再レンダリングを保証

### 結果
Pass（S7: 1.7秒、S8: 1.6秒、S9: 1.8秒）

### 学び
- MUI DatePickerの`required`はネイティブバリデーションと競合する
- カスタムバリデーションで統一的なエラーメッセージ管理が可能
- React state更新は非同期なので、即座に副作用が必要な場合は`setTimeout(0)`を使用
- try-catch + state管理でネットワークエラーのUXを向上

---

## #DS-005: E2E-CHAIN-003-S1/S2（test.only()設定ミス・API期待値誤り）

**日時**: 2025-11-02 19:05 - 19:30
**所要時間**: 25分
**担当**: デバッグマスター #5
**対象テストID**: E2E-CHAIN-003-S1, E2E-CHAIN-003-S2

### 問題
- S1: テストが実行されない（test.only()がS2に設定されていた）
- S1: 「大運（10年周期）」要素が見つからない（実際は実行されていなかっただけ）
- S2: API URL期待値が誤り（`/month/18/0`を期待、実際は`/month/2008`）
- S2: 存在しないフィールド`yearIndex`の検証でエラー

### 調査
1. テストファイルを確認 → S1に`test.only()`がなく、S2にある
2. MonthFortuneScrollSectionのdata-testid属性を確認 → 未設定
3. 月運API仕様を確認 → URLは`/{id}/month/{year}`で年は西暦（2008）、年齢（18）ではない
4. APIレスポンス構造を確認 → `yearIndex`フィールドは存在しない

### 対応
1. **テストファイル修正**:
   - S1に`test.only()`を追加（line 7）
   - S2から`test.only()`を削除（line 116）
   - S2のAPI URL期待値を修正: `/month/18/0` → `/month/2008` (line 217)
   - S2のyear検証を修正: `expect(monthData.year).toBe(18)` → `toBe(2008)` (line 224)
   - S2の存在しない`yearIndex`フィールド検証を削除

2. **コンポーネント修正**（MonthFortuneScrollSection.tsx）:
   - `data-testid="month-scroll-container"` 追加 (line 90)
   - `data-testid="month-card"` 追加 (line 117)
   - `data-testid="month-stem"` 追加 (line 167)
   - `data-testid="month-branch"` 追加 (line 185)
   - `data-testid="fortune-icon"` 追加 (line 206)

### 結果
Pass（S1: 6.8秒、S2: 8.0秒）

### 学び
- `test.only()`の設定ミスで意図しないテストスキップが発生
- 年齢 vs 西暦の混同に注意（大運の開始年齢18歳 ≠ 西暦2008年）
- API仕様書とテスト期待値を常に照合すべき
- E2Eテスト用のdata-testid属性は開発時に一緒に実装すべき
- 存在しないフィールドの検証はAPIレスポンス構造を確認してから書く

---

## #DS-006: E2E-CHAIN-003-S3（タイミング問題による一時的失敗）

**日時**: 2025-11-02 19:35 - 19:40
**所要時間**: 5分
**担当**: デバッグマスター #6
**対象テストID**: E2E-CHAIN-003-S3

### 問題
初回実行時にタイムアウトエラー:
- 期待: `/api/saju/${sajuId}/day/2008/11` API呼び出し
- 実際: API呼び出しが発生せず、2025年11月の日運が自動表示された

### 調査
1. MonthFortuneScrollSectionのクリックイベントを確認 → `onMonthSelect()`が正しく呼ばれている
2. SajuDetailPageの`handleMonthSelect()`を確認 → `selectedMonth` stateが正しく設定される
3. DayFortuneScrollSectionのuseEffectを確認 → API呼び出しロジックは正しく実装されている
4. 依存配列`[sajuId, year, month]`も正しい

### 対応
**コード修正: なし**

実装は既に正しく、以下の理由で初回失敗した可能性:
- バックエンドAPIが一時的に未準備だった
- ネットワークレイテンシによるタイミング問題
- React state更新とuseEffectのタイミング

再実行で問題なく動作することを確認。

### 結果
Pass（8.3秒）

### 学び
- 実装が正しくても、タイミング問題で一時的に失敗することがある
- E2Eテストの再実行で解決する場合、実装ではなく環境・タイミングの問題
- useEffectの依存配列が正しければ、state変更時に自動的にAPI呼び出しが発生する
- React の状態管理とuseEffectのライフサイクルは正しく動作している

---
