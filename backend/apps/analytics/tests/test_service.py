from datetime import timedelta

from apps.analytics.analytics_service import AnalyticsService
from apps.analytics.choices import DeviceTypeChoices, EventTypeChoices
from apps.analytics.tests.utils import AnalyticsTestHelper
from apps.common.utils import TestUtil
from django.utils import timezone
from rest_framework.test import APITestCase


class TestAnalyticsServiceDateRange(APITestCase):
    """Tests for get_date_range method"""

    def test_weekly_period_calculation(self):
        """Test weekly period returns correct 7-day range"""
        result = AnalyticsService.get_date_range(period="weekly")

        today = timezone.now().date()
        expected_start = today - timedelta(days=6)
        expected_previous_start = expected_start - timedelta(days=6)

        self.assertEqual(result["current_start"], expected_start)
        self.assertEqual(result["current_end"], today)
        self.assertEqual(result["previous_start"], expected_previous_start)
        self.assertEqual(result["previous_end"], expected_start)

    def test_monthly_period_calculation(self):
        """Test monthly period returns correct 30-day range"""
        result = AnalyticsService.get_date_range(period="monthly")

        today = timezone.now().date()
        expected_start = today - timedelta(days=29)
        expected_previous_start = expected_start - timedelta(days=29)

        self.assertEqual(result["current_start"], expected_start)
        self.assertEqual(result["current_end"], today)
        self.assertEqual(result["previous_start"], expected_previous_start)

    def test_default_period_is_weekly(self):
        """Test invalid or missing period defaults to weekly"""
        result_invalid = AnalyticsService.get_date_range(period="invalid")
        result_weekly = AnalyticsService.get_date_range(period="weekly")

        self.assertEqual(
            result_invalid["current_start"], result_weekly["current_start"]
        )
        self.assertEqual(result_invalid["current_end"], result_weekly["current_end"])


class TestAnalyticsServiceMetricTrend(APITestCase):
    """Tests for calculate_metric_with_trend method"""

    def test_upward_trend(self):
        """Test trend calculation when current value is higher"""
        result = AnalyticsService.calculate_metric_with_trend(
            current_value=200, previous_value=50
        )

        self.assertEqual(result["trend"], "up")
        self.assertEqual(result["change_percentage"], 300.0)

    def test_downward_trend(self):
        """Test trend calculation when current value is lower"""
        result = AnalyticsService.calculate_metric_with_trend(
            current_value=80, previous_value=100
        )

        self.assertEqual(result["trend"], "down")
        self.assertEqual(result["change_percentage"], 20.0)

    def test_zero_previous_value(self):
        """Test handling of zero previous value (no division by zero)"""
        result = AnalyticsService.calculate_metric_with_trend(
            current_value=50, previous_value=0
        )

        self.assertEqual(result["change_percentage"], 0)
        self.assertEqual(result["trend"], "up")

    def test_equal_values(self):
        """Test when current and previous values are equal"""
        result = AnalyticsService.calculate_metric_with_trend(
            current_value=100, previous_value=100
        )

        self.assertEqual(result["change_percentage"], 0.0)
        self.assertEqual(result["trend"], "up")


