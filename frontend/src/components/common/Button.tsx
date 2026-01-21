import { ButtonProps } from '../../types/types';

function Button({
  children,
  className = '',
  variant = 'primary',
  size = 'md',
  onClick,
  type = 'button',
  disabled,
  ...props
}: ButtonProps) {
  const baseStyles =
    'cursor-pointer focus-visible:outline focus-visible:outline-2 focus-visible:outline-red-800 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-red-300 transition duration-300 flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100';

  const sizes = {
    sm: 'min-w-[32px] min-h-[32px] px-3 py-1 text-xs rounded-md',
    md: 'min-w-[48px] min-h-[48px] px-6 py-2 text-base rounded-lg',
    lg: 'min-w-[64px] min-h-[64px] px-8 py-3 text-lg rounded-xl',
  };

  const variants = {
    primary: 'bg-red text-white hover:bg-red-800 disabled:hover:bg-red',
    outline:
      'border border-red text-red hover:bg-red-800 hover:text-white disabled:hover:bg-transparent disabled:hover:text-red',
    gradient:
      'bg-gradient-to-r from-red-800 to-red-600 text-white hover:from-red-900 hover:to-red-700 hover:scale-105 disabled:hover:from-red-800 disabled:hover:to-red-600',
  };

  const combinedClasses = `${baseStyles} ${sizes[size]} ${variants[variant]} ${className}`;

  return (
    <button
      type={type}
      className={combinedClasses}
      onClick={onClick}
      disabled={disabled}
      tabIndex={0}
      {...props}
    >
      {children}
    </button>
  );
}

export default Button;
