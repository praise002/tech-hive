import PropTypes from 'prop-types';
function Description({ children }) {
  return <p className="text-[#262a2a]">{children}</p>;
}

Description.propTypes = {
  children: PropTypes.node.isRequired,
};

export default Description;
