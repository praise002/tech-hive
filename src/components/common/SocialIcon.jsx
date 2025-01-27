import PropTypes from 'prop-types';

export const SocialIcon = ({ href, icon: Icon }) => (
  <li className="border-purple-700 border rounded-full p-2 bg-customGray flex items-center justify-center hover:bg-lime-500 hover:border-lime-500 transition-colors">
    <a href={href}>
      <Icon className="text-white" />
    </a>
  </li>
);

SocialIcon.propTypes = {
  href: PropTypes.string.isRequired,
  icon: PropTypes.elementType.isRequired,
};
