# フロントエンドディレクトリ構造調査レポート

**調査日**: 2025年11月3日
**対象**: `/frontend` ディレクトリ
**技術スタック**: React 19 + TypeScript 5 + Vite 7

---

## 1. 全体構造（tree形式）

```
frontend/
├── mockups/                    # モックアップHTMLファイル（3件）
├── playwright-report/          # E2Eテストレポート
├── public/
│   ├── images/                 # 画像アセット（7件：peppa.png、光線、キラキラ）
│   └── vite.svg
├── src/
│   ├── assets/
│   │   └── react.svg
│   ├── components/             # 共通コンポーネント（3件）
│   │   ├── GoldenPeppaLoading.tsx
│   │   ├── Header.tsx
│   │   └── Sidebar.tsx
│   ├── features/               # Feature-based構成
│   │   └── auth/
│   │       ├── components/
│   │       │   └── ProtectedRoute.tsx
│   │       ├── contexts/
│   │       │   └── AuthContext.tsx
│   │       ├── hooks/
│   │       │   └── useAuth.ts
│   │       ├── services/
│   │       │   └── authService.ts
│   │       └── utils/          # （空）
│   ├── hooks/                  # （空）
│   ├── layouts/                # レイアウトコンポーネント（2件）
│   │   ├── MainLayout.tsx
│   │   └── PublicLayout.tsx
│   ├── pages/                  # ページコンポーネント
│   │   ├── HomePage.tsx        # ❌ 使用されていない（未削除）
│   │   ├── LoginPage.tsx       # ✅ 単一ファイル
│   │   ├── RegisterPage.tsx    # ✅ 単一ファイル
│   │   ├── SettingsPage.tsx    # ⚠️ 重複（ファイルとディレクトリの両方が存在）
│   │   ├── ListPage/           # ✅ ディレクトリ構成
│   │   │   ├── components/
│   │   │   │   ├── SajuCard.tsx
│   │   │   │   └── SearchFilterBar.tsx
│   │   │   └── index.tsx
│   │   ├── SajuDetailPage/     # ✅ ディレクトリ構成
│   │   │   ├── components/
│   │   │   │   ├── DaeunScrollSection.tsx
│   │   │   │   ├── DayFortuneScrollSection.tsx
│   │   │   │   ├── MonthFortuneScrollSection.tsx
│   │   │   │   └── YearFortuneScrollSection.tsx
│   │   │   ├── BasicInfoSection.tsx
│   │   │   ├── LifeGraphSection.tsx
│   │   │   ├── PillarsSection.tsx
│   │   │   ├── TodayFortuneSection.tsx
│   │   │   └── index.tsx
│   │   ├── SettingsPage/       # ⚠️ 重複（親ディレクトリにもファイルが存在）
│   │   │   ├── components/
│   │   │   │   ├── AccountSection.tsx
│   │   │   │   ├── AppInfoSection.tsx
│   │   │   │   ├── AutoLoginSection.tsx
│   │   │   │   ├── DataManagementSection.tsx
│   │   │   │   └── DisplaySettingsSection.tsx
│   │   │   └── index.tsx
│   │   └── TopPage/            # ✅ ディレクトリ構成
│   │       └── index.tsx
│   ├── services/               # APIサービス層
│   │   └── api/
│   │       ├── client.ts
│   │       ├── sajuCalculationService.ts
│   │       ├── sajuFortuneService.ts
│   │       ├── sajuListService.ts
│   │       └── settingsService.ts
│   ├── theme/                  # MUI v7カスタムテーマ
│   │   ├── components.ts
│   │   ├── index.ts
│   │   ├── palette.ts
│   │   └── typography.ts
│   ├── types/                  # ✅ 単一真実源（絶対分割禁止）
│   │   └── index.ts            # 343行、全型定義を集約
│   ├── utils/                  # ユーティリティ関数
│   │   └── sajuHelpers.ts
│   ├── App.css
│   ├── App.tsx
│   ├── index.css
│   ├── main.tsx
│   └── vite-env.d.ts
├── test-results/               # Playwrightテスト結果
├── tests/                      # E2Eテスト
│   └── e2e/
│       ├── CHAIN-001-saju-calculation-flow.spec.ts
│       ├── chain-001-saju-calculation.spec.ts
│       ├── chain-002-fortune-scroll-display.spec.ts
│       ├── chain-003-interactive-fortune.spec.ts
│       ├── chain-004-guest-to-login.spec.ts
│       ├── chain-005-data-management.spec.ts
│       ├── example.spec.ts
│       └── ui-improvements.spec.ts
├── .vercel/                    # Vercel設定
├── eslint.config.js
├── index.html
├── package.json
├── playwright.config.ts
├── tsconfig.json
├── tsconfig.app.json
├── tsconfig.node.json
└── vite.config.ts
```

