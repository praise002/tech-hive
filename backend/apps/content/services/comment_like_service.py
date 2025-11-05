import json
import logging
from typing import Dict, List, Optional, Set

import redis
from django.conf import settings

logger = logging.getLogger(__name__)


class CommentLikeService:
    """
    Service class to handle comment like operations using Redis.

    Redis Data Structure:
    - Key: comment:likes:{comment_id}
    - Type: SET
    - Members: user_ids who liked the comment
    """

    def __init__(self):
        """Initialize Redis connection with connection pooling."""
        try:
            self.pool = redis.ConnectionPool(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                **settings.REDIS_CONNECTION_POOL,
            )
            self.redis_client = redis.Redis(connection_pool=self.pool)

            # Test connection
            self.redis_client.ping()
            logger.info("Redis connection established successfully")

        except redis.ConnectionError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error connecting to Redis: {e}")
            raise

    def _get_key(self, comment_id: int) -> str:
        """
        Generate Redis key for a comment's likes.

        Args:
            comment_id: ID of the comment

        Returns:
            Redis key string (e.g., "comment:likes:123")
        """
        return f"comment:likes:{comment_id}"

    def toggle_like(self, comment_id: int, user_id: int) -> Dict[str, any]:
        """
        Toggle like status for a comment.
        If user already liked, it unlikes. If not liked, it likes.

        Args:
            comment_id: ID of the comment
            user_id: ID of the user

        Returns:
            Dictionary with:
            - is_liked: bool (current like status)
            - like_count: int (total likes)
            - action: str ('liked' or 'unliked')
        """
        try:
            redis_key = self._get_key(comment_id)

            # Check if user already liked this comment
            is_currently_liked = self.redis_client.sismember(redis_key, user_id)

            if is_currently_liked:
                # Unlike: Remove user from set
                self.redis_client.srem(redis_key, user_id)
                action = "unliked"
                is_liked = False
                logger.info(f"User {user_id} unliked comment {comment_id}")
            else:
                # Like: Add user to set
                self.redis_client.sadd(redis_key, user_id)
                action = "liked"
                is_liked = True
                logger.info(f"User {user_id} liked comment {comment_id}")

            # Get updated like count
            like_count = self.redis_client.scard(redis_key)

            return {"is_liked": is_liked, "like_count": like_count, "action": action}

        except redis.RedisError as e:
            logger.error(f"Redis error in toggle_like: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in toggle_like: {e}")
            raise

    def get_like_status(
        self, comment_id: int, user_id: Optional[int] = None
    ) -> Dict[str, any]:
        # filled-in like button for authenticated user
        """
        Get like status for a comment.

        Args:
            comment_id: ID of the comment
            user_id: ID of the user (optional, to check if they liked)

        Returns:
            Dictionary with:
            - like_count: int (total likes)
            - is_liked: bool or None (if user_id provided)
        """
        try:
            redis_key = self._get_key(comment_id)

            # Get total like count
            like_count = self.redis_client.scard(redis_key)

            # Check if specific user liked (if user_id provided)
            is_liked = None
            if user_id is not None:
                is_liked = self.redis_client.sismember(redis_key, user_id)

            return {"like_count": like_count, "is_liked": is_liked}

        except redis.RedisError as e:
            logger.error(f"Redis error in get_like_status: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in get_like_status: {e}")
            raise

    def get_bulk_like_status(
        self, comment_ids: List[int], user_id: Optional[int] = None
    ) -> Dict[int, Dict[str, any]]:
        """
        Get like status for multiple comments efficiently using Redis pipeline.
        This is useful when displaying a list of comments.

        Args:
            comment_ids: List of comment IDs
            user_id: ID of the user (optional)

        Returns:
            Dictionary mapping comment_id to like data:
            {
                123: {'like_count': 5, 'is_liked': True},
                124: {'like_count': 3, 'is_liked': False},
                ...
            }
        """
        try:
            if not comment_ids:
                return {}

            # Use pipeline for batch operations (single round-trip to Redis)
            pipeline = self.redis_client.pipeline()

            # Queue all operations
            for comment_id in comment_ids:
                redis_key = self._get_key(comment_id)
                pipeline.scard(redis_key)  # Get like count

                if user_id is not None:
                    pipeline.sismember(redis_key, user_id)  # Check if user liked

            # Execute all operations at once
            responses = pipeline.execute()

            # Parse responses
            results = {}
            response_index = 0
            for comment_id in comment_ids:
                like_count = responses[response_index]
                response_index += 1

                is_liked = None
                if user_id is not None:
                    is_liked = responses[response_index]
                    response_index += 1

                results[comment_id] = {"like_count": like_count, "is_liked": is_liked}

            return results

        except redis.RedisError as e:
            logger.error(f"Redis error in get_bulk_like_status: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in get_bulk_like_status: {e}")
            raise

    def get_users_who_liked(self, comment_id: int) -> Set[int]:
        """
        Get all user IDs who liked a comment.

        Args:
            comment_id: ID of the comment

        Returns:
            Set of user IDs
        """
        try:
            redis_key = self._get_key(comment_id)
            user_ids = self.redis_client.smembers(redis_key)

            # Convert string IDs to integers
            return {int(user_id) for user_id in user_ids}

        except redis.RedisError as e:
            logger.error(f"Redis error in get_users_who_liked: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in get_users_who_liked: {e}")
            raise

    def remove_all_likes(self, comment_id: int) -> int:
        """
        Remove all likes from a comment (useful when comment is deleted).

        Args:
            comment_id: ID of the comment

        Returns:
            Number of likes removed
        """
        try:
            redis_key = self._get_key(comment_id)
            like_count = self.redis_client.scard(redis_key)
            self.redis_client.delete(redis_key)

            logger.info(f"Removed {like_count} likes from comment {comment_id}")
            return like_count

        except redis.RedisError as e:
            logger.error(f"Redis error in remove_all_likes: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in remove_all_likes: {e}")
            raise

    def health_check(self) -> bool:
        """
        Check if Redis connection is healthy.

        Returns:
            True if connection is healthy, False otherwise
        """
        try:
            self.redis_client.ping()
            return True
        except:
            return False


# Singleton instance
comment_like_service = CommentLikeService()
