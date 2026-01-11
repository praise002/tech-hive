from apps.accounts.utils import UserRoles
from apps.analytics.choices import EventTypeChoices
from apps.analytics.models import SessionMetrics, UserActivity
from apps.analytics.tests.utils import AnalyticsTestHelper
from apps.common.utils import TestUtil
from apps.content.models import Article
from django.core.cache import cache
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase


class TestDashboardMetricsView(APITestCase):
    url = "/api/v1/analytics/dashboard/"

    def setUp(self):
        self.admin_user = TestUtil.verified_user()
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True
        self.admin_user.save()

        self.regular_user = TestUtil.other_verified_user()

        # Clear cache before each test
        cache.clear()

    def test_unauthenticated_access_denied(self):
        """Test unauthenticated users cannot access dashboard metrics"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_admin_access_denied(self):
        """Test regular users cannot access dashboard metrics"""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_access_allowed(self):
        """Test admin users can access dashboard metrics"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)

    def test_default_period_is_weekly(self):
        """Test defaults to weekly period when not specified"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["period"], "weekly")

    def test_weekly_period_parameter(self):
        """Test with explicit weekly period parameter"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url, {"period": "weekly"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["period"], "weekly")

    def test_monthly_period_parameter(self):
        """Test with monthly period parameter"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url, {"period": "monthly"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["period"], "monthly")

    def test_invalid_period_parameter(self):
        """Test invalid period returns 400 error"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url, {"period": "yearly"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid period", response.data["message"])

    def test_response_structure(self):
        """Test response contains all required fields"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url)

        data = response.data["data"]

        # Check top-level structure
        self.assertIn("period", data)
        self.assertIn("date_range", data)
        self.assertIn("metrics", data)
        self.assertIn("device_types", data)
        self.assertIn("active_users", data)
        self.assertIn("top_performing_posts", data)
        self.assertIn("cached", data)

        # Check metrics structure
        self.assertIn("time_on_page", data["metrics"])
        self.assertIn("bounce_rate", data["metrics"])
        self.assertIn("load_speed", data["metrics"])

    def test_caching_first_request(self):
        """Test first request is not cached"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url, {"period": "weekly"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["cached"], False)

    def test_caching_subsequent_request(self):
        """Test subsequent requests are cached"""
        self.client.force_authenticate(user=self.admin_user)

        # First request
        response1 = self.client.get(self.url, {"period": "weekly"})
        self.assertEqual(response1.data["data"]["cached"], False)

        # Second request (should be cached)
        response2 = self.client.get(self.url, {"period": "weekly"})
        self.assertEqual(response2.data["data"]["cached"], True)

    def test_cache_different_for_different_periods(self):
        """Test cache is separate for different periods"""
        self.client.force_authenticate(user=self.admin_user)

        # Request weekly
        response1 = self.client.get(self.url, {"period": "weekly"})
        self.assertEqual(response1.data["data"]["cached"], False)

        # Request monthly (should not be cached)
        response2 = self.client.get(self.url, {"period": "monthly"})
        self.assertEqual(response2.data["data"]["cached"], False)


