import PropTypes from 'prop-types';

function Text({
  children,
  variant = 'p',
  className = '',
  size = 'base',
  align = 'left',
  bold = true,
  color = 'gray-800',
  ...props
}) {
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

  const VariantElement = ({ children, ...props }) => {
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

Text.propTypes = {
  children: PropTypes.node.isRequired, 
  variant: PropTypes.oneOf(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']), 
  className: PropTypes.string, // Additional custom classes
  size: PropTypes.oneOf(['xs', 'sm', 'base', 'lg', 'xl', '2xl', '3xl', '4xl']), // Size of the text
  align: PropTypes.oneOf(['left', 'center', 'right']), 
  bold: PropTypes.bool, 
  color: PropTypes.string, // Text color (Tailwind color class)
};

export default Text;
