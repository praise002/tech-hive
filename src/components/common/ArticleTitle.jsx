import Text from './Text';
import PropTypes from 'prop-types';

function ArticleTitle({ children }) {
  return (
    <Text
      variant="h4"
      bold={false}
      className="font-semibold sm:text-xl dark:text-custom-white"
      size="lg"
    >
      {children}
    </Text>
  );
}

ArticleTitle.propTypes = {
  children: PropTypes.node.isRequired,
};



export default ArticleTitle;
