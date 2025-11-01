# 四柱推命アプリケーション - UI/UXデザインドキュメント

## 1. プロジェクト概要

### 1.1 アプリケーション名
**四柱推命・相性診断アプリ**

### 1.2 デザインコンセプト
210年節気データベース統合による高精度四柱推命アプリケーションとして、**伝統と先進性の融合**をテーマに、和風の美学と現代的なUIの使いやすさを両立させたデザイン。

### 1.3 設計思想
- **信頼性の視覚化**: 210年データベースの正確性を表現
- **親しみやすさ**: 専門的な内容を初心者にも分かりやすく
- **効率性**: 複雑な計算結果を直感的に理解できる表示
- **継続利用**: ユーザーが長期的に使い続けたくなるUX

## 2. 作成済みモックアップ一覧

### 2.1 完成ページ
- **P-001**: 四柱推命入力・計算ページ (`P-001-saju-calculation.html`)
- **P-002**: 相性診断ページ (`P-002-compatibility-analysis.html`)
- **P-003**: 大運分析ページ (`P-003-daeun-analysis.html`)
- **P-004**: データ管理ページ (`P-004-data-management.html`)

### 2.2 技術スタック
- **フレームワーク**: React 18 + TypeScript
- **UIライブラリ**: Material-UI v5
- **スタイリング**: CSS-in-JS + カスタムCSS
- **レスポンシブ**: Mobile-first アプローチ

## 3. デザインシステム

### 3.1 カラーパレット

#### 主要カラー
```css
/* P-001: 四柱推命計算 - 紺・金系 */
Primary: #1a1a2e → #16213e → #0f3460
Accent: #ffd700, #ffed4a
Secondary: #2d5a87 → #4a90c2

/* P-002: 相性診断 - 茶・金系 */
Primary: #2c1810 → #8b4513 → #daa520
Accent: #ffd700, #ffed4a
Secondary: #8b4513 → #cd853f

/* P-003: 大運分析 - 紫系 */
Primary: #4a148c → #7b1fa2 → #9c27b0
Accent: #ffd700, #ffed4a
Secondary: #7b1fa2 → #9c27b0

/* P-004: データ管理 - 青系 */
Primary: #0d47a1 → #1976d2 → #42a5f5
Accent: #ffd700, #ffed4a
Secondary: #1976d2 → #42a5f5
```

#### 共通カラー
```css
/* 成功・警告・エラー */
Success: #4caf50 → #66bb6a
Warning: #ff9800 → #ffb74d
Error: #f44336 → #ef5350
Info: #2196f3 → #42a5f5

/* ニュートラル */
Background: rgba(255, 255, 255, 0.95)
Text: #1a1a2e, #333, #666
Border: #e0e0e0, #dee2e6
```

### 3.2 タイポグラフィ

#### フォントファミリー
```css
Primary: 'Roboto', 'Noto Sans JP', sans-serif
Secondary: 'Noto Serif JP', serif (四柱推命文字専用)
```

#### フォントサイズ階層
```css
h1 (Main Title): 2.5rem (40px) - モバイル: 2rem (32px)
h2 (Section Title): 1.5rem (24px)
h3 (Subsection): 1.2rem (19px)
Body: 1rem (16px)
Small: 0.9rem (14px)
Caption: 0.8rem (13px)
Micro: 0.7rem (11px)
```

### 3.3 レイアウトシステム

#### グリッドシステム
```css
/* デスクトップ */
Container Max-width: 1200px - 1400px
Columns: 12 column grid
Gutter: 20px - 30px

/* タブレット */
Container: 100% with 20px padding
Columns: Flexible 2-3 columns

/* モバイル */
Container: 100% with 15px padding
Columns: Single column
```

#### 間隔システム
```css
Space-xs: 5px
Space-sm: 10px
Space-md: 15px
Space-lg: 20px
Space-xl: 30px
Space-2xl: 40px
```

### 3.4 コンポーネント設計

#### 基本コンポーネント
```css
/* カード */
.card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 20px-30px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

/* ボタン */
.button-primary {
  background: linear-gradient(45deg, [Primary Color]);
  color: white;
  border-radius: 8px;
  padding: 12px-15px;
  font-weight: 600;
  transition: transform 0.2s ease;
}

.button-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba([Primary], 0.3);
}

/* 入力フィールド */
.input-field {
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 12px;
  transition: border-color 0.3s ease;
}

.input-field:focus {
  border-color: [Primary Color];
  box-shadow: 0 0 0 3px rgba([Primary], 0.1);
}
```

## 4. 各ページ詳細設計

