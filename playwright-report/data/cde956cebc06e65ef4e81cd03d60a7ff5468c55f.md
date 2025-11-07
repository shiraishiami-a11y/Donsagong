# Page snapshot

```yaml
- generic [ref=e4]:
  - generic [ref=e5]:
    - generic [ref=e6]:
      - paragraph [ref=e7]: ✨
      - paragraph [ref=e8]: ゴールデン四柱推命
    - paragraph [ref=e9]: あなたの運命に魔法をかける
  - generic [ref=e10]:
    - paragraph [ref=e12]: ログイン
    - generic [ref=e13]:
      - generic [ref=e14]:
        - paragraph [ref=e15]: メールアドレス
        - generic [ref=e17]:
          - textbox "example@email.com" [ref=e18]
          - group
      - generic [ref=e19]:
        - paragraph [ref=e20]: パスワード
        - generic [ref=e22]:
          - textbox "パスワードを入力" [ref=e23]
          - button [ref=e25] [cursor=pointer]:
            - img [ref=e26]
          - group
      - generic [ref=e28] [cursor=pointer]:
        - generic [ref=e29]:
          - checkbox "ログイン状態を保持" [checked] [ref=e30]
          - img [ref=e31]
        - paragraph [ref=e33]: ログイン状態を保持
    - link "パスワードを忘れた場合" [ref=e35] [cursor=pointer]:
      - /url: "#"
    - generic [ref=e36]:
      - button "ログイン" [ref=e37] [cursor=pointer]
      - paragraph [ref=e40]: または
      - button "ゲストとして利用" [ref=e42] [cursor=pointer]
  - paragraph [ref=e44]:
    - text: アカウントをお持ちでない場合
    - link "新規登録" [ref=e45] [cursor=pointer]:
      - /url: /register
```