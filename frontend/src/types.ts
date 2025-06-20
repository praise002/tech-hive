export interface ErrorFallbackProps {
  error: Error;
  resetErrorBoundary?: () => void;
}

type TextVariant = 'h1' | 'h2' | 'h3'| 'h4' | 'h5' | 'h6' | 'p';
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
  showAdminActions: boolean;
  isOpen: boolean;
  onMenuClick: (id: string) => void;
  context: string;
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
  variant: ButtonVariant;
  onClick?: () => void;
  type?: ButtonType;
}