# UI改善要件定義書

**作成日**: 2025年11月2日
**優先度**: 🔴 最高

---

## 📋 要件一覧

### 1. 人生グラフのバグ修正 🔴

**現状の問題:**
- 階段式グラフが正しく表示されない
- 線が斜めになってしまう

**期待される動作:**
- Rechartsの`type="stepAfter"`を使用
- 各大運の開始年齢にデータポイント
- 水平線 → 垂直線の階段パターン
- dotは非表示（`dot={false}`）

**実装ファイル:**
- `frontend/src/pages/SajuDetailPage/LifeGraphSection.tsx`

**完了条件:**
- [x] 階段式グラフが正しく表示される
- [x] 点（dot）が表示されない
- [x] 線が滑らかに接続される

---

### 2. 詳細ページに閉じるボタン追加 🔴

**要件:**
- 詳細ページの左上に「閉じる」ボタンを追加
- クリックすると命式リストページに戻る

**デザイン仕様:**
```tsx
<IconButton
  onClick={() => navigate('/list')}
  sx={{
    position: 'absolute',
    top: 16,
    left: 16,
    backgroundColor: 'white',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    '&:hover': {
      backgroundColor: '#f5f5f5',
    }
  }}
>
  <CloseIcon />
</IconButton>
```

**実装ファイル:**
- `frontend/src/pages/SajuDetailPage/index.tsx`

**完了条件:**
- [x] 左上に閉じるボタンが表示される
- [x] クリックすると `/list` に遷移する
- [x] ボタンは常に画面の最前面に表示される

---

### 3. 詳細ページ閉じたら命式リストページに遷移 🔴

**要件:**
- 閉じるボタンクリック時の遷移先を `/list` に設定
- 現在のヘッダーの戻るボタンも `/list` に遷移

**実装:**
```tsx
import { useNavigate } from 'react-router-dom';

const navigate = useNavigate();

// 閉じるボタン
<IconButton onClick={() => navigate('/list')}>
  <CloseIcon />
</IconButton>
```

**実装ファイル:**
- `frontend/src/pages/SajuDetailPage/index.tsx`

**完了条件:**
- [x] 閉じるボタンで `/list` に遷移
- [x] ブラウザバックでも正しく動作

---

### 4. 人生グラフを5段階色分け実装 🔴

**現状の問題:**
- 3段階（凶、平/吉、大吉）のみ
- グラフが平坦すぎて分かりにくい

**新しい5段階仕様:**

| 吉凶レベル | fortuneLevel | 色 | 線の種類 | strokeWidth | strokeDasharray |
|-----------|--------------|---|---------|-------------|----------------|
| **大吉（最高運）** | 5 | 🔴 赤 `#F44336` | 太い実線 | 5 | なし |
| **吉** | 4 | 🟡 ゴールド `#D4AF37` | 実線 | 3 | なし |
| **平** | 3 | 🟢 緑 `#4CAF50` | 実線 | 3 | なし |
| **凶（ちょっと悪い）** | 2 | ⚫ 灰色 `#9E9E9E` | 実線 | 3 | なし |
| **大凶（最悪）** | 1 | ⚫ 灰色 `#9E9E9E` | 波線 | 3 | "5 5" |

**実装コード例:**
```tsx
// 大吉（最高運区間）
<Line
  type="stepAfter"
  dataKey="greatFortune"
  stroke="#F44336"
  strokeWidth={5}
  dot={false}
  connectNulls={false}
/>

// 吉
<Line
  type="stepAfter"
  dataKey="goodFortune"
  stroke="#D4AF37"
  strokeWidth={3}
  dot={false}
  connectNulls={false}
/>

// 平
<Line
  type="stepAfter"
  dataKey="normalFortune"
  stroke="#4CAF50"
  strokeWidth={3}
  dot={false}
  connectNulls={false}
/>

// 凶
<Line
  type="stepAfter"
  dataKey="badFortune"
  stroke="#9E9E9E"
  strokeWidth={3}
  dot={false}
  connectNulls={false}
/>

// 大凶（波線）
<Line
  type="stepAfter"
  dataKey="worstFortune"
  stroke="#9E9E9E"
  strokeWidth={3}
  strokeDasharray="5 5"
  dot={false}
  connectNulls={false}
/>
```

**データ生成ロジック:**
```tsx
const chartData = filteredData.map(point => ({
  age: point.age,
  worstFortune: point.fortuneLevel === 1 ? point.fortuneLevel : null,  // 大凶
  badFortune: point.fortuneLevel === 2 ? point.fortuneLevel : null,     // 凶
  normalFortune: point.fortuneLevel === 3 ? point.fortuneLevel : null,  // 平
  goodFortune: point.fortuneLevel === 4 ? point.fortuneLevel : null,    // 吉
  greatFortune: point.fortuneLevel === 5 ? point.fortuneLevel : null,   // 大吉
}));
```

**実装ファイル:**
- `frontend/src/pages/SajuDetailPage/LifeGraphSection.tsx`

**完了条件:**
- [x] 5段階全てが異なる色で表示される
- [x] 大吉は太赤の太い線（strokeWidth=5）
- [x] 大凶は灰色の波線（strokeDasharray="5 5"）
- [x] 平は緑色
- [x] グラフの視覚的な差が明確

---

## 🎯 実装優先順位

1. **要件4: 人生グラフ5段階色分け** （最優先、視覚的インパクト大）
2. **要件1: 人生グラフバグ修正** （要件4と同時実装可能）
3. **要件2: 閉じるボタン追加** （簡単、すぐ実装可能）
4. **要件3: ナビゲーション修正** （要件2と同時実装）

---

## 📁 影響を受けるファイル

```
frontend/src/pages/SajuDetailPage/
├── index.tsx                    # 閉じるボタン追加
└── LifeGraphSection.tsx         # グラフ修正（5段階色分け＋バグ修正）
```

---

## ✅ 完了条件チェックリスト

- [x] 人生グラフが正しい階段式で表示される
- [x] 5段階全ての色が正しく表示される
- [x] 大凶は波線、大吉は太線で表示される
- [x] 詳細ページに閉じるボタンがある
- [x] 閉じるボタンで `/list` に遷移する
- [x] 点（dot）が表示されない
- [x] ブラウザでの動作確認完了（自動テスト実施）

---

**作成者**: BlueLamp AI Assistant
**承認者**: （ユーザー承認待ち）
