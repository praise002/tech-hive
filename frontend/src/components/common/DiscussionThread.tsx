import { useState } from 'react';
import Like from './Like';
import Text from './Text';
import Button from './Button';
import { Comment } from '../../types';

function DiscussionThread() {
  const [comments, setComments] = useState<Comment[]>([
    {
      id: crypto.randomUUID(),
      author: 'Adebayo Abibat',
      text: 'This is really informative',
      timestamp: '2h',
      replies: [],
    },
  ]); // Stores the list of existing comments
  const [newComment, setNewComment] = useState<string>(''); // Tracks the user's input in the textarea
  const [replyText, setReplyText] = useState<Record<string, string>>({}); // For replies (keyed by comment ID)

  function handleAddComment() {
    if (newComment.trim() === '') return; // Prevent empty comments

    const newCommentObj = {
      id: crypto.randomUUID(),
      author: 'Praise Idowu',
      text: newComment,
      timestamp: 'Just now', // Replace with dynamic timestamp logic later
      replies: [],
    };

    setComments([newCommentObj, ...comments]);
    setNewComment(''); // Clear the textarea
  }

  function handleAddReply(commentId: string) {
    const reply = replyText[commentId]?.trim();

    if (!reply) return;

    setComments((prevComments) =>
      prevComments.map((comment) =>
        comment.id === commentId
          ? {
              ...comment,
              replies: [
                {
                  id: crypto.randomUUID(),
                  author: 'Praise Idowu',
                  text: reply,
                  timestamp: 'Just now',
                },
                ...comment.replies,
              ],
            }
          : comment
      )
    );

    setReplyText((prev) => ({ ...prev, [commentId]: '' })); // Clear the reply input
  }

  return (
    <div>
      {/* Comments */}
      <Text
        variant="h4"
        size="lg"
        bold={false}
        className="font-semibold dark:text-custom-white"
      >
        Comments ({comments.length})
      </Text>
      {/* Chat */}
      <div className="dark:text-custom-white">
        {/* New Chat */}
        <div className="flex gap-4 my-4">
          <div className="w-6 h-6 rounded-full border p-1">
            <img
              className="w-full h-full dark:invert"
              src="/src/assets/icons/iconamoon_profile-light.png"
              alt="Profile picture"
            />
          </div>
          <div className="flex-1">
            <textarea
              placeholder="Add to discussion"
              value={newComment}
              onChange={(e) => setNewComment(e.target.value)}
              className="resize-none w-full px-4 py-2 border border-color-text-secondary rounded-md focus:outline-none focus:ring-2 focus:ring-gray-800 focus:border-gray-800"
            ></textarea>
            <Button className="!px-4 text-sm mt-2" onClick={handleAddComment}>
              Post Comment
            </Button>
          </div>
        </div>

        {/* Existing Comments */}
        {comments.map((comment) => (
          <div className="my-4" key={comment.id}>
            <div className="flex gap-4">
              <div className="w-6 h-6">
                <img
                  className="h-full w-full rounded-full"
                  src="/src/assets/icons/profile.jpg"
                  alt="Profile icon"
                />
              </div>
              <div>
                <p className="font-bold">
                  {comment.author}{' '}
                  <span className="ml-2 text-xs">{comment.timestamp}</span>
                </p>
                <p className="text-sm">{comment.text}</p>
                <div className="flex gap-4 my-2">
                  <Like />
                  <div className="inline-flex gap-2 items-center">
                    <button
                      onClick={() =>
                        setReplyText((prev) => ({
                          ...prev,
                          [comment.id]: '',
                        }))
                      }
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        strokeWidth={1.5}
                        stroke="currentColor"
                        className="size-5"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 0 1-.923 1.785A5.969 5.969 0 0 0 6 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337Z"
                        />
                      </svg>
                    </button>
                    <span>Reply</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Reply Input Box */}
            {replyText[comment.id] !== undefined && (
              <div className="flex-1 ml-10">
                <textarea
                  placeholder="Write a reply..."
                  value={replyText[comment.id]}
                  onChange={(e) =>
                    setReplyText((prev) => ({
                      ...prev,
                      [comment.id]: e.target.value,
                    }))
                  }
                  className="resize-none  w-full px-4 py-2 border border-color-text-secondary rounded-md focus:outline-none focus:ring-2 focus:ring-gray-800 focus:border-gray-800"
                ></textarea>
                <Button
                  className="!px-4 text-sm mt-2"
                  onClick={() => handleAddReply(comment.id)}
                >
                  Post Reply
                </Button>
              </div>
            )}

            {/* Nested Replies */}
            {comment.replies.length > 0 && (
              <div className="ml-10 mt-2">
                {comment.replies.map((reply) => (
                  <div key={reply.id} className="flex gap-4 my-2">
                    <div className="w-6 h-6">
                      <img
                        className="h-full w-full rounded-full"
                        src="/src/assets/icons/profile.jpg"
                        alt="Profile picture"
                      />
                    </div>
                    <div>
                      <p className="font-bold">
                        {reply.author}
                        <span className="ml-2 text-xs">{reply.timestamp}</span>
                      </p>
                      <p className="text-sm">{reply.text}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default DiscussionThread;
