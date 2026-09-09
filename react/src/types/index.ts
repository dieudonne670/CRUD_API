/**
 * Domain types mirroring the FastAPI backend.
 *
 * ─────────────────────────────────────────────────────────────────────────────
 * ASSUMPTION BOUNDARY
 * ─────────────────────────────────────────────────────────────────────────────
 * Everything in this file is an *assumption* about the Pydantic schemas served
 * by the backend. Every field that is not guaranteed is optional (`?`) so the
 * UI degrades gracefully instead of crashing when the real payload differs.
 *
 * To adapt the frontend to your actual schemas you should only need to edit:
 *   1. this file            → field names / shapes
 *   2. src/api/endpoints.ts → route paths
 *   3. src/api/*.ts         → request bodies / query params
 * Components never need to change.
 *
 * Conventions assumed here (standard FastAPI + SQLAlchemy + Pydantic v2):
 *   • snake_case field names exactly as produced by Pydantic
 *   • `id` is a number or UUID string, so it is typed loosely as `ID`
 *   • timestamps are ISO-8601 strings (`created_at`)
 */

/** Ids may be integers or UUID strings depending on your models. */
export type ID = string | number;

/* ============================== Auth ==================================== */

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterPayload {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  refresh_token?: string;
  expires_in?: number;
  /** Some backends nest the user inside the auth response. */
  user?: User;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  refresh_token?: string;
  user?: User;
}

/* ============================== Users =================================== */

export interface User {
  id: ID;
  username?: string;
  email?: string;
  full_name?: string;
  first_name?: string;
  last_name?: string;
  avatar_url?: string | null;
  profile_picture?: string | null;
  profile_picture_mime?: string | null;
  profile_picture_size?: number | null;
  /** Some backends expose a nested avatar object instead of a flat url. */
  avatar?: { url?: string } | null;
  cover_url?: string | null;
  bio?: string | null;
  location?: string | null;
  website?: string | null;
  followers_count?: number;
  following_count?: number;
  posts_count?: number;
  is_verified?: boolean;
  is_active?: boolean;
  is_private?: boolean;
  created_at?: string;
  /** Present only on "relationship-aware" endpoints (`is_following`). */
  is_following?: boolean;
  is_followed_by?: boolean;
}

export interface UserUpdatePayload {
  email: string;
  password: string;
}


/* ============================== Media =================================== */

export type MediaKind = "image" | "video" | "audio" | "file";

export interface MediaItem {
  id?: ID;
  url: string;
  type?: MediaKind | string;
  mime_type?: string;
  thumbnail_url?: string | null;
  width?: number;
  height?: number;
  duration?: number;
  size?: number;
  filename?: string;
}


/* ============================== Posts =================================== */

export interface Post {
  id: ID;
  title: string;
  published: boolean;
  owner_id: ID;
  author?: User;
  /** Some backends use `user` or `owner` instead of `author`. */
  user?: User;
  owner?: User;
  content: string;
  text?: string;
  media?: MediaItem[];
  images?: MediaItem[];
  video?: MediaItem | null;
  created_at: string;
  updated_at?: string | null;
  likes_count?: number;
  like_count?: number;
  comments_count?: number;
  comment_count?: number;
  shares_count?: number;
  share_count?: number;
  views_count?: number;
  is_liked?: boolean;
  liked_by_me?: boolean;
  is_bookmarked?: boolean;
  tags?: string[];
}

export interface PostCreatePayload {
  title: string;
  content: string;
  published?: boolean;
  media?: MediaItem[];
}

export interface PostUpdatePayload {
  title: string;
  content: string;
  published?: boolean;
  media?: MediaItem[];
}

export interface PostOut {
  Post: Post;
  vote: number;
}

/* ============================ Comments ================================== */

export interface Comment {
  id: ID;
  post_id?: ID;
  author?: User;
  user?: User;
  content: string;
  created_at: string;
  likes_count?: number;
  is_liked?: boolean;
  parent_id?: ID | null;
  replies_count?: number;
}

export interface CommentCreatePayload {
  content: string;
  post_id?: ID;
  parent_id?: ID | null;
}

/* ============================== Likes =================================== */

export interface Like {
  id: ID;
  user_id?: ID;
  post_id?: ID;
  comment_id?: ID;
  created_at?: string;
}

/* ============================= Follows ================================== */

