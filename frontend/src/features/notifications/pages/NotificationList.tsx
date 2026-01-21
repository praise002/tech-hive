import {
  useDeleteNotification,
  useMarkNotificationAsRead,
  useNotifications,
  useRestoreNotification,
} from '../../../hooks/useNotification';
import { formatDateB } from '../../../utils/utils';
import Text from '../../../components/common/Text';
import Spinner from '../../../components/common/Spinner';
import Button from '../../../components/common/Button';
import { MdDelete } from 'react-icons/md';
import { Notification } from '../../../types/types';

import { toast } from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';

function NotificationList() {
  const [currentPage, setCurrentPage] = useState(1);
  const [notificationToMarkAsRead, setNotificationToMarkAsRead] =
    useState<string>('');
  const pageSize = 10;

  const { notifications, count, next, previous, isPending, isError } =
    useNotifications({
      page: currentPage.toString(),
      page_size: pageSize.toString(),
    });

  const { deleteNotification } = useDeleteNotification();
  const { restoreNotification } = useRestoreNotification();

  // This hook will automatically mark the notification as read when notificationToMarkAsRead changes
  useMarkNotificationAsRead(notificationToMarkAsRead);

  const navigate = useNavigate();

  const totalPages = count ? Math.ceil(count / pageSize) : 0;

  const handleDelete = (id: string) => {
    deleteNotification(id, {
      onSuccess: () => {
        toast.success(
          (t) => (
            <div className="flex items-center gap-2">
              <span>Notification deleted</span>
              <button
                onClick={() => {
                  restoreNotification(id);
                  toast.dismiss(t.id);
                }}
                className="px-2 py-1 text-xs font-semibold text-white bg-blue-600 rounded hover:bg-blue-700"
              >
                Undo
              </button>
            </div>
          ),
          { duration: 4000 }
        );
      },
      onError: () => {
        toast.error('Failed to delete notification');
      },
    });
  };

  if (isPending) {
    return (
      <div className="flex justify-center items-center min-h-[50vh]">
        <Spinner />
      </div>
    );
  }

  if (isError) {
    return (
      <div className="text-center py-10 text-red-600">
        Error loading notifications.
      </div>
    );
  }

  const handleNotificationClick = (notification: Notification) => {
    // Mark notification as read by triggering the hook
    if (!notification.is_read) {
      setNotificationToMarkAsRead(notification.id);
    }

    const {
      target_content_type,
      target_slug,
      target_username,
      target_object_id,
    } = notification;

    // Navigate based on content type
    if (target_content_type === 'article' && target_slug && target_username) {
      // For article notifications (like article likes), just go to the article page
      const articleUrl = `/articles/${target_username}/${target_slug}`;
      navigate(articleUrl);
    } else if (
      target_content_type === 'comment' &&
      target_slug &&
      target_username
    ) {
      // For comment notifications, navigate to the specific comment
      const articleUrl = `/articles/${target_username}/${target_slug}`;
      const fullUrl = target_object_id
        ? `${articleUrl}#comment-${target_object_id}`
        : articleUrl;
      navigate(fullUrl);
    } else if (target_content_type === 'job' && target_object_id) {
      navigate(`/jobs/${target_object_id}`);
    } else if (target_content_type === 'event' && target_object_id) {
      navigate(`/events/${target_object_id}`);
    } else if (target_content_type === 'resource' && target_object_id) {
      navigate(`/resources/${target_object_id}`);
    } else if (target_content_type === 'tool' && target_object_id) {
      navigate(`/tools/${target_object_id}`);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 mt-20">
      {notifications.length === 0 ? (
        <div className="text-center py-10 text-gray-500 dark:text-gray-400">
          You have no notifications.
        </div>
      ) : (
        <>
          <Text
            variant="h2"
            className="mb-6 font-bold text-gray-900 dark:text-white"
          >
            Notifications
          </Text>
          <div className="space-y-4">
            {notifications.map((notification: Notification) => (
              <div
                key={notification.id}
                className={`p-4 rounded-lg border ${
                  notification.is_read === false
                    ? 'bg-blue-50 border-blue-200 dark:bg-blue-900/20 dark:border-blue-800'
                    : 'bg-white border-gray-200 dark:bg-dark dark:border-gray-700'
                } flex justify-between items-start gap-4 transition-colors`}
              >
                <div
                  className="flex-1 cursor-pointer"
                  onClick={() => handleNotificationClick(notification)}
                >
                  <div className="flex items-center gap-2 mb-1">
                    {notification.actor_avatar && (
                      <img
                        src={notification.actor_avatar}
                        alt={notification.actor_name}
                        className="w-6 h-6 rounded-full object-cover"
                      />
                    )}
                    <span className="text-sm font-semibold text-gray-800 dark:text-gray-200">
                      {notification.actor_name}
                    </span>
                    <span className="text-xs text-gray-500 dark:text-gray-400">
                      {formatDateB(notification.created_at)}
                    </span>
                  </div>
                  <p className="text-gray-700 dark:text-gray-300">
                    {notification.description}
                  </p>
                </div>

                <div className="flex flex-col gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    className="!p-2 text-red-600 hover:text-red-700 border-red-200 hover:border-red-300"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDelete(notification.id);
                    }}
                    aria-label="Delete notification"
                  >
                    <MdDelete className="w-5 h-5" />
                  </Button>
                </div>
              </div>
            ))}
          </div>

          {/* Pagination */}
          {count > pageSize && (
            <div className="mt-8 flex items-center justify-center">
              <div className="flex items-center space-x-2">
                <Button
                  variant="primary"
                  aria-label="Go to previous page"
                  disabled={!previous}
                  onClick={() => setCurrentPage((p) => p - 1)}
                >
                  Previous
                </Button>

                <span
                  className="text-gray-600 dark:text-gray-400"
                  aria-live="polite"
                >
                  Page {currentPage} of {totalPages}
                </span>

                <Button
                  variant="primary"
                  aria-label="Go to next page"
                  disabled={!next}
                  onClick={() => setCurrentPage((p) => p + 1)}
                >
                  Next
                </Button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default NotificationList;
