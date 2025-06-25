import { TextProps } from '../../types/types';

function Text({
  children,
  variant = 'p',
  className = '',
  size = 'base',
  align = 'left',
  bold = true,
  color = 'gray-800',
  ...props
}: TextProps) {
  const sizeClasses = {
    xs: 'text-xs',
    sm: 'text-sm',
    base: 'text-base',
    lg: 'text-lg',
    xl: 'text-xl',
    '2xl': 'text-2xl',
    '3xl': 'text-3xl',
    '4xl': 'text-4xl',
  };

  const alignClasses = {
    left: 'text-left',
    center: 'text-center',
    right: 'text-right',
  };

  const VariantElement = ({
    children,
    ...props
  }: { children: React.ReactNode } & React.HTMLAttributes<HTMLElement>) => {
    switch (variant) {
      case 'h1':
        return <h1 {...props}>{children}</h1>;
      case 'h2':
        return <h2 {...props}>{children}</h2>;
      case 'h3':
        return <h3 {...props}>{children}</h3>;
      case 'h4':
        return <h4 {...props}>{children}</h4>;
      case 'h5':
        return <h5 {...props}>{children}</h5>;
      case 'h6':
        return <h6 {...props}>{children}</h6>;
      default:
        return <p {...props}>{children}</p>;
    }
  };

  const combinedClasses = `${bold ? 'font-bold' : ''}  ${sizeClasses[size]} ${
    alignClasses[align]
  } text-${color} ${className}`;

  return (
    <VariantElement className={combinedClasses} {...props}>
      {children}
    </VariantElement>
  );
}

export default Text;
