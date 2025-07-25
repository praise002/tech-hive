import { ButtonProps } from '../../types/types';

function Button({
  children,
  className = '',
  variant = 'primary',
  onClick,
  type = 'button',
  ...props
}: ButtonProps) {
  const baseStyles =
    'cursor-pointer focus-visible:outline-0 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-red-300 transition duration-300';

  const variants = {
    primary: 'bg-red text-white hover:bg-red-800',
    outline: 'border border-red text-red hover:bg-red-800 hover:text-white',
    gradient:
      'bg-gradient-to-r from-red-800 to-red-600 text-white hover:from-red-900 hover:to-red-700 hover:scale-105',
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

export default Button;
