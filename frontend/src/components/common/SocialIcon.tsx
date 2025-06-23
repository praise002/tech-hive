import { SocialIconProps } from "../../types";

export const SocialIcon = ({ href, icon: Icon }: SocialIconProps) => (
  <li>
    <a href={href}>
      <Icon className="h-6 text-gray-100 hover:text-gray-300 transition-colors" />
    </a>
  </li>
);
