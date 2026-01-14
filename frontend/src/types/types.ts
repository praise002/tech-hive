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

export interface Article {
  id: string;
  title: string;
  slug: string;
  content: string;
  cover_image_url: string;
  read_time: number;
  status: string;
  created_at: string;
  is_featured: boolean;
  author: string;
  total_reaction_counts: number;
  reaction_counts: {
    [key: string]: number;
  };
  tags: Array<{
    id: string;
    name: string;
  }>;
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
    [key: string]: number;
  };
  total_reaction_counts: number;
  created_at: string;
  read_time: number;
}

export interface BookmarkProps {
  className: string;
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

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  className?: string;
  variant?: ButtonVariant;
  onClick?: () => void;
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

interface Event {
  title: string;
  organizer: string;
  date: string;
  location: string;
  type: string;
  lastPosted: string;
}

export interface EventCardProps {
  event: Event;
}

interface Job {
  title: string;
  company: string;
  lastPosted: string;
  tags: string[];
}

export interface JobPostingCardProps {
  job: Job;
}

export interface JobTagsProps {
  tags: string[];
}

interface Resource {
  resourceName: string;
  resourceImage: string;
  resourceType: string;
  resourceDescription: string;
  resourceCategories: string[];
  timePosted: string;
}

export interface ResourceCardProps {
  resource: Resource;
}

export interface SearchInputProps {
  inputWidth?: string;
  iconSize: string;
}

interface Tool {
  toolName: string;
  toolImage: string;
  toolDescription: string;
  toolCategories: string[];
  callToAction: string;
  link: string;
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

export interface ArticleReply {
  id: string;
  body: string;
  created_at: string;
  user_name: string;
  user_username: string;
  user_avatar: string;
  replying_to_name: string;
  replying_to_username: string;
}

export interface ArticleComment {
  id: string;
  thread_id: string;
  body: string;
  created_at: string;
  user_name: string;
  user_username: string;
  user_avatar: string;
  total_replies: number;
  replies?: ArticleReply[]; // Optional: only loaded when user clicks "View replies"
}

export interface ArticleDetail extends Article {
  comments: ArticleComment[];
  comments_count: number;
}

export interface DiscussionThreadProps {
  comments: ArticleComment[];
  commentsCount: number;
  articleId: string;
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

export interface ApiResponse<T = any> {
  status: 'success' | 'error';
  message: string;
  data?: T;
  error_code?: string;
  errors?: Record<string, string[]>;
}


// TODO: REMOVE SOME STUFFS