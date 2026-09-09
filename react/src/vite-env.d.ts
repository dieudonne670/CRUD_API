/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL?: string;
  readonly VITE_WS_URL?: string;
  readonly VITE_HLS_URL?: string;
  readonly VITE_API_PREFIX?: string;
  readonly VITE_WS_CHAT_PATH?: string;
  readonly VITE_WS_DM_PATH?: string;
  readonly VITE_WS_NOTIFICATIONS_PATH?: string;
  readonly VITE_HLS_PATH?: string;
  readonly VITE_AUTH_TRANSPORT?: "form" | "json";
  readonly VITE_APP_NAME?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