---

## 2. ファイル数・種類の統計

### 全体統計
- **総ディレクトリ数**: 25
- **TypeScript/TSXファイル数**: 46
  - `.tsx`ファイル: 32
  - `.ts`ファイル: 14
- **その他ファイル**: `.css`（2）、`.svg`（1）
- **総コード行数**（src内）: 8,104行

### ディレクトリ別サイズ
- `src/`: 340KB
- `src/pages/`: 192KB（全体の56%）
- `src/components/`: 24KB
- `src/features/`: 20KB

### ページ別ファイル構成
| ページ | 構成 | ファイル数 | 状態 |
|--------|------|-----------|------|
| TopPage | ディレクトリ | 1（index.tsx） | ✅ 正常 |
| ListPage | ディレクトリ | 3（index + 2 components） | ✅ 正常 |
| SajuDetailPage | ディレクトリ | 9（index + 4 sections + 4 components） | ✅ 正常 |
| SettingsPage | **重複** | 6（親ファイル + index + 5 components） | ⚠️ 不整合 |
| LoginPage | 単一ファイル | 1 | ✅ 正常 |
| RegisterPage | 単一ファイル | 1 | ✅ 正常 |
| HomePage | 単一ファイル | 1 | ❌ 未使用 |

---

## 3. 命名パターンの分析

### ファイル命名規則
- **PascalCaseファイル**: 27件（コンポーネント、ページ）
  - 例: `GoldenPeppaLoading.tsx`, `TopPage/index.tsx`, `SajuCard.tsx`
- **camelCaseファイル**: 19件（サービス、ユーティリティ、設定）
  - 例: `authService.ts`, `sajuHelpers.ts`, `client.ts`
- **index.tsx**: 4件（ページエントリポイント）
  - `TopPage/index.tsx`
  - `ListPage/index.tsx`
  - `SajuDetailPage/index.tsx`
  - `SettingsPage/index.tsx`

### CLAUDE.md規約との整合性

#### ✅ 準拠している点
1. **コンポーネント**: PascalCase.tsx（100%準拠）
2. **ユーティリティ**: camelCase.ts（100%準拠）
3. **型定義**: 単一ファイル`types/index.ts`に集約（343行）
4. **テーマ設定**: 適切なディレクトリ分割（`theme/`配下）
5. **Feature-based構成**: `features/auth/`が適切に実装

#### ⚠️ 改善が必要な点
1. **ページ命名の不統一**:
   - `LoginPage.tsx`（単一ファイル）
   - `TopPage/index.tsx`（ディレクトリ）
   - `SettingsPage.tsx` + `SettingsPage/index.tsx`（重複）

---

## 4. 不整合な構造

### 🔴 重大な問題

#### 4.1 SettingsPageの重複
```
src/pages/
├── SettingsPage.tsx          # 4,380バイト、最終更新: 11月3日 11:56
└── SettingsPage/
    ├── index.tsx             # 3,351バイト、最終更新: 11月1日 17:21
    └── components/           # 5件のセクションコンポーネント
```

**現状の問題**:
- App.tsxは`import SettingsPage from './pages/SettingsPage'`で**単一ファイル版**を参照
- `SettingsPage/index.tsx`と`SettingsPage/components/`が未使用状態
- 2つのファイルが並存し、どちらが正式版か不明確

**推奨対応**:
1. `SettingsPage.tsx`（単一ファイル）を削除
2. `SettingsPage/index.tsx`を正式版として使用
3. App.tsxのimportを`'./pages/SettingsPage/'`に変更
4. 理由: componentsディレクトリが既に存在し、機能分割が進んでいる

