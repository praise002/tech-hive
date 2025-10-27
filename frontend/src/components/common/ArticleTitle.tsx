import { ArticleTitleProps } from '../../types/types';
import Text from './Text';

function ArticleTitle({ children }: ArticleTitleProps) {
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

export default ArticleTitle;