class TestTrackActivityView(APITestCase):
    url = "/api/v1/analytics/track/"

    def setUp(self):
        self.user = TestUtil.verified_user()

    def test_unauthenticated_tracking_allowed(self):
        """Test anonymous users can track activity"""
        payload = {
            "event_type": EventTypeChoices.PAGE_VIEW,
            "session_id": "anonymous-session-123",
            "page_url": "https://techhive.com/articles/test/",
            "device_type": "Mobile",
            "metadata": {"content_type": "article", "content_id": "article-uuid"},
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("activity_id", response.data["data"])

    def test_authenticated_tracking(self):
        """Test authenticated users can track activity"""
        self.client.force_authenticate(user=self.user)

        payload = {
            "event_type": EventTypeChoices.PAGE_VIEW,
            "session_id": "auth-session-456",
            "page_url": "https://techhive.com/articles/test/",
            "device_type": "Desktop",
            "metadata": {"content_type": "article", "content_id": "article-uuid"},
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify user is associated
        activity_id = response.data["data"]["activity_id"]
        activity = UserActivity.objects.get(id=activity_id)
        self.assertEqual(activity.user, self.user)

    def test_creates_session_metrics(self):
        """Test creates SessionMetrics on first activity"""
        payload = {
            "event_type": EventTypeChoices.PAGE_VIEW,
            "session_id": "new-session-789",
            "page_url": "https://techhive.com/test/",
            "device_type": "Tablet",
            "metadata": {"content_type": "article", "content_id": "article-uuid"},
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify session was created
        session = SessionMetrics.objects.get(session_id="new-session-789")
        self.assertIsNotNone(session)
        self.assertEqual(session.device_type, "Tablet")

    def test_reuses_existing_session(self):
        """Test reuses existing session for subsequent activities"""
        session_id = "existing-session-123"

        # First activity
        payload1 = {
            "event_type": EventTypeChoices.PAGE_VIEW,
            "session_id": session_id,
            "page_url": "https://techhive.com/page1/",
            "device_type": "Desktop",
            "metadata": {"content_type": "article", "content_id": "article-uuid"},
        }
        _ = self.client.post(self.url, payload1, format="json")

        # Second activity with same session_id
        payload2 = {
            "event_type": EventTypeChoices.PAGE_VIEW,
            "session_id": session_id,
            "page_url": "https://techhive.com/page2/",
            "device_type": "Desktop",
        }
        _ = self.client.post(self.url, payload2, format="json")

        # Should only have one session
        sessions = SessionMetrics.objects.filter(session_id=session_id)
        self.assertEqual(sessions.count(), 1)

    def test_anonymous_to_authenticated_transition(self):
        """Test session user is updated when anonymous user logs in"""
        session_id = "transition-session-123"

        # Anonymous activity
        payload1 = {
            "event_type": EventTypeChoices.PAGE_VIEW,
            "session_id": session_id,
            "page_url": "https://techhive.com/page1/",
            "device_type": "Mobile",
            "metadata": {"content_type": "article", "content_id": "article-uuid"},
        }
        _ = self.client.post(self.url, payload1, format="json")

        session = SessionMetrics.objects.get(session_id=session_id)
        self.assertIsNone(session.user)

        # Authenticated activity with same session
        self.client.force_authenticate(user=self.user)
        payload2 = {
            "event_type": EventTypeChoices.PAGE_VIEW,
            "session_id": session_id,
            "page_url": "https://techhive.com/page2/",
            "device_type": "Mobile",
            "metadata": {"content_type": "article", "content_id": "article-uuid"},
        }
        _ = self.client.post(self.url, payload2, format="json")

        # Session user should now be set
        session.refresh_from_db()
        self.assertEqual(session.user, self.user)

    def test_page_count_increment(self):
        """Test page_count increments with each activity"""
        session_id = "count-session-123"

        payload = {
            "event_type": EventTypeChoices.PAGE_VIEW,
            "session_id": session_id,
            "page_url": "https://techhive.com/test/",
            "device_type": "Desktop",
            "metadata": {"content_type": "article", "content_id": "article-uuid"},
        }

        # First activity
        self.client.post(self.url, payload, format="json")
        session = SessionMetrics.objects.get(session_id=session_id)
        self.assertEqual(session.page_count, 1)
        self.assertEqual(session.is_bounce, True)

        # Second activity
        self.client.post(self.url, payload, format="json")
        session.refresh_from_db()
        self.assertEqual(session.page_count, 2)
        self.assertEqual(session.is_bounce, False)

    def test_missing_required_fields(self):
        """Test validation error when required fields are missing"""
        # Missing event_type
        payload = {
            "session_id": "test-session",
            "page_url": "https://techhive.com/test/",
            "metadata": {"content_type": "article", "content_id": "article-uuid"},
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_optional_fields_stored(self):
        """Test optional fields are stored when provided"""
        payload = {
            "event_type": EventTypeChoices.PAGE_VIEW,
            "session_id": "optional-fields-session",
            "page_url": "https://techhive.com/test/",
            "device_type": "Desktop",
            "browser": "Chrome",
            "browser_version": "120.0",
            "os": "Windows",
            "os_version": "11",
            "duration_seconds": 180,
            "referrer": "https://google.com/search",
            "metadata": {"content_type": "article", "content_id": "123"},
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        activity_id = response.data["data"]["activity_id"]
        activity = UserActivity.objects.get(id=activity_id)

        self.assertEqual(activity.browser, "Chrome")
        self.assertEqual(activity.os, "Windows")
        self.assertEqual(activity.duration_seconds, 180)
        self.assertEqual(activity.referrer, "https://google.com/search")
        self.assertEqual(activity.metadata["content_type"], "article")

    def test_page_load_event_with_load_time(self):
        """Test PAGE_LOAD event stores load time"""
        payload = {
            "event_type": EventTypeChoices.PAGE_LOAD,
            "session_id": "load-time-session",
            "page_url": "https://techhive.com/test/",
            "load_time_ms": 2500,
            "device_type": "Desktop",
            "metadata": {"content_type": "article", "content_id": "123"},
        }

        response = self.client.post(self.url, payload, format="json")

        activity_id = response.data["data"]["activity_id"]
        activity = UserActivity.objects.get(id=activity_id)

        self.assertEqual(activity.event_type, EventTypeChoices.PAGE_LOAD)
        self.assertEqual(activity.load_time_ms, 2500)


class TestArticlePerformanceView(APITestCase):
    url_template = "/api/v1/analytics/articles/{}/"

    def setUp(self):
        from django.contrib.auth.models import Group

        contributor_group, _ = Group.objects.get_or_create(name=UserRoles.CONTRIBUTOR)

        self.author = TestUtil.verified_user()
        self.author.groups.add(contributor_group)

        self.other_user = TestUtil.other_verified_user()
        self.admin_user = TestUtil.another_verified_user()
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True
        self.admin_user.save()

        self.article = AnalyticsTestHelper.create_article_with_analytics(
            author=self.author, views=10, shares=5, avg_duration=120
        )

        # Clear cache
        cache.clear()

    def test_unauthenticated_access_denied(self):
        """Test unauthenticated users cannot access article analytics"""
        url = self.url_template.format(self.article.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_author_can_view_own_article_analytics(self):
        """Test article author can view their own analytics"""
        self.client.force_authenticate(user=self.author)
        url = self.url_template.format(self.article.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)

    def test_admin_can_view_any_article_analytics(self):
        """Test admin can view any article analytics"""
        self.client.force_authenticate(user=self.admin_user)
        url = self.url_template.format(self.article.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_author_non_admin_denied(self):
        """Test non-author, non-admin users cannot view analytics"""
        self.client.force_authenticate(user=self.other_user)
        url = self.url_template.format(self.article.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_existent_article_returns_404(self):
        """Test returns 404 for non-existent article"""
        self.client.force_authenticate(user=self.admin_user)
        url = self.url_template.format("00000000-0000-0000-0000-000000000000")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_response_structure(self):
        """Test response contains all required analytics fields"""
        self.client.force_authenticate(user=self.author)
        url = self.url_template.format(self.article.id)
        response = self.client.get(url)

        data = response.data["data"]

        self.assertIn("article_id", data)
        self.assertIn("title", data)
        self.assertIn("total_views", data)
        self.assertIn("unique_visitors", data)
        self.assertIn("total_shares", data)
        self.assertIn("avg_time_on_page", data)
        self.assertIn("bounce_rate", data)
        self.assertIn("period", data)
        self.assertIn("date_range", data)

    def test_metrics_calculation(self):
        """Test metrics are calculated correctly"""
        self.client.force_authenticate(user=self.author)
        url = self.url_template.format(self.article.id)
        response = self.client.get(url)

        data = response.data["data"]

        # Article was created with 10 views and 5 shares
        self.assertEqual(data["total_views"], 10)
        self.assertEqual(data["total_shares"], 5)
        self.assertGreater(data["unique_visitors"], 0)

    def test_avg_time_on_page_in_minutes(self):
        """Test avg_time_on_page is returned in minutes"""
        self.client.force_authenticate(user=self.author)
        url = self.url_template.format(self.article.id)
        response = self.client.get(url)

        data = response.data["data"]

        # avg_time_on_page should be a decimal number (minutes)
        self.assertIsInstance(data["avg_time_on_page"], float)

    def test_bounce_rate_calculation(self):
        """Test bounce rate is calculated as percentage"""
        self.client.force_authenticate(user=self.author)
        url = self.url_template.format(self.article.id)
        response = self.client.get(url)

        data = response.data["data"]

        # Bounce rate should be a number between 0 and 100
        self.assertGreaterEqual(data["bounce_rate"], 0)
        self.assertLessEqual(data["bounce_rate"], 100)


# class TestDashboardExportView(APITestCase):
#     url = "/api/v1/analytics/dashboard/export/"

#     def setUp(self):
#         self.admin_user = TestUtil.verified_user()
#         self.admin_user.is_staff = True
#         self.admin_user.is_superuser = True
#         self.admin_user.save()

#         self.regular_user = TestUtil.other_verified_user()

#     def test_unauthenticated_access_denied(self):
#         """Test unauthenticated users cannot export"""
#         response = self.client.get(self.url)

#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_non_admin_access_denied(self):
#         """Test regular users cannot export"""
#         self.client.force_authenticate(user=self.regular_user)
#         response = self.client.get(self.url)

#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# # TODO:
#     def test_admin_can_export_csv(self):
#         """Test admin can export dashboard metrics as CSV"""
#         self.client.force_authenticate(user=self.admin_user)
#         response = self.client.get(self.url, {"format": "csv"})
#         print(response)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response["Content-Type"], "text/csv")
#         self.assertIn("Content-Disposition", response)

#     def test_admin_can_export_excel(self):
#         """Test admin can export dashboard metrics as Excel"""
#         self.client.force_authenticate(user=self.admin_user)
#         response = self.client.get(self.url, {"format": "excel"})

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn("application/vnd.openxmlformats", response["Content-Type"])

#     def test_default_format_is_csv(self):
#         """Test defaults to CSV format"""
#         self.client.force_authenticate(user=self.admin_user)
#         response = self.client.get(self.url)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response["Content-Type"], "text/csv")

#     def test_invalid_format_returns_400(self):
#         """Test invalid format parameter returns error"""
#         self.client.force_authenticate(user=self.admin_user)
#         response = self.client.get(self.url, {"format": "pdf"})

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_invalid_period_returns_400(self):
#         """Test invalid period parameter returns error"""
#         self.client.force_authenticate(user=self.admin_user)
#         response = self.client.get(self.url, {"period": "yearly", "format": "csv"})

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# python manage.py test apps.analytics.tests.test_views.TestDashboardMetricsView
# python manage.py test apps.analytics.tests.test_views.TestTrackActivityView
# python manage.py test apps.analytics.tests.test_views.TestArticlePerformanceView
# python manage.py test apps.analytics.tests.test_views.TestDashboardExportView
