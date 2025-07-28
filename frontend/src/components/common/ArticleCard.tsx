import Tags from './Tags';
import ArticleTitle from './ArticleTitle';

import { Link } from 'react-router-dom';

import Description from './Description';

import ArticleReactions from './ArticleReactions';
import Image from './Image';
import Button from './Button';
import { ArticleCardProps } from '../../types/types';

function ArticleCard({
  article,
  isOpen,
  onMenuClick = () => {},
  showAdminActions = false,
  context = 'published', // TODO: GET BACK TO WHAT IT IS LATER
}: ArticleCardProps) {
  return (
    <>
      <article className="relative overflow-hidden rounded-lg shadow-lg h-full flex flex-col">
        <Image
          alt={article.title}
          src={article.image}
          className="flex-shrink-0"
        />
        {showAdminActions && (
          <>
            <div className="absolute top-2 right-4">
              <button
                type="button"
                onClick={() => onMenuClick(article.id)}
                className="flex flex-col items-center justify-center gap-1 m-auto bg-red rounded-sm p-2"
                aria-label="Open article actions menu"
                aria-haspopup="true"
                aria-expanded={isOpen}
              >
                <p
                  className="bg-fill rounded-full w-1 h-1"
                  aria-hidden="true"
                ></p>
                <p
                  className="bg-fill rounded-full w-1 h-1"
                  aria-hidden="true"
                ></p>
                <p
                  className="bg-fill rounded-full w-1 h-1"
                  aria-hidden="true"
                ></p>
              </button>
            </div>
            {isOpen && (
              <div className="absolute top-15 right-2">
                <div
                  className="relative bg-custom-white text-gray-800 gap-2 py-3 px-5 w-25 flex flex-col items-start rounded-md"
                  role="menu"
                  aria-label="Article actions"
                >
                  {context === 'published' ? (
                    <>
                      <button role="menuitem">Edit</button>
                      <button role="menuitem">Archive</button>
                      <button role="menuitem">Delete</button>
                    </>
                  ) : (
                    <>
                      <button role="menuitem">Restore</button>
                      <button role="menuitem">Delete</button>
                    </>
                  )}

                  <div
                    className="absolute -top-3 right-3 w-4 h-4 bg-white"
                    style={{ clipPath: 'polygon(50% 0%, 0% 100%, 100% 100%)' }}
                    aria-hidden="true"
                  ></div>
                </div>
              </div>
            )}
          </>
        )}

        <div className="flex flex-col justify-between flex-grow p-5 border border-l border-r border-b border-gray dark:border-gray-700 rounded-bl-lg rounded-br-lg overflow-hidden">
          <div className="space-y-2">
            <ArticleTitle>{article.title}</ArticleTitle>
            <Description>{article.description}</Description>
            <Tags tags={article.tags} />
          </div>
          <div className="space-y-2">
            <Button className="w-auto" variant="outline">
              <Link to="/articles/a">View details</Link>
            </Button>
            <ArticleReactions
              reactions={article.reactions}
              reactionsCount={article.reactionsCount}
              posted={article.posted}
              readTime={article.readTime}
            />
          </div>
        </div>
      </article>
      {/* <div className="relative overflow-hidden rounded-lg shadow-lg flex">
        <Image alt="Article" src="/assets/articles/the-future-ui-ux.jpg" />
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

export default ArticleCard;
