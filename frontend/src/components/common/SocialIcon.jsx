import PropTypes from 'prop-types';

export const SocialIcon = ({ href, icon: Icon }) => (
  <li>
    <a href={href}>
      <Icon className="h-6 text-gray-100 hover:text-gray-300 transition-colors" />
    </a>
  </li>
);

SocialIcon.propTypes = {
  href: PropTypes.string.isRequired,
  icon: PropTypes.elementType.isRequired,
};
