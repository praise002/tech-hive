from datetime import timedelta

from apps.accounts.models import User
from apps.analytics.choices import DeviceTypeChoices, EventTypeChoices
from apps.analytics.models import SessionMetrics, UserActivity
from apps.common.utils import TestUtil
from apps.content.models import Article, Category, Event, Job
from django.utils import timezone


class AnalyticsTestHelper:
    """
    Helper class for creating analytics test data
    """

    @staticmethod
    def create_session_metrics(user=None, **kwargs):
        """
        Create a SessionMetrics instance with sensible defaults

        Args:
            user: User instance (optional, defaults to None for anonymous)
            **kwargs: Override any field values

        Returns:
            SessionMetrics instance
        """
        defaults = {
            "session_id": f"session-{timezone.now().timestamp()}",
            "user": user,
            # "device_type": random.choice([DeviceTypeChoices.DESKTOP, DeviceTypeChoices.MOBILE, DeviceTypeChoices.TABLET]),
            "device_type": DeviceTypeChoices.DESKTOP,
            "start_time": timezone.now(),
            "page_count": 0,
            "total_duration": 0,
            "is_bounce": False,
        }
        defaults.update(kwargs)
        return SessionMetrics.objects.create(**defaults)

    @staticmethod
    def create_user_activity(session=None, user=None, **kwargs):
        """
        Create a UserActivity instance with sensible defaults

        Args:
            session: SessionMetrics instance (optional)
            user: User instance (optional)
            **kwargs: Override any field values

        Returns:
            UserActivity instance
        """
        defaults = {
            "session": session,
            "user": user,
            "event_type": EventTypeChoices.PAGE_VIEW,
            "page_url": "https://techhive.com/test-page/",
            "device_type": DeviceTypeChoices.DESKTOP,
            "browser": "Chrome",
            "browser_version": "120.0",
            "os": "Windows",
            "os_version": "11",
            "duration_seconds": 60,
            "metadata": {},
        }
        defaults.update(kwargs)

        return UserActivity.objects.create(**defaults)

    @staticmethod
    def create_article_with_analytics(
        author=None, views=10, shares=5, avg_duration=120
    ):
        """
        Create an Article with associated analytics activities

        Args:
            author: User instance (creates one if not provided)
            views: Number of page view activities to create
            shares: Number of share activities to create
            avg_duration: Average duration in seconds for views

        Returns:
            Article instance with analytics data
        """
        if not author:
            try:
                author = User.objects.get(email="testverifieduser@example.com")
            except User.DoesNotExist:
                author = TestUtil.verified_user()

        category, _ = Category.objects.get_or_create(
            name="Technology", defaults={"desc": "Tech articles"}
        )

        article = Article.objects.create(
            title=f"Test Article {timezone.now().timestamp()}",
            content="<p>Test content for analytics</p>",
            author=author,
            category=category,
            status="published",
            published_at=timezone.now(),
        )

        # Create page view activities
        for i in range(views):
            session = AnalyticsTestHelper.create_session_metrics(
                user=author if i % 2 == 0 else None,
            )
            AnalyticsTestHelper.create_user_activity(
                session=session,
                user=(
                    author if i % 2 == 0 else None
                ),  # Mix of authenticated and anonymous
                event_type=EventTypeChoices.PAGE_VIEW,
                page_url=f"https://techhive.com/articles/{article.slug}/",
                duration_seconds=avg_duration + (i * 10),  # Vary duration
                metadata={
                    "content_type": "article",
                    "content_id": str(article.id),
                },
            )

        # Create share activities
        for i in range(shares):
            session = AnalyticsTestHelper.create_session_metrics(
                user=author if i % 2 == 0 else None,
            )
            AnalyticsTestHelper.create_user_activity(
                session=session,
                user=author if i % 2 == 0 else None,
                event_type=EventTypeChoices.SHARE,
                page_url=f"https://techhive.com/articles/{article.slug}/",
                metadata={
                    "content_type": "article",
                    "content_id": str(article.id),
                    "share_platform": "twitter",
                },
            )

        return article

    @staticmethod
    def create_job_with_analytics(views=8, shares=3):
        """
        Create a Job with associated analytics activities

        Args:
            views: Number of page view activities to create
            shares: Number of share activities to create

        Returns:
            Job instance with analytics data
        """
        category, _ = Category.objects.get_or_create(
            name="Engineering", defaults={"desc": "Engineering jobs"}
        )

        job = Job.objects.create(
            title=f"Test Job {timezone.now().timestamp()}",
            company="TechCorp",
            desc="Test job description",
            requirements="Test requirements",
            responsibilities="Test responsibilities",
            url="https://example.com/jobs/test",
            category=category,
            location="Remote",
            job_type="FULL_TIME",
            work_mode="REMOTE",
        )

        user1, _ = User.objects.get_or_create(
            email="testverifieduser@example.com",
            defaults={
                "username": "testuser",
                "password": "Testpassword@123",
                "is_email_verified": True,
            },
        )

        user2, _ = User.objects.get_or_create(
            email="testotheruser@example.com",
            defaults={
                "username": "testotheruser",
                "password": "Testpassword@123",
                "is_email_verified": True,
            },
        )

        # Create page view activities
        for i in range(views):
            session = AnalyticsTestHelper.create_session_metrics(
                user=user2 if i % 2 == 0 else None,
            )
            AnalyticsTestHelper.create_user_activity(
                session=session,
                user=user2 if i % 2 == 0 else None,
                # use  default event_type and other defaults
                page_url=f"https://techhive.com/jobs/{job.id}/",
                metadata={
                    "content_type": "job",
                    "content_id": str(job.id),
                },
            )

        # Create share activities
        for i in range(shares):
            session = AnalyticsTestHelper.create_session_metrics(
                user=user1 if i % 2 == 0 else None,
            )
            AnalyticsTestHelper.create_user_activity(
                session=session,
                user=user1 if i % 2 == 0 else None,
                event_type=EventTypeChoices.SHARE,
                page_url=f"https://techhive.com/jobs/{job.id}/",
                metadata={
                    "content_type": "job",
                    "content_id": str(job.id),
                },
            )

        return job

    @staticmethod
    def create_event_with_analytics(views=6, shares=2):
        """
        Create an Event with associated analytics activities

        Args:
            views: Number of page view activities to create
            shares: Number of share activities to create

        Returns:
            Event instance with analytics data
        """
        category, _ = Category.objects.get_or_create(
            name="Conferences", defaults={"desc": "Tech conferences"}
        )

        event = Event.objects.create(
            title=f"Test Event {timezone.now().timestamp()}",
            desc="Test event description",
            category=category,
            location="Virtual",
            agenda="Test agenda",
            ticket_url="https://example.com/tickets/test",
            start_date=timezone.now() + timedelta(days=7),
            end_date=timezone.now() + timedelta(days=8),
        )

        user, _ = User.objects.get_or_create(
            email="testverifieduser@example.com",
            defaults={
                "username": "testuser",
                "password": "Testpassword@123",
                "is_email_verified": True,
            },
        )

        # Create page view activities
        for i in range(views):
            session = AnalyticsTestHelper.create_session_metrics(
                user=user if i % 2 == 0 else None,
            )
            AnalyticsTestHelper.create_user_activity(
                session=session,
                user=user if i % 2 == 0 else None,
                page_url=f"https://techhive.com/events/{event.id}/",
                metadata={
                    "content_type": "event",
                    "content_id": str(event.id),
                },
            )

        # Create share activities
        for i in range(shares):
            session = AnalyticsTestHelper.create_session_metrics(
                user=user if i % 2 == 0 else None,
            )
            AnalyticsTestHelper.create_user_activity(
                session=session,
                user=user if i % 2 == 0 else None,
                event_type=EventTypeChoices.SHARE,
                page_url=f"https://techhive.com/events/{event.id}/",
                metadata={
                    "content_type": "event",
                    "content_id": str(event.id),
                },
            )

        return event

    @staticmethod
    def create_activities_in_date_range(start_date, end_date, count=5, **kwargs):
        """
        Create multiple UserActivity records spread across a date range

        Args:
            start_date: Start of date range
            end_date: End of date range
            count: Number of activities to create
            **kwargs: Additional fields for activities

        Returns:
            List of UserActivity instances
        """
        activities = []
        delta = (end_date - start_date) / count

        for i in range(count):
            timestamp = start_date + (delta * i)
            session = AnalyticsTestHelper.create_session_metrics(start_time=timestamp)
            activity = AnalyticsTestHelper.create_user_activity(
                session=session, timestamp=timestamp, **kwargs
            )
            activities.append(activity)

        return activities

    @staticmethod
    def create_page_load_activities(count=5, avg_load_time_ms=2000):
        """
        Create PAGE_LOAD activities with load times

        Args:
            count: Number of activities to create
            avg_load_time_ms: Average load time in milliseconds

        Returns:
            List of UserActivity instances
        """
        activities = []
        for i in range(count):
            session = AnalyticsTestHelper.create_session_metrics()
            activity = AnalyticsTestHelper.create_user_activity(
                session=session,
                event_type=EventTypeChoices.PAGE_LOAD,
                load_time_ms=avg_load_time_ms + (i * 100),  # Vary load time
            )
            activities.append(activity)

        return activities

    @staticmethod
    def create_bounce_sessions(count=3):
        """
        Create sessions that bounced (only 1 page view)

        Args:
            count: Number of bounce sessions to create

        Returns:
            List of SessionMetrics instances
        """
        sessions = []
        for _ in range(count):
            session = AnalyticsTestHelper.create_session_metrics(
                page_count=1,
                is_bounce=True,
            )
            # Create the single page view
            AnalyticsTestHelper.create_user_activity(
                session=session,
                event_type=EventTypeChoices.PAGE_VIEW,
            )
            sessions.append(session)

        return sessions

    @staticmethod
    def create_non_bounce_sessions(count=3):
        """
        Create sessions that did NOT bounce (multiple page views)

        Args:
            count: Number of non-bounce sessions to create

        Returns:
            List of SessionMetrics instances
        """
        sessions = []
        for _ in range(count):
            session = AnalyticsTestHelper.create_session_metrics(
                page_count=3,
                is_bounce=False,
            )
            # Create multiple page views
            for _ in range(3):
                AnalyticsTestHelper.create_user_activity(
                    session=session,
                    event_type=EventTypeChoices.PAGE_VIEW,
                )
            sessions.append(session)

        return sessions

    @staticmethod
    def create_device_distribution(mobile=5, desktop=10, tablet=3):
        """
        Create activities with specific device distribution

        Args:
            mobile: Number of mobile activities
            desktop: Number of desktop activities
            tablet: Number of tablet activities

        Returns:
            Dict with counts by device type
        """
        # Create mobile activities
        for _ in range(mobile):
            session = AnalyticsTestHelper.create_session_metrics(
                device_type=DeviceTypeChoices.MOBILE
            )
            AnalyticsTestHelper.create_user_activity(
                session=session,
                device_type=DeviceTypeChoices.MOBILE,
            )

        # Create desktop activities
        for _ in range(desktop):
            session = AnalyticsTestHelper.create_session_metrics(
                device_type=DeviceTypeChoices.DESKTOP
            )
            AnalyticsTestHelper.create_user_activity(
                session=session,
                device_type=DeviceTypeChoices.DESKTOP,
            )

        # Create tablet activities
        for _ in range(tablet):
            session = AnalyticsTestHelper.create_session_metrics(
                device_type=DeviceTypeChoices.TABLET
            )
            AnalyticsTestHelper.create_user_activity(
                session=session,
                device_type=DeviceTypeChoices.TABLET,
            )

        return {
            "mobile": mobile,
            "desktop": desktop,
            "tablet": tablet,
            "total": mobile + desktop + tablet,
        }

    @staticmethod
    def create_daily_active_users(date, registered_count=5, visitor_count=3):
        """
        Create user activities for a specific date

        Args:
            date: Date for the activities
            registered_count: Number of unique registered users
            visitor_count: Number of unique visitor sessions

        Returns:
            Dict with created counts
        """
        # Create activities for registered users
        for i in range(registered_count):
            user = (
                TestUtil.verified_user() if i == 0 else TestUtil.other_verified_user()
            )
            session = AnalyticsTestHelper.create_session_metrics(
                user=user,
                start_time=timezone.make_aware(
                    timezone.datetime.combine(date, timezone.datetime.min.time())
                ),
            )
            AnalyticsTestHelper.create_user_activity(
                session=session,
                user=user,
                timestamp=session.start_time,
            )

        # Create activities for visitors (anonymous)
        for _ in range(visitor_count):
            session = AnalyticsTestHelper.create_session_metrics(
                user=None,
                start_time=timezone.make_aware(
                    timezone.datetime.combine(date, timezone.datetime.min.time())
                ),
            )
            AnalyticsTestHelper.create_user_activity(
                session=session,
                user=None,
                timestamp=session.start_time,
            )

        return {
            "registered": registered_count,
            "visitors": visitor_count,
            "total": registered_count + visitor_count,
        }