class TestAnalyticsServiceTimeOnPage(APITestCase):
    """Tests for calculate_time_on_page method"""

    def test_time_on_page_with_valid_data(self):
        """Test average time calculation with valid activity data"""
        # Create activities in current period with known durations
        for duration in [60, 120, 180]:  # 1, 2, 3 minutes in seconds
            session = AnalyticsTestHelper.create_session_metrics()
            AnalyticsTestHelper.create_user_activity(
                session=session, duration_seconds=duration
            )

        result = AnalyticsService.calculate_time_on_page(period="weekly")

        # Average: (60 + 120 + 180) / 3 = 120 seconds = 2 minutes
        self.assertEqual(result["value"], 2.0)
        self.assertEqual(result["unit"], "minutes")
        self.assertIn("trend", result)
        self.assertIn("change_percentage", result)

    def test_time_on_page_with_no_data(self):
        """Test returns 0 when no activity data exists"""
        result = AnalyticsService.calculate_time_on_page(period="weekly")

        self.assertEqual(result["value"], 0.0)
        self.assertEqual(result["unit"], "minutes")

    def test_filters_out_zero_durations(self):
        """Test that zero durations are excluded from calculation"""
        session = AnalyticsTestHelper.create_session_metrics()

        # Create activities with zero and valid durations
        AnalyticsTestHelper.create_user_activity(
            session=session,
            duration_seconds=0,
        )
        AnalyticsTestHelper.create_user_activity(
            session=session,
            duration_seconds=120,
        )

        result = AnalyticsService.calculate_time_on_page(period="weekly")

        # Should only count the 120 seconds activity = 2 minutes
        self.assertEqual(result["value"], 2.0)

    def test_period_filtering(self):
        """Test only includes activities within date range"""
        # Create activity outside current period (60 days ago)
        past_date = timezone.now() - timedelta(days=60)
        session = AnalyticsTestHelper.create_session_metrics(start_time=past_date)
        AnalyticsTestHelper.create_user_activity(
            session=session, duration_seconds=300, timestamp=past_date
        )

        # Create activity in current period
        session2 = AnalyticsTestHelper.create_session_metrics()
        AnalyticsTestHelper.create_user_activity(
            session=session2, duration_seconds=120, timestamp=timezone.now()
        )

        result = AnalyticsService.calculate_time_on_page(period="weekly")

        # Should only count recent activity (120 seconds = 2 minutes)
        self.assertEqual(result["value"], 2.0)


class TestAnalyticsServiceBounceRate(APITestCase):
    """Tests for calculate_bounce_rate method"""

    def test_bounce_rate_with_mixed_sessions(self):
        """Test bounce rate calculation with bounced and non-bounced sessions"""
        # Create 3 bounce sessions
        AnalyticsTestHelper.create_bounce_sessions()

        # Create 7 non-bounce sessions
        AnalyticsTestHelper.create_non_bounce_sessions(count=7)

        result = AnalyticsService.calculate_bounce_rate(period="weekly")

        # 3 bounces out of 10 total = 30%
        self.assertEqual(result["value"], 30.0)
        self.assertEqual(result["unit"], "percentage")

    def test_bounce_rate_with_no_sessions(self):
        """Test returns 0 when no sessions exist"""
        result = AnalyticsService.calculate_bounce_rate(period="weekly")

        self.assertEqual(result["value"], 0.0)
        self.assertEqual(result["unit"], "percentage")

    def test_bounce_rate_all_bounced(self):
        """Test bounce rate when all sessions bounced"""
        AnalyticsTestHelper.create_bounce_sessions(count=5)

        result = AnalyticsService.calculate_bounce_rate(period="weekly")

        self.assertEqual(result["value"], 100.0)

    def test_bounce_rate_no_bounces(self):
        """Test bounce rate when no sessions bounced"""
        AnalyticsTestHelper.create_non_bounce_sessions(count=5)

        result = AnalyticsService.calculate_bounce_rate(period="weekly")

        self.assertEqual(result["value"], 0.0)

    def test_period_filtering(self):
        """Test only includes sessions within date range"""
        # Create old session (outside range)
        past_date = timezone.now() - timedelta(days=60)
        AnalyticsTestHelper.create_session_metrics(
            start_time=past_date, is_bounce=True, page_count=1
        )

        # Create recent bounced session
        AnalyticsTestHelper.create_bounce_sessions(count=1)

        # Create recent non-bounced session
        AnalyticsTestHelper.create_non_bounce_sessions(count=1)

        result = AnalyticsService.calculate_bounce_rate(period="weekly")

        # Should be 50% (1 bounce out of 2 recent sessions)
        self.assertEqual(result["value"], 50.0)


