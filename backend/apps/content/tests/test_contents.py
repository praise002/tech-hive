from apps.common.utils import TestUtil
from apps.content.models import Category, Event, Job, Resource, Tool
from rest_framework import status
from rest_framework.test import APITestCase


class TestContents(APITestCase):
    jobs_url = "/api/v1/jobs/"
    events_url = "/api/v1/events/"
    resources_url = "/api/v1/resources/"
    tools_url = "/api/v1/tools/"
    categories_url = "/api/v1/categories/"

    def setUp(self):
        self.user1 = TestUtil.new_user()
        self.user2 = TestUtil.verified_user()

        # Create test data
        self.category = Category.objects.create(
            name="Technology", desc="Technology related articles"
        )

        self.job1 = Job.objects.create(
            title="Software Engineer",
            company="Tech Co",
            location="San Francisco",
            category=self.category,
            salary=120000,
        )
        self.job2 = Job.objects.create(
            title="Data Scientist",
            company="Data Corp",
            location="New York",
            category=self.category,
            salary=150000,
        )

        self.event1 = Event.objects.create(
            title="Tech Conference",
            location="Las Vegas",
            category=self.category,
            start_date="2025-10-27",
            end_date="2025-10-29",
        )
        self.event2 = Event.objects.create(
            title="AI Summit",
            location="London",
            category=self.category,
            start_date="2025-11-05",
            end_date="2025-11-07",
        )

        self.resource1 = Resource.objects.create(
            name="Django Tutorial", category=self.category
        )
        self.resource2 = Resource.objects.create(
            name="React Docs", category=self.category
        )

        self.tool1 = Tool.objects.create(name="VS Code", category=self.category)
        self.tool2 = Tool.objects.create(name="PyCharm", category=self.category)

    def test_job_list(self):
        """Test job list endpoint"""
        response = self.client.get(self.jobs_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["data"]

        self.assertEqual(len(data["results"]), 2)

    def test_job_detail(self):
        """Test job detail endpoint"""
        response = self.client.get(f"{self.jobs_url}{self.job1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["data"]

        self.assertEqual(data["id"], str(self.job1.id))
        self.assertEqual(data["title"], "Software Engineer")
        self.assertEqual(data["company"], "Tech Co")

    def test_job_detail_not_found(self):
        """Test job detail with invalid ID"""
        import uuid

        fake_id = uuid.uuid4()
        response = self.client.get(f"{self.jobs_url}{fake_id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_event_list(self):
        """Test event list endpoint"""
        response = self.client.get(self.events_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["data"]

        self.assertEqual(len(data["results"]), 2)

    def test_event_detail(self):
        """Test event detail endpoint"""
        response = self.client.get(f"{self.events_url}{self.event1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["data"]

        self.assertEqual(data["id"], str(self.event1.id))
        self.assertEqual(data["title"], "Tech Conference")
        self.assertEqual(data["location"], "Las Vegas")

    def test_event_detail_not_found(self):
        """Test event detail with invalid ID"""
        import uuid

        fake_id = uuid.uuid4()
        response = self.client.get(f"{self.events_url}{fake_id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_resource_list(self):
        """Test resource list endpoint"""
        response = self.client.get(self.resources_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["data"]

        self.assertEqual(len(data["results"]), 2)

    def test_resource_detail(self):
        """Test resource detail endpoint"""
        response = self.client.get(f"{self.resources_url}{self.resource1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["data"]

        self.assertEqual(data["id"], str(self.resource1.id))
        self.assertEqual(data["name"], "Django Tutorial")

    def test_resource_detail_not_found(self):
        """Test resource detail with invalid ID"""
        import uuid

        fake_id = uuid.uuid4()
        response = self.client.get(f"{self.resources_url}{fake_id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_tool_list(self):
        """Test tool list endpoint"""
        response = self.client.get(self.tools_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["data"]

        self.assertEqual(len(data["results"]), 2)

    def test_tool_detail(self):
        """Test tool detail endpoint"""
        response = self.client.get(f"{self.tools_url}{self.tool1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["data"]

        self.assertEqual(data["id"], str(self.tool1.id))
        self.assertEqual(data["name"], "VS Code")

    def test_tool_detail_not_found(self):
        """Test tool detail with invalid ID"""
        import uuid

        fake_id = uuid.uuid4()
        response = self.client.get(f"{self.tools_url}{fake_id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_category_list(self):
        """Test category list endpoint"""
        response = self.client.get(self.categories_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["data"]

        self.assertGreaterEqual(len(data["results"]), 1)

    def test_category_detail(self):
        """Test category detail endpoint"""
        response = self.client.get(f"{self.categories_url}{self.category.slug}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["data"]

        self.assertEqual(data["id"], str(self.category.id))
        self.assertEqual(data["name"], "Technology")
        self.assertEqual(data["slug"], "technology")

    def test_category_detail_not_found(self):
        """Test category detail with invalid slug"""
        response = self.client.get(f"{self.categories_url}non-existent-slug/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# python manage.py test apps.content.tests.test_contents
