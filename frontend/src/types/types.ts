export interface ErrorFallbackProps {
  error: Error;
  resetErrorBoundary?: () => void;
}

type TextVariant = 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6' | 'p';
type TextSize = 'xs' | 'sm' | 'base' | 'lg' | 'xl' | '2xl' | '3xl' | '4xl';
type TextAlign = 'left' | 'center' | 'right';

export interface TextProps {
  children: React.ReactNode;
  variant?: TextVariant;
  className?: string;
  size?: TextSize;
  align?: TextAlign;
  bold?: boolean;
  color?: string;
}

export interface MarkdownTagsProps {
  tags: string[];
  mode: 'edit' | 'preview';
  onRemove: (tag: string) => void;
}

// Version 1: showAdminActions is true, onMenuClick is REQUIRED
interface PropsWithAdminActions {
  showAdminActions: true;
  isOpen: boolean;
  onMenuClick: (id: string) => void;
  article: Article;
  context?: string;
}

// Version 2: showAdminActions is false, onMenuClick is OPTIONAL
interface PropsWithoutAdminActions {
  showAdminActions?: false;
  isOpen?: boolean;
  onMenuClick?: (id: string) => void;
  article: Article;
  context?: string;
}

// Combine the two versions using a union type
export type ArticleCardProps = PropsWithAdminActions | PropsWithoutAdminActions;

export interface DescriptionProps {
  children: React.ReactNode;
}

export interface ImageProps {
  src: string;
  alt: string;
  className: string;
  imgClassName?: string;
}

export interface ArticleReactionsProps {
  reaction_counts: {
    [key: string]: number | undefined;
  };
  total_reaction_counts: number;
  created_at?: string;
  read_time: number;
  articleId: string;
}

export interface BookmarkProps {
  className: string;
  articleId: string;
}

export interface TagsProps {
  tags: Array<{
    id: string;
    name: string;
  }>;
}

export interface ArticleTitleProps {
  children: React.ReactNode;
}

type ButtonVariant = 'primary' | 'outline' | 'gradient';
type ButtonType = 'button' | 'submit' | 'reset';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  className?: string;
  variant?: ButtonVariant;
  size?: 'sm' | 'md' | 'lg';
  type?: ButtonType;
}

interface Reply {
  id: string;
  author: string;
  text: string;
  timestamp: string;
}

export interface Comment {
  id: string;
  author: string;
  text: string;
  timestamp: string;
  replies: Reply[];
}

import { Article } from './article';
import type { Event, Job, Resource, Tool } from './content';
export type { Event, Job, Resource, Tool };

export interface EventCardProps {
  event: Event;
}

export interface JobPostingCardProps {
  job: Job;
}

export interface JobTagsProps {
  tags: string[];
}

export interface ResourceCardProps {
  resource: Resource;
}

export interface SearchInputProps {
  inputWidth?: string;
  iconSize: string;
}

export interface ToolCardProps {
  tool: Tool;
}

export interface SocialIconProps {
  href: string;
  icon: React.ComponentType<{ className?: string }>;
  ariaLabel: string;
}

export interface SocialLinksProps {
  visible: boolean;
  title: string;
  sharemsg: string;
  content?: string;
  url: string;
  onSummarize?: (forceRegenerate?: boolean) => void;
  summaryContent?: string | null;
  isSummarizing?: boolean;
  summaryError?: string | null;
}

export interface ToolTipProps {
  children: React.ReactNode;
  text: string;
  position?: string;
}

export interface ArticlesProps {
  marginTop?: number;
  showAdminActions?: boolean;
  visibleHeader?: boolean;
  context?: string;
  category?: string;
}

export interface MarkdownTagsProps {
  tags: string[];
  onRemove: (tag: string) => void;
}

export interface KeyboardEvent extends React.KeyboardEvent<HTMLInputElement> {
  key: string;
}

export interface TagInputProps {
  tags: string[];
  suggestedTags: string[];
  onAddTag: (tag: string) => void;

  value?: string;
  onInputChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onInputKeyDown?: (e: KeyboardEvent) => void;
  maxTags?: number;
}

export interface ProtectedRouteProps {
  children: React.ReactNode;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// ============================================================================
// API RESPONSE WRAPPER (from your CustomResponse backend)
// ============================================================================

export interface ApiResponse<T = unknown> {
  status: 'success' | 'error';
  message: string;
  data?: T;
  error_code?: string;
  errors?: Record<string, string[]>;
}

// GENERAL

export interface SiteDetail {
  image_url: string;
  body: string;
  fb: string;
  ln: string;
  x: string;
  ig: string;
}

export interface NewsletterSubscribeRequest {
  email: string;
}

export interface NewsletterUnsubscribeParams {
  email: string;
}

export interface ContactRequest {
  name: string;
  email: string;
  content: string;
}

export interface Notification {
  id: string;
  recipient_name: string;
  verb: string;
  is_read: boolean;
  is_deleted: boolean;
  created_at: string;
  actor_name: string;
  actor_avatar: string | null;
  description: string;
  target_content_type: string | null;
  target_object_id: string | null;
  target_slug: string | null;
  target_username: string | null;
}

export interface User {
  id: string;
  email: string;
  created_at: string;
  first_name: string;
  last_name: string;
  username: string;
  avatar_url: string;
  role: string;
}