class TestAnalyticsServiceLoadSpeed(APITestCase):
    """Tests for calculate_load_speed method"""

    def test_load_speed_calculation(self):
        """Test average load speed calculation in seconds"""
        # Create page load activities with known load times
        # 2000ms, 3000ms, 4000ms
        for load_time in [2000, 3000, 4000]:
            session = AnalyticsTestHelper.create_session_metrics()
            AnalyticsTestHelper.create_user_activity(
                session=session,
                event_type=EventTypeChoices.PAGE_LOAD,
                load_time_ms=load_time,
            )

        result = AnalyticsService.calculate_load_speed(period="weekly")

        # Average: 3000ms = 3.0 seconds
        self.assertEqual(result["value"], 3.0)
        self.assertEqual(result["unit"], "seconds")

    def test_filters_only_page_load_events(self):
        """Test only PAGE_LOAD events are included"""
        session = AnalyticsTestHelper.create_session_metrics()

        # Create PAGE_VIEW with load time (should be ignored)
        AnalyticsTestHelper.create_user_activity(
            session=session,
            event_type=EventTypeChoices.PAGE_VIEW,
            load_time_ms=5000,
        )

        # Create PAGE_LOAD with load time (should be counted)
        AnalyticsTestHelper.create_user_activity(
            session=session,
            event_type=EventTypeChoices.PAGE_LOAD,
            load_time_ms=2000,
        )

        result = AnalyticsService.calculate_load_speed(period="weekly")

        # Should only count PAGE_LOAD: 2000ms = 2.0 seconds
        self.assertEqual(result["value"], 2.0)

    def test_filters_out_zero_load_times(self):
        """Test zero load times are excluded"""
        session = AnalyticsTestHelper.create_session_metrics()

        AnalyticsTestHelper.create_user_activity(
            session=session,
            event_type=EventTypeChoices.PAGE_LOAD,
            load_time_ms=0,
        )
        AnalyticsTestHelper.create_user_activity(
            session=session,
            event_type=EventTypeChoices.PAGE_LOAD,
            load_time_ms=3000,
        )

        result = AnalyticsService.calculate_load_speed(period="weekly")

        self.assertEqual(result["value"], 3.0)

    def test_filters_out_null_load_times(self):
        """Test null load times are excluded"""
        session = AnalyticsTestHelper.create_session_metrics()

        AnalyticsTestHelper.create_user_activity(
            session=session,
            event_type=EventTypeChoices.PAGE_LOAD,
            load_time_ms=None,
            timestamp=timezone.now(),
        )
        AnalyticsTestHelper.create_user_activity(
            session=session,
            event_type=EventTypeChoices.PAGE_LOAD,
            load_time_ms=2500,
            timestamp=timezone.now(),
        )

        result = AnalyticsService.calculate_load_speed(period="weekly")

        self.assertEqual(result["value"], 2.5)

    def test_no_load_data_returns_zero(self):
        """Test returns 0 when no load data exists"""
        result = AnalyticsService.calculate_load_speed(period="weekly")

        self.assertEqual(result["value"], 0.0)


