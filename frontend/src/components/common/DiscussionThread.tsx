import { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import Like from './Like';
import Text from './Text';
import Button from './Button';
import Spinner from './Spinner';

import { formatDateB } from '../../utils/utils';
import {
  useCreateComment,
  useUpdateComment,
} from '../../features/articles/hooks/useArticle';
import { useCurrentUser } from '../../features/profile/hooks/useProfile';
import { useAuthModal } from '../../context/AuthModalContext';
import { useProfileApi } from '../../features/profile/hooks/useProfileApi';
import { useArticleApi } from '../../features/articles/hooks/useArticleApi';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import {
  ArticleComment,
  DiscussionThreadProps,
  User,
} from '../../types/article';

function DiscussionThread({
  comments: initialComments,
  commentsCount,
  articleId,
}: DiscussionThreadProps) {
  const [comments, setComments] = useState<ArticleComment[]>(initialComments);
  const [newComment, setNewComment] = useState<string>('');
  const [replyText, setReplyText] = useState<Record<string, string>>({});
  const navigate = useNavigate();
  const location = useLocation();

  const handleUnauthenticated = () => {
    navigate('/login');
  };

  const { createComment, isPending: isSubmitting } = useCreateComment(
    handleUnauthenticated
  );

  const { updateComment, isPending: isUpdatingComment } = useUpdateComment(
    handleUnauthenticated
  );
  const { getThreadReplies } = useArticleApi();
  const { isAuthenticated, user } = useCurrentUser();
  const { openAuthModal } = useAuthModal();
  const { getUsernames } = useProfileApi();
  const [loadingReplies, setLoadingReplies] = useState<Record<string, boolean>>(
    {}
  );
  const [editingCommentId, setEditingCommentId] = useState<string | null>(null);
  const [editBody, setEditBody] = useState<string>('');

  // Mention State
  const [mentionQuery, setMentionQuery] = useState('');
  const [suggestions, setSuggestions] = useState<User[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [activeCommentId, setActiveCommentId] = useState<string | null>(null); // To know which reply box is active

  // Sync state with props when they change (due to refetching)
  useEffect(() => {
    setComments(initialComments);
  }, [initialComments]);

  // Handle Mention Suggestions
  useEffect(() => {
    if (mentionQuery.length > 0) {
      const fetchSuggestions = async () => {
        try {
          const data = await getUsernames({
            search: mentionQuery,
            page_size: 5,
          });
          setSuggestions(data.results);
          setShowSuggestions(true);
        } catch (error) {
          console.error('Failed to fetch suggestions', error);
          setShowSuggestions(false);
        }
      };

      const timeoutId = setTimeout(fetchSuggestions, 300); // Debounce
      return () => clearTimeout(timeoutId);
    } else {
      setShowSuggestions(false);
    }
  }, [mentionQuery, getUsernames]);

  // Scroll to comment if hash is present in URL (from notification click)
  useEffect(() => {
    if (location.hash && comments.length > 0) {
      const commentId = location.hash.replace('#comment-', '');
      console.log('🔍 Looking for comment:', commentId);
      console.log('📋 Root comments loaded:', comments.length);

      const scrollToElement = () => {
        const element = document.getElementById(`comment-${commentId}`);
        if (element) {
          console.log('✅ Found element, scrolling...');
          element.scrollIntoView({ behavior: 'smooth', block: 'center' });
          element.classList.add('bg-blue-50', 'dark:bg-blue-900/20');
          setTimeout(() => {
            element.classList.remove('bg-blue-50', 'dark:bg-blue-900/20');
          }, 2000);
          return true;
        }
        console.log('❌ Element not found in DOM');
        return false;
      };

      // Try immediate scroll (works for root comments)
      if (scrollToElement()) return;

      // If not found, it's likely a reply - load all threads with replies
      const loadRepliesAndScroll = async () => {
        console.log('🔄 Not a root comment, checking replies...');

        for (const comment of comments) {
          if (comment.total_replies > 0) {
            // Check if replies are already loaded
            if (!comment.replies || comment.replies.length === 0) {
              try {
                console.log(
                  `⬇️ Loading ${comment.total_replies} replies for comment ${comment.id}...`
                );
                const replies = await getThreadReplies(comment.id);
                console.log(`📥 Loaded ${replies.length} replies`);

                // Check if our target is in these replies
                const foundReply = replies.find(
                  (r: { id: string }) => r.id === commentId
                );
                if (foundReply) {
                  console.log('🎯 Found target reply! Updating state...');
                  setComments((prev) =>
                    prev.map((c) =>
                      c.id === comment.id ? { ...c, replies } : c
                    )
                  );
                  // Wait for DOM update then scroll
                  setTimeout(() => {
                    if (scrollToElement()) {
                      console.log('✨ Successfully scrolled to reply!');
                    }
                  }, 600);
                  return;
                }
              } catch (error) {
                console.error('❌ Failed to load replies:', error);
              }
            } else {
              // Replies already loaded, check if target is there
              const foundReply = comment.replies.find(
                (r) => r.id === commentId
              );
              if (foundReply) {
                console.log('🎯 Found in already-loaded replies');
                setTimeout(scrollToElement, 300);
                return;
              }
            }
          }
        }
        console.log('❌ Comment not found anywhere');
      };

      // Delay to let page render first
      setTimeout(loadRepliesAndScroll, 500);
    }
  }, [location.hash, comments, getThreadReplies]);

  function handleInputChange(
    text: string,
    commentId: string | null = null // null for main comment
  ) {
    if (commentId) {
      setReplyText((prev) => ({ ...prev, [commentId]: text }));
      setActiveCommentId(commentId);
    } else {
      setNewComment(text);
      setActiveCommentId('main');
    }

    // Detect if valid mention trigger
    const lastWord = text.split(/\s+/).pop();
    if (lastWord && lastWord.startsWith('@') && lastWord.length > 1) {
      setMentionQuery(lastWord.slice(1));
    } else {
      setMentionQuery('');
      setShowSuggestions(false);
    }
  }

  function insertMention(username: string) {
    const textToUpdate =
      activeCommentId === 'main' ? newComment : replyText[activeCommentId!];
    const words = textToUpdate.split(/\s+/);
    words.pop(); // Remove the partial mention
    const newText = [...words, `@${username} `].join(' ');

    if (activeCommentId === 'main') {
      setNewComment(newText);
    } else if (activeCommentId) {
      setReplyText((prev) => ({ ...prev, [activeCommentId]: newText }));
    }

    setMentionQuery('');
    setShowSuggestions(false);
    // Focus back would be ideal but simpler to just close for now
  }

  // Helper to check if comment was edited (updated_at > created_at by more than 1 minute)
  function isCommentEdited(createdAt: string, updatedAt?: string): boolean {
    if (!updatedAt) return false;
    const created = new Date(createdAt).getTime();
    const updated = new Date(updatedAt).getTime();
    const diffInSeconds = (updated - created) / 1000;
    return diffInSeconds > 60; // Grace period of 1 minute
  }

  // Helper function to render text with clickable mentions
  function renderTextWithMentions(text: string) {
    // Regex to match @username (alphanumeric, underscore, hyphen)
    const mentionRegex = /@([a-zA-Z0-9_-]+)/g;
    const parts: (string | JSX.Element)[] = [];
    let lastIndex = 0;
    let match;

    while ((match = mentionRegex.exec(text)) !== null) {
      // Add text before the mention
      if (match.index > lastIndex) {
        parts.push(text.substring(lastIndex, match.index));
      }

      // Add the mention as a clickable link
      const username = match[1];
      parts.push(
        <Link
          key={`mention-${match.index}`}
          to={`/profile/${username}`}
          className="text-blue-600 dark:text-blue-400 hover:underline font-medium"
          onClick={(e) => e.stopPropagation()}
        >
          @{username}
        </Link>
      );

      lastIndex = match.index + match[0].length;
    }

    // Add remaining text after last mention
    if (lastIndex < text.length) {
      parts.push(text.substring(lastIndex));
    }

    return parts.length > 0 ? parts : text;
  }

  function handleAddComment(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (!newComment.trim()) return;

    createComment(
      { article_id: articleId, body: newComment },
      {
        onSuccess: (response) => {
          toast.success(response?.message || 'Comment posted successfully');
          setNewComment('');
        },
        onError: (error: any) => {
          toast.error(error?.message || 'Failed to post comment');
        },
      }
    );
  }

  function handleAddReply(commentId: string, threadId: string) {
    const reply = replyText[commentId]?.trim();
    if (!reply) return;

    createComment(
      { article_id: articleId, thread_id: threadId, body: reply },
      {
        onSuccess: (response) => {
          toast.success(response?.message || 'Reply posted successfully');
          setReplyText((prev) => {
            const newState = { ...prev };
            delete newState[commentId];
            return newState;
          });
        },
        onError: (error: any) => {
          toast.error(error?.message || 'Failed to post reply');
        },
      }
    );
  }

  async function handleViewReplies(commentId: string) {
    setLoadingReplies((prev) => ({ ...prev, [commentId]: true }));
    try {
      const replies = await getThreadReplies(commentId);
      setComments((prevComments) =>
        prevComments.map((c) =>
          c.id === commentId ? { ...c, replies: replies } : c
        )
      );
    } catch (error) {
      console.error('Failed to load replies', error);
    } finally {
      setLoadingReplies((prev) => ({ ...prev, [commentId]: false }));
    }
  }

  function handleEditClick(commentId: string, currentBody: string) {
    setEditingCommentId(commentId);
    setEditBody(currentBody);
  }

  function handleUpdateComment(commentId: string) {
    if (!editBody.trim()) return;

    updateComment(
      { commentId, body: editBody },
      {
        onSuccess: (response) => {
          toast.success(response?.message || 'Comment updated successfully');
          setEditingCommentId(null);

          // Get current timestamp for updated_at
          const now = new Date().toISOString();

          setComments((prevComments) =>
            prevComments.map((c) => {
              if (c.id === commentId) {
                // Update root comment
                return { ...c, body: editBody, updated_at: now };
              }
              // Also check replies
              if (c.replies) {
                const updatedReplies = c.replies.map((r) =>
                  r.id === commentId
                    ? { ...r, body: editBody, updated_at: now }
                    : r
                );
                return { ...c, replies: updatedReplies };
              }
              return c;
            })
          );
        },
        onError: (error: any) => {
          toast.error(error?.message || 'Failed to update comment');
        },
      }
    );
  }

  return (
    <div className="relative">
      {/* Comments Header */}
      <div className="flex justify-between items-center mb-6">
        <Text
          variant="h4"
          size="lg"
          bold={false}
          className="font-semibold dark:text-custom-white"
        >
          Comments ({commentsCount})
        </Text>
      </div>

      {/* Mention Suggestions Dropdown */}
      {showSuggestions && suggestions.length > 0 && (
        <div
          className="absolute z-50 bg-white dark:bg-dark-bg border border-gray-200 dark:border-gray-700 rounded-md shadow-lg max-h-48 overflow-y-auto w-64"
          style={{
            // Simple positioning logic - likely needs improvement for robustness
            top: activeCommentId === 'main' ? '80px' : 'auto',
            left: '60px',
          }}
        >
          <ul>
            {suggestions.map((user) => (
              <li
                key={user.username}
                className="px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-800 cursor-pointer flex items-center gap-2"
                onClick={() => insertMention(user.username)}
              >
                <div className="w-6 h-6 rounded-full overflow-hidden">
                  <img
                    src={user.avatar_url || '/assets/icons/profile.jpg'}
                    alt=""
                    className="w-full h-full object-cover"
                  />
                </div>
                <span className="text-sm font-medium dark:text-custom-white">
                  {user.username}
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="dark:text-custom-white">
        {/* New Comment Input */}
        <div className="flex gap-4 my-4 relative">
          <div className="w-8 h-8 rounded-full border p-1 flex-shrink-0">
            <img
              className="w-full h-full dark:invert"
              src="/assets/icons/iconamoon_profile-light.png"
              alt="Profile picture"
            />
          </div>
          <form className="flex-1" onSubmit={handleAddComment}>
            <textarea
              placeholder="Add to discussion"
              value={newComment}
              onFocus={(e) => {
                if (!isAuthenticated) {
                  e.target.blur();
                  openAuthModal(window.location.pathname);
                } else {
                  setActiveCommentId('main');
                }
              }}
              onChange={(e) => handleInputChange(e.target.value)}
              aria-label="Add a comment"
              className="resize-none w-full px-4 py-2 border border-secondary rounded-md focus:outline-none focus:ring-2 focus:ring-primary dark:bg-dark-bg transition-all"
              rows={3}
              disabled={isSubmitting}
            ></textarea>
            <div className="flex justify-end mt-2">
              <Button
                type="submit"
                disabled={
                  !isAuthenticated || isSubmitting || !newComment.trim()
                }
                className="disabled:cursor-not-allowed disabled:opacity-50"
              >
                {isSubmitting ? <Spinner /> : 'Post Comment'}
              </Button>
            </div>
          </form>
        </div>

        {/* Existing Comments List */}
        <ul className="space-y-6">
          {comments.map((comment) => (
            <li
              className="border-t border-gray-100 dark:border-gray-800 pt-6 transition-colors duration-500"
              key={comment.id}
              id={`comment-${comment.id}`}
            >
              <div className="flex gap-4">
                <div className="w-8 h-8 flex-shrink-0">
                  <img
                    className="h-full w-full rounded-full object-cover"
                    src={comment.user_avatar || '/assets/icons/profile.jpg'}
                    alt={`${comment.user_name}'s avatar`}
                  />
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <div className="flex items-center gap-1.5">
                      {isAuthenticated &&
                        user?.username === comment.user_username && (
                          <span className="text-xs font-semibold text-primary bg-primary/10 px-1.5 py-0.5 rounded">
                            You
                          </span>
                        )}
                      <p className="font-bold text-sm">{comment.user_name}</p>
                    </div>
                    <span className="text-xs text-secondary">
                      {formatDateB(
                        isCommentEdited(comment.created_at, comment.updated_at)
                          ? comment.updated_at!
                          : comment.created_at
                      )}
                    </span>
                    {isCommentEdited(
                      comment.created_at,
                      comment.updated_at
                    ) && (
                      <span className="text-xs text-gray-500 italic">
                        (Edited)
                      </span>
                    )}
                  </div>

                  {editingCommentId === comment.id ? (
                    <div className="mb-3">
                      <textarea
                        value={editBody}
                        onChange={(e) => setEditBody(e.target.value)}
                        className="w-full p-2 border rounded-md dark:bg-dark-bg focus:outline-none focus:ring-2 focus:ring-primary"
                        rows={3}
                      />
                      <div className="flex gap-2 mt-2">
                        <Button
                          size="sm"
                          onClick={() => handleUpdateComment(comment.id)}
                          disabled={isUpdatingComment || !editBody.trim()}
                        >
                          {isUpdatingComment ? <Spinner /> : 'Save'}
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => setEditingCommentId(null)}
                        >
                          Cancel
                        </Button>
                      </div>
                    </div>
                  ) : (
                    <p className="text-sm leading-relaxed mb-3">
                      {renderTextWithMentions(comment.body)}
                    </p>
                  )}

                  <div className="flex gap-6 items-center">
                    <Like commentId={comment.id} />
                    <button
                      onClick={() => {
                        if (!isAuthenticated) {
                          openAuthModal(window.location.pathname);
                          return;
                        }

                        const isCurrentlyOpen =
                          replyText[comment.id] !== undefined;

                        if (!isCurrentlyOpen) {
                          setReplyText((prev) => ({
                            ...prev,
                            [comment.id]: `@${comment.user_username} `,
                          }));
                          setActiveCommentId(comment.id);
                        } else {
                          setReplyText((prev) => {
                            const newState = { ...prev };
                            delete newState[comment.id];
                            return newState;
                          });
                          if (activeCommentId === comment.id) {
                            setActiveCommentId(null);
                          }
                        }
                      }}
                      className="text-xs text-secondary hover:text-primary transition-colors flex items-center gap-1"
                      aria-label={`Reply to ${comment.user_name}'s comment`}
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        strokeWidth={1.5}
                        stroke="currentColor"
                        className="size-4"
                        aria-hidden="true"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 0 1-.923 1.785A5.969 5.969 0 0 0 6 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337Z"
                        />
                      </svg>
                      Reply
                    </button>
                    {isAuthenticated &&
                      user?.username === comment.user_username && (
                        <button
                          onClick={() =>
                            handleEditClick(comment.id, comment.body)
                          }
                          className="text-xs text-secondary hover:text-primary transition-colors flex items-center gap-1"
                        >
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                            strokeWidth={1.5}
                            stroke="currentColor"
                            className="size-4"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10"
                            />
                          </svg>
                          Edit
                        </button>
                      )}
                  </div>

                  {/* Reply Input Box */}
                  {replyText[comment.id] !== undefined && (
                    <form
                      className="mt-4 animate-in fade-in slide-in-from-top-2 duration-200 relative"
                      onSubmit={(e) => {
                        e.preventDefault();
                        handleAddReply(comment.id, comment.thread_id);
                      }}
                    >
                      <textarea
                        placeholder={`Reply to ${comment.user_name}...`}
                        value={replyText[comment.id]}
                        onChange={(e) =>
                          handleInputChange(e.target.value, comment.id)
                        }
                        onFocus={() => setActiveCommentId(comment.id)}
                        autoFocus
                        aria-label={`Reply form for ${comment.user_name}'s comment`}
                        className="resize-none w-full px-4 py-2 border border-secondary rounded-md focus:outline-none focus:ring-2 focus:ring-primary dark:bg-dark-bg"
                        rows={2}
                        disabled={isSubmitting}
                      ></textarea>
                      <div className="flex gap-2 mt-2">
                        <Button
                          type="submit"
                          size="sm"
                          disabled={
                            isSubmitting || !replyText[comment.id].trim()
                          }
                        >
                          {isSubmitting ? 'Posting... ' : 'Post Reply'}
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() =>
                            setReplyText((prev) => {
                              const newState = { ...prev };
                              delete newState[comment.id];
                              return newState;
                            })
                          }
                        >
                          Cancel
                        </Button>
                      </div>
                    </form>
                  )}

                  {/* View Replies Button */}
                  {comment.total_replies > 0 &&
                    (!comment.replies || comment.replies.length === 0) && (
                      <button
                        onClick={() => handleViewReplies(comment.id)}
                        disabled={loadingReplies[comment.id]}
                        className="mt-2 text-xs font-semibold text-primary dark:text-blue-400 hover:underline flex items-center gap-2"
                      >
                        {loadingReplies[comment.id] ? (
                          <Spinner />
                        ) : (
                          <div className="flex items-center gap-2">
                            <div className="w-8 border-t border-gray-300 dark:border-gray-600"></div>
                            <span>
                              View {comment.total_replies}{' '}
                              {comment.total_replies === 1
                                ? 'reply'
                                : 'replies'}
                            </span>
                          </div>
                        )}
                      </button>
                    )}

                  {/* Nested Replies */}
                  {comment.replies && comment.replies.length > 0 && (
                    <ul className="mt-4 space-y-4 border-l-2 border-gray-100 dark:border-gray-800 pl-4">
                      {comment.replies.map((reply) => (
                        <li
                          key={reply.id}
                          id={`comment-${reply.id}`}
                          className="flex gap-3 transition-colors duration-500"
                        >
                          <div className="w-6 h-6 flex-shrink-0">
                            <img
                              className="h-full w-full rounded-full object-cover"
                              src={
                                reply.user_avatar || '/assets/icons/profile.jpg'
                              }
                              alt={`${reply.user_name}'s avatar`}
                            />
                          </div>
                          <div>
                            <div className="flex items-center gap-2 mb-1">
                              <div className="flex items-center gap-1">
                                {isAuthenticated &&
                                  user?.username === reply.user_username && (
                                    <span className="text-[10px] font-semibold text-primary bg-primary/10 px-1 py-0.5 rounded">
                                      You
                                    </span>
                                  )}
                                <p className="font-bold text-xs">
                                  {reply.user_name}
                                </p>
                              </div>
                              <span className="text-[10px] text-secondary">
                                {formatDateB(
                                  isCommentEdited(
                                    reply.created_at,
                                    reply.updated_at
                                  )
                                    ? reply.updated_at!
                                    : reply.created_at
                                )}
                              </span>
                              {isCommentEdited(
                                reply.created_at,
                                reply.updated_at
                              ) && (
                                <span className="text-[10px] text-gray-500 italic">
                                  (Edited)
                                </span>
                              )}
                            </div>
                            {editingCommentId === reply.id ? (
                              <div className="mb-2">
                                <textarea
                                  value={editBody}
                                  onChange={(e) => setEditBody(e.target.value)}
                                  className="w-full p-2 border rounded-md dark:bg-dark-bg focus:outline-none focus:ring-2 focus:ring-primary text-xs"
                                  rows={2}
                                />
                                <div className="flex gap-2 mt-2">
                                  <Button
                                    size="sm"
                                    onClick={() =>
                                      handleUpdateComment(reply.id)
                                    }
                                    disabled={
                                      isUpdatingComment || !editBody.trim()
                                    }
                                  >
                                    {isUpdatingComment ? 'Updating...' : 'Save'}
                                  </Button>
                                  <Button
                                    variant="outline"
                                    size="sm"
                                    onClick={() => setEditingCommentId(null)}
                                  >
                                    Cancel
                                  </Button>
                                </div>
                              </div>
                            ) : (
                              <p className="text-xs leading-relaxed">
                                {renderTextWithMentions(reply.body)}
                              </p>
                            )}

                            <div className="flex gap-4 items-center mt-1">
                              <Like commentId={reply.id} />
                              {isAuthenticated &&
                                user?.username === reply.user_username &&
                                editingCommentId !== reply.id && (
                                  <button
                                    onClick={() =>
                                      handleEditClick(reply.id, reply.body)
                                    }
                                    className="text-[10px] text-secondary hover:text-primary transition-colors flex items-center gap-1"
                                  >
                                    <svg
                                      xmlns="http://www.w3.org/2000/svg"
                                      fill="none"
                                      viewBox="0 0 24 24"
                                      strokeWidth={1.5}
                                      stroke="currentColor"
                                      className="size-3"
                                    >
                                      <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10"
                                      />
                                    </svg>
                                    Edit
                                  </button>
                                )}
                            </div>
                          </div>
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default DiscussionThread;
