/// <reference types="vite/client" />

interface ImportMetaEnv {
  /**
   * E2Eテスト用: 認証をスキップする（ヘッドレスモード）
   * @default undefined
   */
  readonly VITE_SKIP_AUTH?: string;

  /**
   * バックエンドAPIのベースURL
   * @default 'http://localhost:8432/api'
   */
  readonly VITE_API_URL?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
