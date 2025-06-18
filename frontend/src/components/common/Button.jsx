import PropTypes from 'prop-types';

function Button({
  children,
  className = '',
  variant = 'primary',
  onClick,
  type = 'button',
  ...props
}) {
  const baseStyles =
    'cursor-pointer focus-visible:outline-0 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-red-300 transition duration-300';

  const variants = {
    primary: 'bg-red text-gray-100 hover:bg-red-800',
    outline: 'border border-red text-red hover:bg-red-800 hover:text-white',
    gradient:
      'bg-gradient-to-r from-red to-primary-light text-gray-100 hover:from-red-800 hover:to-orange-500 hover:scale-105',
  };

  const combinedClasses = `${baseStyles} ${variants[variant]} ${className}`;

  return (
    <button
      type={type}
      className={`px-6 py-2 rounded-lg ${combinedClasses}`}
      onClick={onClick}
      {...props}
    >
      {children}
    </button>
  );
}

Button.propTypes = {
  children: PropTypes.node.isRequired, // Content inside the button (text, icons, etc.)
  className: PropTypes.string, // Additional custom classes
  variant: PropTypes.oneOf(['primary', 'outline', 'gradient']), // Button style variant
  onClick: PropTypes.func, // Click handler function
  type: PropTypes.oneOf(['button', 'submit', 'reset']), // Button type
};

export default Button;
