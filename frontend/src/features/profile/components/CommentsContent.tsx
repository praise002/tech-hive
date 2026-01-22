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

interface CommentsContentProps {
  username?: string;
}

function CommentsContent({ username }: CommentsContentProps) {
  const { isPending, isError, comments } = useUserComments();

  if (isPending) return <Spinner />;

  if (isError) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        Failed to load comments
      </div>
    );
  }

  if (!comments?.data?.results?.length)
    return (
      <div className="text-center py-20 text-secondary">
        <p>
          {username
            ? 'No recent comments found.'
            : 'No recent comments available.'}
        </p>
      </div>
    );

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
      {comments.data.results.map((comment: Comment) => (
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
            <p className="text-secondary text-sm mb-1">
              {comment.article_title}
            </p>
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
