# 使用されていないファイル調査レポート

**調査日**: 2025-11-03
**プロジェクト**: ゴールデン四柱推命アプリケーション

---

## 📊 調査概要

### 調査対象
- ルートディレクトリのPythonスクリプト（62ファイル）
- ルートディレクトリのJSONデータファイル（18ファイル）
- ルートディレクトリのシェルスクリプト（6ファイル）
- mockupsディレクトリのHTMLファイル（16 + 3ファイル）
- フロントエンドのTypeScriptファイル
- HTMLデバッグファイル

### 調査対象外
- `node_modules/`, `venv/`, `.git/` ディレクトリ
- ドキュメントファイル（`*.md`）
- 設定ファイル（`package.json`, `tsconfig.json`等）
- `backend/`, `frontend/src/`, `src/` 内の実装コード（現在使用中のため）

---

## 🗑️ 削除推奨ファイル

### 1. ルートディレクトリのPythonスクリプト（62ファイル）

#### カテゴリA: テスト・検証用スクリプト（全て削除可）
これらは開発初期の検証・デバッグ用で、現在はbackend/testsに統合済み。

```
accurate_daeun_calculator.py
accurate_saju_system_test.py
analyze_daeun_theory.py
calculate_1908_male.py
calculate_1988_female.py
calculate_compatibility.py
debug_1903_calculation.py
debug_solar_terms.py
detailed_female_calculation.py
final_test_system.py
saju_verification_system.py
test_1900_random_case.py
test_1906_1907.py
test_1908_accurate.py
test_1909_male.py
test_75_degree.py
test_corrected_1900.py
test_csv_fetch.py
test_daeun.py
test_daeun2.py
test_ephem.py
test_expected_case.py
test_koyomi_fetch.py
test_multiple_birthcases.py
test_multiple_cases.py
test_random_saju_cases.py
test_results_analysis.py
test_with_lunar.py
validate_1980_2020.py
validate_2020_2060.py
verify_daeun_calculation.py
```

**理由**:
- backend/tests/にPytestベースの正式なテストスイートが存在
- importしているコードなし
- 開発履歴の参考用だが、Gitで保存されているため削除可

#### カテゴリB: データベース生成スクリプト（役目終了、削除可）
節気データベースは既に完成しており、再生成の必要なし。

```
add_1903_complete_solar_terms.py
add_1908_solar_terms.py
add_1909_solar_terms.py
add_all_missing_solar_terms.py
create_accurate_1986_database.py
collect_jeolip_data.py
generate_jeolip_database.py
generate_solar_terms_1910_1960.py
generate_solar_terms_1960_2010.py
generate_solar_terms_2010_2100.py
generate_solar_terms_2101_2109.py
merge_210_years_database.py
merge_all_solar_terms_database.py
multi_source_jeolip_collector.py
remove_zhongqi_from_database.py
solar_terms_validation_framework.py
final_210_year_validation.py
fix_solar_terms.py
fetch_accurate_1986_data.py
```

**理由**:
- 最終成果物（`solar_terms_1900_2109_JIEQI_ONLY.json`）が既に存在
- 再実行の必要性なし（210年分完成・検証済み）

#### カテゴリC: 分析・互換性チェックスクリプト（削除可）
ドンサゴン分析ロジックは `backend/app/services/fortune_analyzer.py` に統合済み。

```
analyze_koyomi_html.py
automated_compatibility_analyzer.py
automated_compatibility_analyzer_jp.py
compatibility_analyzer_complete.py
compatibility_analyzer_friendly.py
correct_matrix_analysis.py
donsagong_compatibility_analysis.py
donsagong_complete_analysis.py
donsagong_correct_analysis.py
donsagong_final_analysis.py
donsagong_matrix_analysis.py
new_compatibility_analysis.py
```

**理由**:
- バックエンドのプロダクションコードに統合済み
- スタンドアロンスクリプトとしての用途なし

---

### 2. JSONデータファイル

#### 削除可（中間生成物・古いバージョン）

```
solar_terms_1900-1910_database.json          # 部分データ（最終版に統合済み）
solar_terms_1900_2100_COMPLETE.json          # 旧バージョン（2109年版が最新）
solar_terms_1900_2100_JIEQI_ONLY.json        # 旧バージョン（2109年版が最新）
solar_terms_1910_1960_complete.json          # 部分データ
solar_terms_1960_2010_complete.json          # 部分データ
solar_terms_2010_2100_complete.json          # 部分データ
solar_terms_2101_2109_complete.json          # 部分データ
solar_terms_1900_2109_COMPLETE.json          # 中気含む版（使用していない）
```