#### 4.2 HomePage.tsx（未使用ファイル）
- `src/pages/HomePage.tsx`が存在するが、App.tsxで参照されていない
- TopPageがトップページとして実装済み
- 削除対象

### 🟡 軽微な不整合

#### 4.3 ページ構成の不統一
| ページ | 複雑度 | 構成 |
|--------|--------|------|
| LoginPage | 高（12KB, 321行） | 単一ファイル |
| RegisterPage | 高（14KB, 370行） | 単一ファイル |
| TopPage | 高（19KB, 501行） | ディレクトリ（1ファイル） |

**問題点**:
- 大型ページ（10KB以上）が単一ファイルとディレクトリで混在
- TopPageは`index.tsx`のみでcomponentsディレクトリが未作成

**推奨**: 10KB以上のページはディレクトリ構成に統一

#### 4.4 空ディレクトリ
- `src/hooks/`: 空（AuthContextで`useAuth`をカスタムフックとして実装中）
- `src/features/auth/utils/`: 空

**推奨**: 使用予定がなければ削除

---

## 5. React 19 + TypeScript 5 + Vite 7のベストプラクティス照合

### ✅ 良好な実装

#### 5.1 TypeScript設定
- **strictモード有効** (`tsconfig.app.json`)
- **verbatimModuleSyntax**: `true`（MUI v7対応）
- **型推論の厳格化**: `noUnusedLocals`, `noUnusedParameters`有効

#### 5.2 Vite設定
- ポート3247を明示的に設定（CLAUDE.md準拠）
- React Fast Refresh有効

#### 5.3 依存関係バージョン
```json
"react": "^19.1.1"           // ✅ React 19最新
"typescript": "~5.9.3"        // ✅ TypeScript 5.9
"vite": "^7.1.7"              // ✅ Vite 7最新
"@mui/material": "^7.3.4"     // ✅ MUI v7最新
"recharts": "^3.3.0"          // ✅ Recharts v3.3（最新）
```

#### 5.4 アーキテクチャパターン
1. **Feature-based構成**: `features/auth/`でカプセル化実装
2. **Atomic Design風構成**:
   - `components/`: 共通コンポーネント
   - `pages/[PageName]/components/`: ページ固有コンポーネント
3. **APIサービス層の分離**: `services/api/`で集約

#### 5.5 型定義の単一真実源
- `src/types/index.ts`（343行）に全型を集約
- バックエンドとの同期を前提とした設計
- コメントで明確なセクション分割:
  ```typescript
  // ==================== ユーザー・認証関連 ====================
  // ==================== 命式データ関連 ====================
  // ==================== P-003: 命式詳細ページ用型 ====================
  ```

### ⚠️ 改善推奨事項

#### 5.6 React 19の新機能未活用
- **React Compiler**: 未導入（検討推奨）
- **useFormStatus**, **useFormState**: フォームで未使用（LoginPage, RegisterPageで検討）
- **use() Hook**: データフェッチで未使用

#### 5.7 Vite 7の最適化未活用
- **環境変数の型定義**: `vite-env.d.ts`が最小限（407バイト）
- **動的import**: ページ単位のCode Splittingが未実装
  ```typescript
  // 推奨: React.lazy + Suspenseでページ分割
  const TopPage = lazy(() => import('./pages/TopPage'));
  ```

#### 5.8 MUI v7対応の不完全性
- **verbatimModuleSyntax対応**: tsconfig.app.jsonで有効だが、
  ```typescript
  // 推奨: 型インポートは明示的に
  import type { Theme } from '@mui/material/styles';
  ```
- **TypographyOptions**: MUI v7で非推奨（`theme/typography.ts`で確認要）

#### 5.9 Playwrightテストの網羅性
- E2Eテストが8件存在（CHAIN-001〜005 + ui-improvements）
- テストカバレッジの可視化が未実装
- `playwright-report/`が手動管理（CI/CD未統合）

---

## 6. 具体的な改善アクションプラン

### 🔥 緊急対応（即時実施）

#### 6.1 SettingsPage重複解消
```bash
# 1. 単一ファイル版を削除
rm src/pages/SettingsPage.tsx

# 2. App.tsxのimportを修正
# Before: import SettingsPage from './pages/SettingsPage';
# After:  import SettingsPage from './pages/SettingsPage/';
```

