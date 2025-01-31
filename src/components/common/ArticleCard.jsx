import ArticleDescription from './ArticleDescription';
import ArticleImage from './ArticleImage';
import ArticleReactions from './ArticleReactions';
import ArticleTags from './ArticleTags';
import ArticleTitle from './ArticleTitle';
import Button from './Button';

function ArticleCard() {
  return (
    <div>
      <ArticleImage />
      <div>
        <ArticleTitle />
        <ArticleDescription />
        <ArticleTags />
        <Button variant="outline">View details</Button>
        <ArticleReactions />
      </div>
    </div>
  );
}

export default ArticleCard;