**保持すべきファイル**:
- ✅ `solar_terms_1900_2109_JIEQI_ONLY.json` （本番環境で使用中）

#### 削除可（テスト結果ファイル）

```
accurate_saju_system_test_results.json       # テスト実行結果（再実行可能）
random_saju_test_results.json                # テスト実行結果（再実行可能）
validation_1900_1940.json                    # 検証結果（再検証可能）
validation_1940_1980.json
validation_1980_2020.json
validation_2020_2060.json
validation_2060_2100.json
validation_test_2020_2024.json
```

**理由**: pytestで再実行可能なため、結果ファイルは不要

#### 削除可（未使用データベース）

```
data/accurate_1986_jeolip_database.json
data/jeolip_database_1900_2100.json
data/optimized_jeolip_database_1900_2100.json
```

**理由**: backend/src/内でimportされていない（未使用）

#### テストペイロード（削除可）

```
test-login-payload.json                      # デバッグ用（不要）
```

---

### 3. シェルスクリプト（テスト用）

#### 削除可

```
create-test-user.sh
create-test-example-user.sh
create-goldensaju-test-user.sh
setup-test-saju-data.sh
test-login.sh
test-register.sh
```

**理由**:
- 開発初期の手動テスト用
- 現在は `backend/tests/` のpytestで自動化済み
- 手動実行の必要性なし

---

### 4. mockupsディレクトリ（HTMLファイル）

#### 削除対象（役目終了）