class TestAnalyticsServiceDeviceDistribution(APITestCase):
    """Tests for get_device_distribution method"""

    def test_device_distribution_with_multiple_types(self):
        """Test device distribution calculation with multiple device types"""
        AnalyticsTestHelper.create_device_distribution(mobile=10, desktop=20, tablet=5)

        result = AnalyticsService.get_device_distribution(period="weekly")

        # Should return 3 items ordered by count (desktop, mobile, tablet)
        self.assertEqual(len(result), 3)

        # Check desktop (highest count)
        desktop = next(
            item for item in result if item["name"] == DeviceTypeChoices.DESKTOP
        )
        self.assertEqual(desktop["value"], 20)
        self.assertEqual(
            desktop["percentage"], 57.0
        )  # 20/35 * 100 = 57.14, rounded to 57

        # Check mobile
        mobile = next(
            item for item in result if item["name"] == DeviceTypeChoices.MOBILE
        )
        self.assertEqual(mobile["value"], 10)
        self.assertEqual(
            mobile["percentage"], 29.0
        )  # 10/35 * 100 = 28.57, rounded to 29

        # Check tablet
        tablet = next(
            item for item in result if item["name"] == DeviceTypeChoices.TABLET
        )
        self.assertEqual(tablet["value"], 5)
        self.assertEqual(
            tablet["percentage"], 14.0
        )  # 5/35 * 100 = 14.28, rounded to 14

    def test_device_distribution_ordered_by_count(self):
        """Test results are ordered by count descending"""
        AnalyticsTestHelper.create_device_distribution(mobile=15, desktop=5, tablet=25)

        result = AnalyticsService.get_device_distribution(period="weekly")

        # Should be ordered: tablet (25), mobile (15), desktop (5)
        self.assertEqual(result[0]["name"], DeviceTypeChoices.TABLET)
        self.assertEqual(result[1]["name"], DeviceTypeChoices.MOBILE)
        self.assertEqual(result[2]["name"], DeviceTypeChoices.DESKTOP)

    def test_device_distribution_with_unknown_device(self):
        """Test handles null device types as Unknown"""
        session = AnalyticsTestHelper.create_session_metrics()
        AnalyticsTestHelper.create_user_activity(
            session=session, device_type=None, timestamp=timezone.now()
        )

        result = AnalyticsService.get_device_distribution(period="weekly")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Unknown")
        self.assertEqual(result[0]["value"], 1)

    def test_device_distribution_no_data(self):
        """Test returns empty list when no activities exist"""
        result = AnalyticsService.get_device_distribution(period="weekly")

        self.assertEqual(result, [])

    def test_percentage_calculation_accuracy(self):
        """Test percentage calculations are rounded correctly"""
        # Create exact scenario for testing rounding
        AnalyticsTestHelper.create_device_distribution(mobile=33, desktop=33, tablet=34)

        result = AnalyticsService.get_device_distribution(period="weekly")

        # Percentages should roughly sum to 100
        total_percentage = sum(item["percentage"] for item in result)
        self.assertGreaterEqual(total_percentage, 99)
        self.assertLessEqual(total_percentage, 101)


