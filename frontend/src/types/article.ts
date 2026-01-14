import { Category } from './content';
import { PaginatedResponse } from './types';

export enum ArticleStatus {
  DRAFT = 'draft',
  SUBMITTED = 'submitted',
  UNDER_REVIEW = 'under_review',
  CHANGES_REQUESTED = 'changes_requested',
  APPROVED = 'approved',
  READY_FOR_PUBLISHING = 'ready_for_publishing',
  PUBLISHED = 'published',
  REJECTED = 'rejected',
  ARCHIVED = 'archived',
}

export interface User {
  id: string;
  name: string;
  username: string;
  avatar_url: string;
}

export interface EditorUser {
  id: string;
  name: string;
  avatar_url: string;
}

export interface Tag {
  id: string;
  name: string;
}

export type TagsResponse = Tag[];

export interface ArticleAuthor {
  name: string;
  avatar: string;
}

export interface ReactionCounts {
  '❤️'?: number;
  '👍'?: number;
  '🔥'?: number;
  '🎉'?: number;
  '💯'?: number;
  [key: string]: number | undefined;
}

export interface Article {
  id: string;
  title: string;
  slug: string;
  content: string;
  cover_image_url: string | null;
  read_time: number;
  status: ArticleStatus;
  created_at: string;
  is_featured: boolean;
  author: ArticleAuthor;
  total_reaction_counts: number;
  reaction_counts: ReactionCounts;
  tags: Tag[];
}

export type ArticlesResponse = PaginatedResponse<Article>;

export interface Comment {
  id: string;
  thread_id: string;
  body: string;
  created_at: string;
  user_name: string;
  user_username: string;
  user_avatar: string;
  total_replies: number;
}

export interface ArticleDetail extends Article {
  comments: Comment[];
  comments_count: number;
}

export interface CommentCreateRequest {
  article_id: string;
  body: string;
  thread_id?: string; // Optional - if provided, creates a reply
}

export interface CommentCreateResponse {
  id: string;
  thread_id: string;
  body: string;
  created_at: string;
  user_name: string;
  user_username: string;
  user_avatar: string;
  is_root: boolean;
}

export interface ThreadReply {
  id: string;
  body: string;
  created_at: string;
  user_name: string;
  user_username: string;
  user_avatar: string;
}

export interface CommentLikeStatus {
  comment_id: string;
  like_count: number;
  is_liked: boolean | null; // null for unauthenticated users
}

export interface CommentLikeToggleResponse {
  comment_id: string;
  is_liked: boolean;
  like_count: number;
}

export interface ArticleSummaryResponse {
  article_id: string;
  article_title: string;
  article_slug: string;
  summary: string;
  cached: boolean;
}

export type ReactionType = '❤️' | '😍' | '👍' | '🔥';

export interface ArticleReactionToggleRequest {
  reaction_type: ReactionType;
}

export interface ArticleReactionToggleResponse {
  article_id: string;
  action: 'added' | 'removed';
  is_reacted: boolean;
  reaction_counts: ReactionCounts;
  total_reactions: number;
}

export interface ArticleReactionStatisticsResponse {
  article_id: string;
  reaction_counts: ReactionCounts;
  total_reactions: number;
  user_reactions: ReactionType[] | null; // null if not authenticated
}

export interface ArticleEditorResponse {
  id: string;
  category: Category | null;
  title: string;
  slug: string;
  content: string;
  cover_image_url: string | null;
  status: ArticleStatus;
  liveblocks_room_id: string;
  user_can_edit: boolean;
  is_published: boolean;
  author: EditorUser;
  assigned_reviewer: EditorUser | null;
  assigned_editor: EditorUser | null;
  tags: Tag[];
  created_at: string;
  content_last_synced_at: string | null;
  updated_at: string;
}

export interface ArticleSubmitResponse {
  status: ArticleStatus;
  is_resubmission: boolean;
}

export interface ArticleForReview {
  id: string;
  title: string;
  status: ArticleStatus;
  author: User;
  created_at: string;
  updated_at: string;
  liveblocks_room_id: string;
}

export enum ReviewStatus {
  PENDING = 'pending',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
}

export interface ReviewListItem {
  id: string;
  article: ArticleForReview;
  reviewed_by: User;
  status: ReviewStatus;
  started_at: string | null;
  completed_at: string | null;
}

export type AssignedReviewsResponse = PaginatedResponse<ReviewListItem>;

export interface WorkflowHistoryEntry {
  id: string;
  from_status: ArticleStatus;
  to_status: ArticleStatus;
  changed_by: User;
  changed_at: string;
  notes: string | null;
}

export interface ArticleDetailForReview {
  id: string;
  title: string;
  content: string;
  cover_image_url: string | null;
  status: ArticleStatus;
  author: User;
  assigned_reviewer: User | null;
  assigned_editor: User | null;
  created_at: string;
  updated_at: string;
  liveblocks_room_id: string;
  content_last_synced_at: string | null;
}

export interface ReviewDetail {
  id: string;
  article: ArticleDetailForReview;
  reviewed_by: User;
  status: ReviewStatus;
  started_at: string | null;
  completed_at: string | null;
  reviewer_notes: string | null; // Only visible to reviewer
  workflow_history: WorkflowHistoryEntry[];
}

export interface ReviewActionRequest {
  reviewer_notes?: string;
}

export interface ReviewStartResponse {
  review_status: ReviewStatus;
  article_status: ArticleStatus;
  started_at: string;
}

export interface ReviewActionResponse {
  article_status: ArticleStatus;
  completed_at: string;
}

export interface ReviewApproveResponse {
  article_status: ArticleStatus;
  assigned_editor: User;
  completed_at: string;
}

// ============================================================================
// GROUP 8: LIVEBLOCKS
// ============================================================================

export interface LiveblocksAuthRequest {
  room_id: string;
}

export interface LiveblocksAuthResponse {
  token: string;
  user_id: string;
}

export interface UserMention {
  id: string;
  name: string;
  avatar_url: string;
  cursor_color: string;
}

export interface UserSearchParams {
  q: string;
  room_id: string;
}

export type UserSearchResponse = UserMention[];

export interface UserBatchRequest {
  user_ids: string[];
}

export type UserBatchResponse = UserMention[];

export interface RssFeedInfo {
  rss_url: string;
  description: string;
  format: string;
  items_count: number;
  update_frequency: string;
}