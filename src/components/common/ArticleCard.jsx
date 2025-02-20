import Description from './Description';
import Image from './Image';
import ArticleReactions from './ArticleReactions';
import Tags from './Tags';
import ArticleTitle from './ArticleTitle';
import Button from './Button';
import PropTypes from 'prop-types';

function ArticleCard({ article }) {
  return (
    <>
      <div className="relative overflow-hidden rounded-lg shadow-lg h-full flex flex-col">
        <Image
          alt={article.title}
          src={article.image}
          className="flex-shrink-0"
        />
        <div className="flex flex-col justify-between flex-grow p-5 border border-l border-r border-b border-gray rounded-bl-lg rounded-br-lg overflow-hidden">
          <div className="space-y-2">
            <ArticleTitle>{article.title}</ArticleTitle>
            <Description>{article.description}</Description>
            <Tags tags={article.tags} />
          </div>
          <div className="space-y-2">
            <Button className="w-auto" variant="outline">
              View details
            </Button>
            <ArticleReactions
              reactions={article.reactions}
              reactionsCount={article.reactionsCount}
              posted={article.posted}
              readTime={article.readTime}
            />
          </div>
        </div>
      </div>
      {/* <div className="relative overflow-hidden rounded-lg shadow-lg flex">
        <Image alt="Article" src="/src/assets/articles/the-future-ui-ux.jpg" />
        <div className="p-5 border-t border-r border-b border-gray rounded-br-lg rounded-tr-lg overflow-hidden">
          <ArticleTitle>{article.title}</ArticleTitle>
          <Description>{article.description}</Description>
          <Tags tags={article.tags} />
          <Button variant="outline">View details</Button>
          <ArticleReactions
            reactions={article.reactions}
            reactionsCount={article.reactionsCount}
            posted={article.posted}
            readTime={article.readTime}
          />
        </div>
      </div> */}
    </>
  );
}

ArticleCard.propTypes = {
  article: PropTypes.shape({
    image: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
    description: PropTypes.string.isRequired,
    tags: PropTypes.arrayOf(
      PropTypes.shape({
        name: PropTypes.string.isRequired,
        color: PropTypes.string.isRequired,
      })
    ).isRequired,
    reactions: PropTypes.arrayOf(PropTypes.string).isRequired,
    reactionsCount: PropTypes.number.isRequired,
    posted: PropTypes.string.isRequired,
    readTime: PropTypes.string.isRequired,
  }).isRequired,
};

export default ArticleCard;