class TestAnalyticsServiceActiveUsersTimeline(APITestCase):
    """Tests for get_active_users_timeline method"""

    def test_daily_breakdown_with_data(self):
        """Test daily active users breakdown"""
        date_range = AnalyticsService.get_date_range("weekly")
        test_date = date_range["current_start"]

        # Create users for the first day
        user1 = TestUtil.verified_user()
        user2 = TestUtil.other_verified_user()

        # Registered users
        for user in [user1, user2]:
            session = AnalyticsTestHelper.create_session_metrics(
                user=user,
                # Combines a date + time into a datetime object
                start_time=timezone.make_aware(
                    timezone.datetime.combine(test_date, timezone.datetime.min.time())
                ),
            )
            AnalyticsTestHelper.create_user_activity(
                session=session, user=user, timestamp=session.start_time
            )

        # Visitors (anonymous)
        for _ in range(3):
            session = AnalyticsTestHelper.create_session_metrics(
                user=None,
                start_time=timezone.make_aware(
                    timezone.datetime.combine(test_date, timezone.datetime.min.time())
                ),
            )
            AnalyticsTestHelper.create_user_activity(
                session=session, user=None, timestamp=session.start_time
            )

        result = AnalyticsService.get_active_users_timeline(period="weekly")

        # Check first day
        first_day = result[0]
        self.assertEqual(first_day["registered_users"], 2)
        self.assertEqual(first_day["visitors"], 3)
        self.assertEqual(first_day["total_active_users"], 5)

    def test_date_formatting(self):
        """Test date and day formatting in timeline"""
        result = AnalyticsService.get_active_users_timeline(period="weekly")

        # Should have 7 days for weekly period
        self.assertEqual(len(result), 7)

        for day_data in result:
            # Check ISO format date
            self.assertIn("date", day_data)
            self.assertRegex(day_data["date"], r"^\d{4}-\d{2}-\d{2}$")

            # Check abbreviated day name
            self.assertIn("day", day_data)
            self.assertIn(
                day_data["day"], ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            )

    def test_distinct_user_counting(self):
        """Test same user with multiple activities counts as one"""
        date_range = AnalyticsService.get_date_range("weekly")
        test_date = date_range["current_start"]

        user = TestUtil.verified_user()
        session = AnalyticsTestHelper.create_session_metrics(
            user=user,
            start_time=timezone.make_aware(
                timezone.datetime.combine(test_date, timezone.datetime.min.time())
            ),
        )

        # Create 5 activities for same user on same day
        for _ in range(5):
            AnalyticsTestHelper.create_user_activity(
                session=session, user=user, timestamp=session.start_time
            )

        result = AnalyticsService.get_active_users_timeline(period="weekly")
        first_day = result[0]

        # Should count as only 1 registered user
        self.assertEqual(first_day["registered_users"], 1)

    def test_distinct_session_counting_for_visitors(self):
        """Test same session with multiple activities counts as one visitor"""
        date_range = AnalyticsService.get_date_range("weekly")
        test_date = date_range["current_start"]

        session = AnalyticsTestHelper.create_session_metrics(
            user=None,
            start_time=timezone.make_aware(
                timezone.datetime.combine(test_date, timezone.datetime.min.time())
            ),
        )

        # Create 5 activities for same anonymous session on same day
        for _ in range(5):
            AnalyticsTestHelper.create_user_activity(
                session=session, user=None, timestamp=session.start_time
            )

        result = AnalyticsService.get_active_users_timeline(period="weekly")
        first_day = result[0]

        # Should count as only 1 visitor
        self.assertEqual(first_day["visitors"], 1)

    def test_days_with_no_activity(self):
        """Test days with no activity return zero counts"""
        result = AnalyticsService.get_active_users_timeline(period="weekly")

        # All days should exist with 0 counts
        for day_data in result:
            self.assertEqual(day_data["registered_users"], 0)
            self.assertEqual(day_data["visitors"], 0)
            self.assertEqual(day_data["total_active_users"], 0)

    def test_covers_entire_period(self):
        """Test timeline covers all days in period"""
        result = AnalyticsService.get_active_users_timeline(period="weekly")

        # Weekly should have 7 days
        self.assertEqual(len(result), 7)

        # Verify dates are consecutive
        for i in range(len(result) - 1):
            current_date = timezone.datetime.fromisoformat(result[i]["date"])
            next_date = timezone.datetime.fromisoformat(result[i + 1]["date"])
            self.assertEqual((next_date - current_date).days, 1)