### 4.1 P-001: 四柱推命計算ページ

#### 設計意図
- **信頼性重視**: 210年データベースの正確性を前面に押し出し
- **シンプルな入力**: 必要最小限の入力項目で操作の迷いを排除
- **結果の視覚化**: 四柱を分かりやすくカード形式で表示

#### 主要機能
1. **生年月日時入力フォーム**: 直感的な日時ピッカー
2. **性別選択**: ビジュアルなボタン選択
3. **四柱表示**: 伝統的な漢字表記 + 読み方
4. **大運タイムライン**: 現在運勢のハイライト
5. **ドンサゴン分析**: 独自の価値提案

#### 実装注意点
```typescript
// API統合ポイント
interface BirthDataRequest {
  birth_datetime: Date;
  gender: 'male' | 'female';
  timezone_offset: number;
}

// 状態管理
const [calculationResult, setCalculationResult] = useState<SajuResponse | null>(null);
const [isLoading, setIsLoading] = useState(false);

// バリデーション
const validateBirthData = (data: BirthDataRequest): boolean => {
  // 生年月日の範囲チェック（1900-2109年）
  // 時刻の有効性チェック
  // 性別選択チェック
}
```

### 4.2 P-002: 相性診断ページ

#### 設計意図
- **比較の明確化**: 二人の情報を対比しやすいレイアウト
- **スコアの視覚化**: 数値だけでなく色とグラフで直感的理解
- **マトリックス表示**: 複雑な分析結果を整理して表示

#### 主要機能
1. **二人分入力フォーム**: 区別しやすいデザイン
2. **総合スコア表示**: 大きく分かりやすい数値
3. **天干マトリックス**: インタラクティブな表示
4. **詳細解説**: ドンサゴン分析による説明

#### 実装注意点
```typescript
// 複雑な計算結果の処理
interface CompatibilityResponse {
  overall_score: number;
  stem_analysis: Record<string, StemCompatibility>;
  branch_analysis: Record<string, BranchCompatibility>;
  detailed_explanation: string;
}

// マトリックス表示の最適化
const renderMatrix = useMemo(() => {
  // 100組合せの天干マトリックス
  // 144組合せの地支調候表
  // パフォーマンス考慮した描画
}, [compatibilityData]);
```

### 4.3 P-003: 大運分析ページ

#### 設計意図
- **時系列の明確化**: タイムライン形式で人生の流れを表現
- **現在の強調**: 現在運勢を視覚的にハイライト
- **未来予測**: 重要時期の予測を分かりやすく表示

#### 主要機能
1. **サイドバー概要**: 現在状況と重要時期の要約
2. **大運タイムライン**: 10年周期の流れ表示
3. **詳細分析**: 各大運期の特徴と対策
4. **年運組み合わせ**: 近年の詳細予測

#### 実装注意点
```typescript
// タイムライン表示の最適化
interface DaeunPeriod {
  start_age: number;
  end_age: number;
  daeun_stem: string;
  daeun_branch: string;
  characteristics: string[];
  is_current: boolean;
}

// スクロール連動ナビゲーション
const handleScroll = useCallback(() => {
  // セクション判定とナビゲーション更新
}, []);
```

### 4.4 P-004: データ管理ページ

#### 設計意図
- **効率的な検索**: 複数フィルターによる絞り込み機能
- **履歴管理**: 使いやすい一覧表示と操作
- **データ保護**: バックアップ・復元機能の提供

#### 主要機能
1. **検索・フィルター**: リアルタイム検索と複数条件絞り込み
2. **データ一覧**: カード形式での見やすい表示
3. **お気に入り管理**: 重要データの迅速アクセス
4. **エクスポート機能**: 複数形式での出力対応

#### 実装注意点
```typescript
// ページネーションとフィルタリング
interface DataFilter {
  type?: 'saju' | 'compatibility' | 'daeun';
  date_range?: string;
  favorite_only?: boolean;
  search_query?: string;
}

// 大量データの効率的処理
const useDataList = () => {
  const [data, setData] = useState<CalculationHistory[]>([]);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);

  // 仮想スクロール or ページネーション実装
};
```

## 5. レスポンシブデザイン戦略

### 5.1 ブレークポイント
```css
/* モバイル優先設計 */
Mobile: 320px - 767px
Tablet: 768px - 1023px
Desktop: 1024px - 1440px
Large Desktop: 1441px+
```

### 5.2 各デバイスでの最適化

#### モバイル（320px-767px）
- **シングルカラムレイアウト**
- **大きなタッチターゲット（44px以上）**
- **スワイプ操作対応**
- **フォントサイズ調整**