export interface Follow {
  id: ID;
  follower_id?: ID;
  following_id?: ID;
  follower?: User;
  following?: User;
  created_at?: string;
}

/* ========================== Notifications =============================== */

export type NotificationKind =
  | "like"
  | "comment"
  | "follow"
  | "mention"
  | "message"
  | "livestream"
  | "system"
  | string;

export interface AppNotification {
  id: ID;
  type?: NotificationKind;
  kind?: NotificationKind;
  actor?: User | null;
  user?: User | null;
  message?: string | null;
  body?: string | null;
  title?: string | null;
  post_id?: ID | null;
  comment_id?: ID | null;
  conversation_id?: ID | null;
  livestream_id?: ID | null;
  is_read?: boolean;
  read?: boolean;
  created_at: string;
}

/* ============================ Messaging ================================= */

export interface Conversation {
  id: ID;
  /** Backend may expose `participants`, `members` or two explicit users. */
  participants?: User[];
  members?: User[];
  recipient?: User | null;
  last_message?: Message | null;
  last_message_at?: string | null;
  unread_count?: number;
  is_group?: boolean;
  title?: string | null;
  created_at?: string;
  updated_at?: string | null;
}

export interface Message {
  id: ID;
  conversation_id?: ID;
  sender?: User;
  sender_id?: ID;
  recipient?: User;
  recipient_id?: ID;
  content: string;
  body?: string;
  attachment?: MediaItem | null;
  is_read?: boolean;
  read_at?: string | null;
  created_at: string;
}

export interface MessageCreatePayload {
  receiver_id: ID;
  message: string;
}

/* ============================ Livestream ================================ */

export type StreamStatus = "live" | "offline" | "ended" | string;

export interface Livestream {
  id: ID;
  title: string;
  description?: string | null;
  category?: string | null;
  thumbnail?: string | null;
  thumbnail_url?: string | null;
  status?: StreamStatus;
  tags?: string[];
  owner_id: ID;
  owner?: User | null;
  stream_key: string;
  playback_url?: string | null;
  is_live: boolean;
  current_viewers: number;
  peak_viewers: number;
  recording_url?: string | null;
  started_at?: string | null;
  ended_at?: string | null;
  created_at: string;
}

export interface LivestreamCreatePayload {
  title: string;
  description?: string;
  category?: string;
  thumbnail?: string;
}
export interface LivestreamUpdatePayload {
  title?: string;
  description?: string;
  category?: string;
  thumbnail?: string;
}
export interface LivestreamWatchResponse {
  stream_id: ID;
  playback_url?: string | null;
  is_live: boolean;
  stream: Livestream;
}
export interface LivestreamStats {
  stream_id: ID;
  is_live: boolean;
  current_viewers: number;
  peak_viewers: number;
  started_at?: string | null;
  ended_at?: string | null;
}
export interface ChatMessage {
  id?: ID;
  user?: User;
  username?: string;
  content?: string;
  message?: string;
  created_at?: string;
  timestamp?: string | number;
  type?: string;
}

/* ============================== Search ================================== */

export type SearchScope = "all" | "users" | "posts" | "livestreams";

export interface SearchMeta {
  total?: number;
  took?: number;
  query?: string;
}

export interface SearchResponse<T = unknown> extends SearchMeta {
  /** Elasticsearch wrappers vary: hits.hits[]._source, results, items, data… */
  items?: T[];
  results?: T[];
  hits?: { hits?: { _source?: T }[] } | T[];
  data?: T[];
}

export interface UnifiedSearchResponse {
  users?: SearchResponse<User> | User[];
  posts?: SearchResponse<Post> | Post[];
  livestreams?: SearchResponse<Livestream> | Livestream[];
  streams?: SearchResponse<Livestream> | Livestream[];
}

/* ============================ Pagination ================================ */

export interface PaginationParams {
  page?: number;
  size?: number;
  limit?: number;
  offset?: number;
  sort?: string;
  cursor?: string;
}

/** FastAPI pagination wrappers differ — accept the common shapes. */
export interface Paginated<T> {
  items?: T[];
  results?: T[];
  data?: T[];
  total?: number;
  page?: number;
  size?: number;
  pages?: number;
  next?: string | null;
  previous?: string | null;
}

/* ========================= Livestream chat ============================== */


/* ============================ Feed / misc =============================== */

export interface FeedParams extends PaginationParams {
  category?: string;
  tag?: string;
}