class TestAnalyticsServiceTopPerformingPosts(APITestCase):
    """Tests for get_top_performing_posts method"""

    def test_returns_top_article_by_views(self):
        """Test returns the single top article with most views"""
        # Create 3 articles with different view counts
        _ = AnalyticsTestHelper.create_article_with_analytics(views=5, shares=2)
        article2 = AnalyticsTestHelper.create_article_with_analytics(views=15, shares=3)
        _ = AnalyticsTestHelper.create_article_with_analytics(views=10, shares=1)

        result = AnalyticsService.get_top_performing_posts(period="weekly")

        # Should only return article2 (highest views)
        articles = [item for item in result if item["category"] == "Articles"]
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0]["id"], str(article2.id))
        self.assertEqual(articles[0]["views"], 15)
        self.assertEqual(articles[0]["shares"], 3)
        self.assertEqual(articles[0]["title"], article2.title)

    def test_returns_top_job_by_views(self):
        """Test returns the single top job with most views"""
        _ = AnalyticsTestHelper.create_job_with_analytics(views=8, shares=2)
        job2 = AnalyticsTestHelper.create_job_with_analytics(views=12, shares=4)

        result = AnalyticsService.get_top_performing_posts(period="weekly")

        jobs = [item for item in result if item["category"] == "Jobs"]
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]["id"], str(job2.id))
        self.assertEqual(jobs[0]["views"], 12)
        self.assertEqual(jobs[0]["shares"], 4)

    def test_returns_top_event_by_views(self):
        """Test returns the single top event with most views"""
        _ = AnalyticsTestHelper.create_event_with_analytics(views=6, shares=1)
        event2 = AnalyticsTestHelper.create_event_with_analytics(views=9, shares=3)

        result = AnalyticsService.get_top_performing_posts(period="weekly")

        events = [item for item in result if item["category"] == "Events"]
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["id"], str(event2.id))
        self.assertEqual(events[0]["views"], 9)
        self.assertEqual(events[0]["shares"], 3)

    def test_returns_all_three_categories(self):
        """Test returns one item from each category"""
        AnalyticsTestHelper.create_article_with_analytics(views=10, shares=2)
        AnalyticsTestHelper.create_job_with_analytics(views=8, shares=1)
        AnalyticsTestHelper.create_event_with_analytics(views=6, shares=3)

        result = AnalyticsService.get_top_performing_posts(period="weekly")

        # Should have 3 items (one per category)
        self.assertEqual(len(result), 3)
        categories = [item["category"] for item in result]
        self.assertIn("Articles", categories)
        self.assertIn("Jobs", categories)
        self.assertIn("Events", categories)

    def test_handles_non_existent_content_gracefully(self):
        """Test gracefully handles when content is deleted but activities exist"""
        # Create article with analytics
        article = AnalyticsTestHelper.create_article_with_analytics(views=10, shares=2)
        article_id = article.id

        # Delete the article
        article.delete()

        # Should not crash and should skip this article
        result = AnalyticsService.get_top_performing_posts(period="weekly")

        # Should return empty or not include deleted article
        article_ids = [
            item.get("id") for item in result if item["category"] == "Articles"
        ]
        self.assertNotIn(str(article_id), article_ids)

    def test_no_views_returns_empty_list(self):
        """Test returns empty list when no views exist"""
        result = AnalyticsService.get_top_performing_posts(period="weekly")

        self.assertEqual(result, [])

    def test_period_filtering(self):
        """Test only counts views within specified period"""
        article = AnalyticsTestHelper.create_article_with_analytics(views=5, shares=2)

        # Create old view (outside period)
        past_date = timezone.now() - timedelta(days=60)
        session = AnalyticsTestHelper.create_session_metrics(start_time=past_date)
        AnalyticsTestHelper.create_user_activity(
            session=session,
            event_type=EventTypeChoices.PAGE_VIEW,
            timestamp=past_date,
            metadata={"content_type": "article", "content_id": str(article.id)},
        )

        result = AnalyticsService.get_top_performing_posts(period="weekly")

        # Should only count the 5 recent views, not the old one
        articles = [item for item in result if item["category"] == "Articles"]
        if articles:
            self.assertEqual(articles[0]["views"], 5)

    def test_shares_count_accuracy(self):
        """Test shares are counted correctly for top post"""
        _ = AnalyticsTestHelper.create_article_with_analytics(views=10, shares=7)

        result = AnalyticsService.get_top_performing_posts(period="weekly")

        articles = [item for item in result if item["category"] == "Articles"]
        self.assertEqual(articles[0]["shares"], 7)


