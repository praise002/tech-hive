import { useState } from 'react';
import { useParams } from 'react-router-dom';
import Bookmark from '../../../components/common/Bookmark';
import DiscussionThread from '../../../components/common/DiscussionThread';
import Image from '../../../components/common/Image';
import Reaction from '../../../components/common/Reaction';
import Rectangle from '../../../components/common/Rectangle';
import SocialLinks from '../../../components/common/SocialLinks';
import Spinner from '../../../components/common/Spinner';
import Tags from '../../../components/common/Tags';
import Text from '../../../components/common/Text';
import CategoryBar from '../../../components/sections/CategoryBar';
import Subscribe from '../../../components/sections/Subscribe';

import {
  useArticleDetail,
  useGenerateArticleSummary,
} from '../hooks/useArticle';
import { formatDateB, getPreviewText } from '../../../utils/utils';
import { ArticleSummaryData } from '../../../types/article';

function ArticleDetail() {
  const { username, slug } = useParams<{ username: string; slug: string }>();
  const { isPending, isError, article, error } = useArticleDetail(
    username!,
    slug!
  );

  const [summaryData, setSummaryData] = useState<ArticleSummaryData | null>(
    null
  );
  const {
    generateArticleSummary,
    isPending: isSummarizing,
    error: summaryError,
  } = useGenerateArticleSummary();

  const handleSummarize = (forceRegenerate: boolean = false) => {
    generateArticleSummary(
      { articleId: article?.id || '', forceRegenerate },
      {
        onSuccess: (data) => {
          setSummaryData(data as unknown as ArticleSummaryData);
        },
      }
    );
  };

  if (isPending) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spinner />
      </div>
    );
  }

  if (isError || !article) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-red-600">Error</h2>
          <p className="text-gray-600 mt-2">
            {error?.message || 'Article not found'}
          </p>
        </div>
      </div>
    );
  }

  const {
    id: articleId,
    title,
    content,
    created_at: createdAt,
    author,
    tags,
    comments,
    comments_count: commentsCount,
  } = article;

  return (
    <>
      <CategoryBar />
      <div className="flex flex-col md:flex-row gap-8 px-4 md:px-10 py-8 min-h-screen">
        {/* Left Column: Social Links */}
        <div className="hidden md:block px-10 mt-70">
          <SocialLinks
            visible={true}
            title={title}
            url={`${window.location.origin}/${username}/${slug}`}
            content={content}
            sharemsg={title}
            onSummarize={handleSummarize}
            summaryContent={summaryData?.summary}
            isSummarizing={isSummarizing}
            summaryError={summaryError?.message}
          />
        </div>

        {/* Right Column: Content */}
        <div className="w-full md:w-3/4 mt-20 md:mt-10 border border-gray rounded-tl-lg rounded-tr-lg overflow-hidden">
          <Image
            alt="Article Image"
            src="/assets/articles/the-future-ui-ux.jpg"
            className="w-full h-64 md:h-96 object-cover shadow-md"
          />
          <div className="px-4 py-6 border border-secondary text-primary">
            <div className="my-4 text-xs text-secondary">
              Posted {formatDateB(createdAt)} ago
            </div>
            <Text
              variant="h3"
              size="xl"
              bold={false}
              className="font-semibold dark:text-custom-white"
            >
              {title}
            </Text>

            {/* Optional Author if a contributor */}
            <div className="flex items-center gap-4 my-4">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-full overflow-hidden">
                  <Image
                    alt={author.name}
                    src={author.avatar}
                    className="w-full h-full"
                  />
                </div>
                <Text
                  variant="h3"
                  size="base"
                  bold={false}
                  className="dark:text-custom-white"
                >
                  {author.name}
                </Text>
              </div>
            </div>

            <div
              className="text-base md:text-lg leading-relaxed dark:text-custom-white prose lg:prose-xl max-w-none start-article"
              dangerouslySetInnerHTML={{ __html: content }}
            />
            <Tags tags={tags} />
            <div className="flex justify-between my-4">
              <Reaction articleId={articleId} />
              <div>
                <Bookmark
                  className="w-6 h-6 dark:invert"
                  articleId={articleId}
                />
              </div>
            </div>
            <DiscussionThread
              comments={comments}
              commentsCount={commentsCount}
              articleId={articleId}
            />
          </div>
        </div>

        {/* Mobile social link */}
        <div className="block md:hidden">
          <SocialLinks
            visible={true}
            title={title}
            url={`${window.location.origin}/${username}/${slug}`}
            content={getPreviewText(content, 200)}
            sharemsg={title}
            onSummarize={handleSummarize}
            summaryContent={summaryData?.summary}
            isSummarizing={isSummarizing}
            summaryError={summaryError?.message}
          />
        </div>
      </div>
      <Rectangle />
      <Subscribe />
    </>
  );
}

export default ArticleDetail;
