import Spinner from '../../../components/common/Spinner';
import Text from '../../../components/common/Text';
import { formatDate } from '../../../utils/utils';
import { useUserComments } from '../hooks/useProfile';

interface Comment {
  id: string;
  article_title: string;
  body: string;
  created_at: string;
}

function CommentsContent() {
  const { isPending, isError, articles } = useUserComments();

  if (isPending) return <Spinner />;

  if (isError) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        Failed to load comments
      </div>
    );
  }

  if (!articles?.data?.results?.length)
    return <p className="font-bold text-sm">No recent comments available.</p>;

  return (
    <>
      <Text
        variant="h3"
        size="lg"
        bold={false}
        className="font-semibold mb-2 dark:text-custom-white"
      >
        Recent Comments
      </Text>
      {articles.data.results.map((comment: Comment) => (
        <div key={comment.id}>
          <div>
            {/* <Text
              variant="h3"
              size="base"
              bold={false}
              className="font-semibold mb-2 dark:text-custom-white"
            >
              {comment.article_title}
            </Text> */}
            <p className="text-secondary text-sm mb-1">{comment.article_title}</p>
          </div>
          <div className="flex items-center gap-2 text-xs md:text-sm">
            <p className="font-bold">{comment.body}</p>
            <p className="text-secondary">{formatDate(comment.created_at)}</p>
          </div>
        </div>
      ))}
    </>
  );
}

export default CommentsContent;
