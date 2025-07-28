import { SocialIconProps } from '../../types/types';

export const SocialIcon = ({
  href,
  icon: Icon,
  ariaLabel,
}: SocialIconProps) => (
  <li>
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      aria-label={ariaLabel}
    >
      <Icon className="h-6 text-gray-100 hover:text-gray-300 transition-colors" />
    </a>
  </li>
);
