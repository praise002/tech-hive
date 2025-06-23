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
  image: string;
  title: string;
  description: string;
  tags: string[];
  reactions: string[];
  reactionsCount: number;
  posted: string;
  readTime: string;
}

export interface ArticleCardProps {
  article: Article;
  showAdminActions?: boolean;
  isOpen?: boolean;
  onMenuClick: (id: string) => void;
  context?: string;
}

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
  reactions: string[];
  reactionsCount: number;
  posted: string;
  readTime: string;
}

export interface BookmarkProps {
  className: string;
}

export interface TagsProps {
  tags: string[];
}

export interface ArticleTitleProps {
  children: React.ReactNode;
}

type ButtonVariant = 'primary' | 'outline' | 'gradient';
type ButtonType = 'button' | 'submit' | 'reset';

export interface ButtonProps {
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
  inputWidth: string;
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
  showAdminActions: boolean;
  visibleHeader?: boolean;
  context: string;
}