#### タブレット（768px-1023px）
- **2カラムレイアウト**
- **タッチ操作最適化**
- **横画面対応**

#### デスクトップ（1024px+）
- **マルチカラムレイアウト**
- **ホバー効果活用**
- **キーボードショートカット**

### 5.3 実装例
```css
/* Mobile First */
.main-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}

/* Tablet */
@media (min-width: 768px) {
  .main-content {
    grid-template-columns: 300px 1fr;
    gap: 25px;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .main-content {
    grid-template-columns: 300px 1fr 300px;
    gap: 30px;
  }
}
```

## 6. アクセシビリティ対応

### 6.1 WCAG 2.1 AA準拠

#### 色彩設計
- **コントラスト比**: 4.5:1以上確保
- **色だけに依存しない情報伝達**
- **カラーブラインド対応**

#### キーボード操作
```typescript
// キーボードナビゲーション
const handleKeyDown = (event: KeyboardEvent) => {
  switch (event.key) {
    case 'Tab':
      // フォーカス順序管理
      break;
    case 'Enter':
    case ' ':
      // ボタン・リンク実行
      break;
    case 'Escape':
      // モーダル・ドロップダウン閉じる
      break;
  }
};
```

#### スクリーンリーダー対応
```html
<!-- 適切なARIAラベル -->
<button
  aria-label="四柱推命を計算する"
  aria-describedby="calculation-help"
>
  計算実行
</button>

<!-- セマンティックHTML -->
<main role="main">
  <section aria-labelledby="results-title">
    <h2 id="results-title">計算結果</h2>
  </section>
</main>
```

### 6.2 ユーザビリティ配慮
- **明確なフィードバック**: 処理状況の表示
- **エラーハンドリング**: 分かりやすいエラーメッセージ
- **ヘルプ機能**: 初心者向けガイダンス

## 7. パフォーマンス最適化

### 7.1 読み込み速度最適化

#### Code Splitting
```typescript
// ページレベルの遅延読み込み
const SajuCalculation = lazy(() => import('./pages/SajuCalculation'));
const CompatibilityAnalysis = lazy(() => import('./pages/CompatibilityAnalysis'));
const DaeunAnalysis = lazy(() => import('./pages/DaeunAnalysis'));
const DataManagement = lazy(() => import('./pages/DataManagement'));
```

#### 画像最適化
```css
/* WebP対応とフォールバック */
.background-image {
  background-image: url('image.webp');
  background-image: url('image.jpg'); /* フォールバック */
}

/* レスポンシブ画像 */
img {
  max-width: 100%;
  height: auto;
  loading: lazy;
}
```

### 7.2 レンダリング最適化

#### React最適化
```typescript
// メモ化による再レンダリング防止
const PillarCard = memo(({ pillar }: { pillar: Pillar }) => {
  return (
    <div className="pillar-card">
      {/* ... */}
    </div>
  );
});

// 重い計算のメモ化
const calculatedData = useMemo(() => {
  return expensiveCalculation(inputData);
}, [inputData]);
```

### 7.3 ネットワーク最適化
```typescript
// API呼び出しの最適化
const useApiWithCache = (endpoint: string) => {
  return useQuery({
    queryKey: [endpoint],
    queryFn: () => fetchData(endpoint),
    staleTime: 5 * 60 * 1000, // 5分キャッシュ
    cacheTime: 10 * 60 * 1000, // 10分保持
  });
};
```

## 8. 実装時の技術的注意点

### 8.1 State Management
```typescript
// Zustand による状態管理
interface AppState {
  user: User | null;
  calculations: Calculation[];
  favorites: string[];
  setUser: (user: User) => void;
  addCalculation: (calc: Calculation) => void;
  toggleFavorite: (id: string) => void;
}

const useAppStore = create<AppState>((set) => ({
  user: null,
  calculations: [],
  favorites: [],
  setUser: (user) => set({ user }),
  addCalculation: (calc) => set((state) => ({
    calculations: [...state.calculations, calc]
  })),
  toggleFavorite: (id) => set((state) => ({
    favorites: state.favorites.includes(id)
      ? state.favorites.filter(fav => fav !== id)
      : [...state.favorites, id]
  })),
}));
```