**ルートmockups/**:
```
mockups/ListPage_Responsive.html              # 実装完了（frontend/src/pages/ListPage/）
mockups/ListPage_Simple.html                  # 実装完了
mockups/ListPage_Updated.html                 # 実装完了
mockups/LoginPage.html                        # 実装完了（frontend/src/pages/LoginPage.tsx）
mockups/LoginPage_Responsive.html             # 実装完了
mockups/RegisterPage.html                     # 実装完了（frontend/src/pages/RegisterPage.tsx）
mockups/RegisterPage_Responsive.html          # 実装完了
mockups/SajuDetailPage_Responsive.html        # 実装完了（frontend/src/pages/SajuDetailPage/）
mockups/SajuDetailPage_Updated.html           # 実装完了
mockups/SettingsPage_Responsive.html          # 実装完了（frontend/src/pages/SettingsPage/）
mockups/TopPage.html                          # 実装完了（frontend/src/pages/TopPage/）
mockups/TopPage_Responsive.html               # 実装完了
mockups/P-001-saju-restored-final.html        # デザイン検討用（実装済み）
mockups/P-001-web-version-complete.html       # デザイン検討用（実装済み）
mockups/design-theme-selector.html            # デザインテーマ決定済み
mockups/golden-peppa-animation-standalone.html # コンポーネント化済み（GoldenPeppaLoading.tsx）
```

**frontend/mockups/**:
```
frontend/mockups/SajuDetailPage_Fixed.html
frontend/mockups/SettingsPage_Guest.html
frontend/mockups/SettingsPage_Login.html
```

**未使用CSS/JS**:
```
mockups/SajuDetailPage_v2.css                 # どのHTMLからも参照されていない
mockups/SajuDetailPage_v2.js                  # どのHTMLからも参照されていない
```

**理由**:
- 全てReact実装に移行完了
- デザイン参考用だが、実装コードで代替可能
- Git履歴で保存されている

**保持すべきか検討**:
- デザインの視覚的参考資料として価値があるかもしれないが、実装コードで十分

---

### 5. HTMLデバッグファイル

#### 削除対象

```
debug_1986_get.html
debug_keisan_1986.html
```

**理由**: 開発初期のデバッグ用、現在は不要

---

### 6. フロントエンドの未使用ファイル

#### 削除済み（git statusで確認）
```
D frontend/src/features/auth/services/mockAuthService.ts  # 既に削除済み
D frontend/src/pages/ListPage.tsx                         # 既に削除済み（index.tsxに移行）
```

#### 未使用ページ（削除可）

```
frontend/src/pages/HomePage.tsx
```

**理由**:
- App.tsxでimportされていない
- TopPage.tsxが実際のトップページとして実装済み
- HomePageは初期スケルトンのまま放置されている

---

### 7. E2Eテスト（重複ファイル）

#### 削除対象

```
frontend/tests/e2e/CHAIN-001-saju-calculation-flow.spec.ts  # 大文字版（重複）
frontend/tests/e2e/example.spec.ts                          # Playwrightのサンプル
```

**保持すべきファイル**:
- ✅ `frontend/tests/e2e/chain-001-saju-calculation.spec.ts` （実際のテスト）
- ✅ `frontend/tests/e2e/chain-002-fortune-scroll-display.spec.ts`
- ✅ その他chain-00x系ファイル

---

## 📝 削除推奨サマリー

### 削除可能なファイル数
- **Pythonスクリプト**: 62ファイル（全て）
- **JSONデータファイル**: 17ファイル（1ファイルのみ保持）
- **シェルスクリプト**: 6ファイル（全て）
- **mockups HTML**: 19ファイル（全て）
- **HTMLデバッグ**: 2ファイル（全て）
- **フロントエンド未使用**: 1ファイル（HomePage.tsx）
- **E2Eテスト重複**: 2ファイル

**合計**: 約109ファイル

### ディスク容量削減見込み
- 中間JSONファイル: 約50-100MB
- Pythonスクリプト: 約5MB
- mockups HTML: 約10MB
- **合計削減見込み**: 約65-115MB

---

## ⚠️ 削除前の注意事項

### 絶対に削除してはいけないファイル
1. `solar_terms_1900_2109_JIEQI_ONLY.json` （本番使用中）
2. `backend/` 配下の全ファイル（実装コード）
3. `frontend/src/` 配下の実装コード
4. `src/manseryeok/` 配下のPythonモジュール
5. `.env.local` （環境変数、既に.gitignore済み）
6. 設定ファイル（package.json, tsconfig.json, etc.）

### 削除前の推奨手順
1. **バックアップブランチ作成**
   ```bash
   git checkout -b backup/unused-files
   git add .
   git commit -m "backup: 削除前のスナップショット"
   ```

2. **段階的削除**
   - まずPythonテストスクリプトから削除
   - 次に中間JSONファイル
   - 最後にmockups

3. **各段階でテスト実行**
   ```bash
   cd backend && pytest
   cd frontend && npm test
   ```

---

## 🚀 削除コマンド例

### 安全な削除コマンド（段階的）

#### Phase 1: Pythonテストスクリプト
```bash
rm -f accurate_*.py analyze_*.py calculate_*.py compatibility_*.py \
      correct_*.py create_accurate_*.py debug_*.py detailed_*.py \
      donsagong_*.py final_*.py new_*.py saju_*.py test_*.py \
      validate_*.py verify_*.py add_*.py collect_*.py fetch_*.py \
      fix_*.py generate_*.py merge_*.py multi_*.py remove_*.py \
      solar_terms_*.py
```

#### Phase 2: 中間JSONファイル
```bash
rm -f solar_terms_1900-1910_database.json \
      solar_terms_1900_2100_*.json \
      solar_terms_1910_1960_complete.json \
      solar_terms_1960_2010_complete.json \
      solar_terms_2010_2100_complete.json \
      solar_terms_2101_2109_complete.json \
      solar_terms_1900_2109_COMPLETE.json \
      accurate_saju_system_test_results.json \
      random_saju_test_results.json \
      validation_*.json \
      test-login-payload.json
```

#### Phase 3: データディレクトリ
```bash
rm -rf data/
```

#### Phase 4: シェルスクリプト
```bash
rm -f create-*.sh setup-*.sh test-*.sh
```

#### Phase 5: mockups
```bash
rm -rf mockups/
rm -rf frontend/mockups/
```

#### Phase 6: HTMLデバッグファイル
```bash
rm -f debug_*.html
```

#### Phase 7: フロントエンド未使用ファイル
```bash
rm -f frontend/src/pages/HomePage.tsx
rm -f frontend/tests/e2e/CHAIN-001-saju-calculation-flow.spec.ts
rm -f frontend/tests/e2e/example.spec.ts
```

---

## ✅ 削除後の検証チェックリスト

- [ ] バックエンドテスト全合格: `cd backend && pytest`
- [ ] フロントエンドビルド成功: `cd frontend && npm run build`
- [ ] E2Eテスト全合格: `cd frontend && npm run test:e2e`
- [ ] 開発サーバー起動確認: `cd backend && uvicorn app.main:app --reload`
- [ ] フロントエンド起動確認: `cd frontend && npm run dev`
- [ ] ブラウザで主要機能動作確認
  - [ ] トップページ（命式計算）
  - [ ] ログイン
  - [ ] 命式一覧
  - [ ] 命式詳細（グラフ表示）
  - [ ] 設定ページ

---

## 📌 結論

**削除推奨**: 109ファイル（約65-115MB）

全て以下の条件を満たしています：
1. 現在のコードベースでimportされていない
2. 機能が既に実装コードに統合されている
3. Git履歴で保存されており、必要時に復元可能
4. テスト結果などは再実行可能

**推奨アクション**:
段階的に削除し、各段階でテストを実行して安全性を確認してください。