#### 6.2 未使用ファイルの削除
```bash
rm src/pages/HomePage.tsx
rm -rf src/hooks/                   # 空ディレクトリ
rm -rf src/features/auth/utils/     # 空ディレクトリ
```

### 🟡 中期対応（1週間以内）

#### 6.3 大型ページのディレクトリ化
```bash
# LoginPage（12KB）とRegisterPage（14KB）を分割
mkdir src/pages/LoginPage src/pages/RegisterPage
mv src/pages/LoginPage.tsx src/pages/LoginPage/index.tsx
mv src/pages/RegisterPage.tsx src/pages/RegisterPage/index.tsx

# 各ページ内のセクションをcomponentsに分割
# 例: LoginPage
mkdir src/pages/LoginPage/components
# LoginForm, SocialLoginButtons等に分割
```

#### 6.4 Code Splitting導入
```typescript
// App.tsx
import { lazy, Suspense } from 'react';
import GoldenPeppaLoading from './components/GoldenPeppaLoading';

const TopPage = lazy(() => import('./pages/TopPage'));
const ListPage = lazy(() => import('./pages/ListPage'));
// ...

function App() {
  return (
    <Suspense fallback={<GoldenPeppaLoading />}>
      {/* Routes */}
    </Suspense>
  );
}
```

### 🟢 長期対応（次フェーズ）

#### 6.5 React 19最適化
- `useFormStatus`/`useFormState`でフォーム実装を最適化
- Server Components検討（Next.js移行時）

#### 6.6 型安全性強化
- バックエンドのOpenAPI定義から自動生成
- Zodスキーマとの統合

#### 6.7 テスト戦略
- Vitest導入（ユニットテスト）
- Playwrightの自動化（CI/CD統合）
- カバレッジ80%目標

---

## 7. 総合評価

### 🌟 強み
1. **型定義の単一真実源**: `types/index.ts`の一元管理
2. **Feature-based構成**: 認証機能のカプセル化
3. **最新技術スタック**: React 19, TypeScript 5, Vite 7, MUI v7
4. **E2Eテスト**: Playwrightで8件のシナリオを実装済み
5. **CLAUDE.md準拠**: 命名規則が90%以上準拠

### ⚠️ 改善点
1. **SettingsPageの重複**: 最優先で解消すべき構造的問題
2. **未使用ファイル**: HomePage.tsx等の整理
3. **ページ構成の不統一**: 大型ページのディレクトリ化
4. **React 19機能未活用**: 新Hooksの導入検討
5. **Code Splitting未実装**: パフォーマンス最適化の余地

### 📊 採点
| 項目 | スコア | 理由 |
|------|--------|------|
| 構造設計 | 7/10 | Feature-based良好、ページ構成に不統一 |
| 型安全性 | 9/10 | 単一真実源の厳守、strictモード有効 |
| 命名規則 | 8/10 | CLAUDE.md準拠率90% |
| 保守性 | 6/10 | 重複ファイル、未使用コード存在 |
| パフォーマンス | 6/10 | Code Splitting未実装 |
| テスト | 7/10 | E2E充実、ユニットテスト未整備 |
| **総合** | **7.2/10** | 堅実な基礎、即時改善で8.5+可能 |

---

## 8. まとめ

### 現状
フロントエンドは**React 19 + TypeScript 5 + Vite 7 + MUI v7の最新技術スタックで構築された堅実な基盤**を持つ。Feature-based構成と型定義の一元管理により、プロジェクトの基本方針である「単一性の原則」を概ね実現している。

### 即時対応が必要な問題
1. **SettingsPageの重複解消**（構造的不整合）
2. **未使用ファイルの削除**（刹那性の原則違反）

### 次ステップ
上記2点を解消後、大型ページのディレクトリ化とCode Splittingを実施すれば、**8.5/10以上の高品質な構造**を達成可能。

### 備考
- types/index.tsは**絶対に分割しない**（単一真実源の原則厳守）
- すべての改善は「最小性の原則」に基づき、必要最小限の変更に留めること
- 刹那性の原則に従い、役目を終えたコードは即座に削除すること

---

**レポート作成日**: 2025年11月3日
**調査者**: Claude Code（ブルーランプエージェント）
**調査範囲**: `/Users/shiraishiami/Desktop/Bluelamp/donsagong-master/frontend`
