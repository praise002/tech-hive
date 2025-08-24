from apps.accounts.models import ContributorOnboarding
from apps.accounts.utils import UserRoles
from apps.common.utils import TestUtil
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase


class TestContents(APITestCase):
    onboarding_url = "/api/v1/contribute/"

    def setUp(self):
        self.user1 = TestUtil.new_user()
        self.user2 = TestUtil.verified_user()
        self.contributor_group = Group.objects.get_or_create(name=UserRoles.CONTRIBUTOR)

    def test_onboarding(self):
        self.valid_data = {"terms_accepted": True}
        self.invalid_data = {"terms_accepted": False}
        # invalid_data_sets = [
        #     {"terms_accepted": "true"},
        #     {"terms_accepted": 1},
        #     {"terms_accepted": None},
        # ]

        # 401
        response = self.client.post(self.onboarding_url, self.valid_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # 422 - Validation error
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(self.onboarding_url, self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertFalse(self.user1.groups.filter(name=UserRoles.CONTRIBUTOR).exists())
        self.assertFalse(ContributorOnboarding.objects.filter(user=self.user1).exists())

        # 422
        # for invalid_data in invalid_data_sets:
        #     with self.subTest(data=invalid_data):
        #         response = self.client.post(self.onboarding_url, invalid_data)
        #         print(response.json())
                # self.assertEqual(
                #     response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY
                # )

        # 422
        response = self.client.post(self.onboarding_url, {})
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertFalse(self.user1.groups.filter(name=UserRoles.CONTRIBUTOR).exists())

        # 200 - Already contributor
        contributor_group = Group.objects.get(name=UserRoles.CONTRIBUTOR)
        self.user1.groups.add(contributor_group)
        response = self.client.post(self.onboarding_url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 201 - Successfully became contributor
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(self.onboarding_url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.user2.refresh_from_db()
        self.assertTrue(self.user2.groups.filter(name=UserRoles.CONTRIBUTOR).exists())

        self.assertTrue(ContributorOnboarding.objects.filter(user=self.user2).exists())

        onboarding_record = ContributorOnboarding.objects.get(user=self.user2)
        self.assertTrue(onboarding_record.terms_accepted)
        self.assertIsNotNone(onboarding_record.accepted_at)


# python manage.py test apps.content.tests.TestContents.test_onboarding