### 8.2 API統合
```typescript
// OpenAPI Generator使用
import { DefaultApi, Configuration } from './generated/api';

const api = new DefaultApi(new Configuration({
  basePath: process.env.REACT_APP_API_BASE_URL,
  accessToken: () => getAuthToken(),
}));

// エラーハンドリング
const useSajuCalculation = () => {
  return useMutation({
    mutationFn: (data: BirthDataRequest) => api.calculateSaju(data),
    onError: (error) => {
      console.error('Calculation failed:', error);
      toast.error('計算に失敗しました。もう一度お試しください。');
    },
    onSuccess: (result) => {
      toast.success('計算が完了しました');
    },
  });
};
```

### 8.3 データバリデーション
```typescript
// Yup による入力バリデーション
const birthDataSchema = yup.object({
  birth_datetime: yup.date()
    .min(new Date('1900-01-01'), '1900年以降の日付を入力してください')
    .max(new Date('2109-12-31'), '2109年以前の日付を入力してください')
    .required('生年月日は必須です'),
  gender: yup.string()
    .oneOf(['male', 'female'], '性別を選択してください')
    .required('性別は必須です'),
});

// React Hook Form との統合
const { control, handleSubmit, formState: { errors } } = useForm({
  resolver: yupResolver(birthDataSchema),
});
```

## 9. セキュリティ考慮事項

### 9.1 データ保護
```typescript
// 個人情報の暗号化
const encryptPersonalData = (data: PersonalData): string => {
  return CryptoJS.AES.encrypt(JSON.stringify(data), secretKey).toString();
};

// セッション管理
const useSecureSession = () => {
  const [token, setToken] = useState<string | null>(
    () => sessionStorage.getItem('auth_token')
  );

  const logout = useCallback(() => {
    sessionStorage.removeItem('auth_token');
    setToken(null);
  }, []);

  return { token, logout };
};
```

### 9.2 XSS防止
```typescript
// HTML エスケープ
import DOMPurify from 'dompurify';

const SafeHTML: React.FC<{ content: string }> = ({ content }) => {
  const sanitizedContent = DOMPurify.sanitize(content);
  return <div dangerouslySetInnerHTML={{ __html: sanitizedContent }} />;
};
```

## 10. 今後の拡張計画

### 10.1 フェーズ2機能
- **年運詳細分析**: より詳細な年単位分析
- **択日システム**: 重要な日取り選定機能
- **モバイルアプリ**: React Native版開発

### 10.2 UI/UX改善計画
- **ダークモード**: 夜間使用への配慮
- **アニメーション強化**: より滑らかな画面遷移
- **音声ガイド**: アクセシビリティ向上

### 10.3 AI統合
```typescript
// AI による解説文生成
const useAIExplanation = (sajuData: SajuData) => {
  return useQuery({
    queryKey: ['ai-explanation', sajuData.id],
    queryFn: () => api.generateAIExplanation(sajuData),
    enabled: !!sajuData.id,
  });
};
```

## 11. 品質保証

### 11.1 テスト戦略
```typescript
// ユニットテスト
describe('SajuCalculation', () => {
  test('正常な入力で計算が実行される', () => {
    const input = {
      birth_datetime: new Date('1990-03-15T10:30:00'),
      gender: 'male' as const,
      timezone_offset: 9,
    };

    const result = calculateSaju(input);
    expect(result).toBeDefined();
    expect(result.year_stem).toBeTruthy();
  });
});

// インテグレーションテスト
test('API呼び出しと結果表示の統合', async () => {
  render(<SajuCalculationPage />);

  fireEvent.change(screen.getByLabelText('生年月日'), {
    target: { value: '1990-03-15' }
  });
  fireEvent.click(screen.getByText('計算実行'));

  await waitFor(() => {
    expect(screen.getByText('計算結果')).toBeInTheDocument();
  });
});
```

### 11.2 パフォーマンステスト
- **Lighthouse スコア**: 90点以上維持
- **Core Web Vitals**: 全項目Green達成
- **ロードテスト**: 同時100ユーザー対応確認

## 12. 運用・保守

### 12.1 監視項目
- **エラー率**: <1%維持
- **応答時間**: 平均2秒以内
- **ユーザー満足度**: NPS調査実施

### 12.2 更新計画
- **定期バックアップ**: 日次自動実行
- **セキュリティ更新**: 月次適用
- **機能更新**: 四半期ごとリリース

---

## まとめ

本デザインドキュメントに基づいて実装することで、四柱推命の専門性を保ちながら、現代的で使いやすいアプリケーションを構築できます。特に210年データベースの正確性とドンサゴン分析法の独自性を活かした、他にない価値のあるサービスの提供が可能になります。

実装時は段階的な開発を行い、各フェーズでユーザーフィードバックを収集して改善を重ねることで、より良いユーザー体験を実現していきます。