class TestAnalyticsServiceDashboardMetrics(APITestCase):
    """Tests for get_dashboard_metrics integration method"""

    def test_dashboard_metrics_structure(self):
        """Test dashboard metrics returns complete data structure"""
        result = AnalyticsService.get_dashboard_metrics(period="weekly")

        # Check top-level keys
        self.assertIn("period", result)
        self.assertIn("date_range", result)
        self.assertIn("metrics", result)
        self.assertIn("device_types", result)
        self.assertIn("active_users", result)
        self.assertIn("top_performing_posts", result)

        # Check period value
        self.assertEqual(result["period"], "weekly")

        # Check date_range structure
        self.assertIn("start", result["date_range"])
        self.assertIn("end", result["date_range"])

        # Check metrics structure
        self.assertIn("time_on_page", result["metrics"])
        self.assertIn("bounce_rate", result["metrics"])
        self.assertIn("load_speed", result["metrics"])

    def test_dashboard_metrics_with_weekly_period(self):
        """Test dashboard metrics with weekly period parameter"""
        result = AnalyticsService.get_dashboard_metrics(period="weekly")

        self.assertEqual(result["period"], "weekly")

        # Active users should have 7 days
        self.assertEqual(len(result["active_users"]), 7)

    def test_dashboard_metrics_with_monthly_period(self):
        """Test dashboard metrics with monthly period parameter"""
        result = AnalyticsService.get_dashboard_metrics(period="monthly")

        self.assertEqual(result["period"], "monthly")

    def test_dashboard_metrics_with_actual_data(self):
        """Test dashboard metrics calculates all sub-metrics correctly"""
        # Create comprehensive test data
        AnalyticsTestHelper.create_bounce_sessions(count=2)
        AnalyticsTestHelper.create_non_bounce_sessions(count=8)
        AnalyticsTestHelper.create_page_load_activities(count=5, avg_load_time_ms=2000)
        AnalyticsTestHelper.create_device_distribution(mobile=10, desktop=20, tablet=5)
        AnalyticsTestHelper.create_article_with_analytics(views=15, shares=5)

        result = AnalyticsService.get_dashboard_metrics(period="weekly")

        # Verify metrics are calculated
        self.assertIsNotNone(result["metrics"]["time_on_page"]["value"])
        self.assertIsNotNone(result["metrics"]["bounce_rate"]["value"])
        self.assertIsNotNone(result["metrics"]["load_speed"]["value"])

        # Verify device types are populated
        self.assertGreater(len(result["device_types"]), 0)

        # Verify top posts are populated
        self.assertGreater(len(result["top_performing_posts"]), 0)

    def test_date_range_format(self):
        """Test date range is in ISO format"""
        result = AnalyticsService.get_dashboard_metrics(period="weekly")

        start_date = result["date_range"]["start"]
        end_date = result["date_range"]["end"]

        # Should be valid ISO date strings
        self.assertRegex(start_date, r"^\d{4}-\d{2}-\d{2}")
        self.assertRegex(end_date, r"^\d{4}-\d{2}-\d{2}")

    def test_metrics_contain_trend_data(self):
        """Test all metrics include trend and change percentage"""
        result = AnalyticsService.get_dashboard_metrics(period="weekly")

        for metric_name in ["time_on_page", "bounce_rate", "load_speed"]:
            metric = result["metrics"][metric_name]
            self.assertIn("value", metric)
            self.assertIn("unit", metric)
            self.assertIn("trend", metric)
            self.assertIn("change_percentage", metric)


# python manage.py test apps.analytics.tests.test_service.TestAnalyticsServiceDateRange
# python manage.py test apps.analytics.tests.test_service.TestAnalyticsServiceMetricTrend
# python manage.py test apps.analytics.tests.test_service.TestAnalyticsServiceTimeOnPage
# python manage.py test apps.analytics.tests.test_service.TestAnalyticsServiceBounceRate
# python manage.py test apps.analytics.tests.test_service.TestAnalyticsServiceLoadSpeed
# python manage.py test apps.analytics.tests.test_service.TestAnalyticsServiceDeviceDistribution
# python manage.py test apps.analytics.tests.test_service.TestAnalyticsServiceActiveUsersTimeline
# python manage.py test apps.analytics.tests.test_service.TestAnalyticsServiceTopPerformingPosts
# python manage.py test apps.analytics.tests.test_service.TestAnalyticsServiceDashboardMetrics
