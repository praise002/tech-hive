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
import { useArticleDetail } from '../../../hooks/useContent';
import { formatDateB, getPreviewText } from '../../../utils/utils';

function ArticleDetail() {
  const { username, slug } = useParams<{ username: string; slug: string }>();
  const { isPending, isError, article, error } = useArticleDetail(
    username!,
    slug!
  );

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
    slug: articleSlug,
    content,
    cover_image_url: coverImageUrl,
    read_time: readTime,
    status,
    created_at: createdAt,
    is_featured: isFeatured,
    author,
    total_reaction_counts: totalReactionCounts,
    reaction_counts: reactionCounts,
    tags,
    comments,
    comments_count: commentsCount,
  } = article;

  return (
    <>
      <CategoryBar />
      <div className="flex flex-col md:flex-row gap-8 px-4 md:px-10 py-8">
        {/* Left Column: Social Links */}
        <div className="hidden md:block px-10 mt-70">
          <SocialLinks
            visible={true}
            title={title}
            url={`${window.location.origin}/${username}/${slug}`}
            content={content}
            sharemsg={title}
          />
        </div>

        {/* Right Column: Content */}
        <div className="w-full md:w-3/4 mt-20 md:mt-10 border border-gray rounded-tl-lg rounded-tr-lg overflow-hidden">
          <Image
            alt="Article Image"
            src={coverImageUrl}
            className="w-full h-auto shadow-md"
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

            <p className="text-base md:text-lg leading-relaxed dark:text-custom-white">
              {content}
            </p>
            <Tags tags={tags} />
            <div className="flex justify-between my-4">
              <Reaction />
              <div>
                <Bookmark className="w-6 h-6 dark:invert" />
              </div>
            </div>
            <DiscussionThread />
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
          />
        </div>
      </div>
      <Rectangle />
      <Subscribe />
    </>
  );
}

export default ArticleDetail;
