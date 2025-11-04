import logging

from apps.accounts.models import User

logger = logging.getLogger(__name__)


class TestUtil:
    def new_user():
        user_dict = {
            "first_name": "Test",
            "last_name": "Name",
            "email": "test@example.com",
            "password": "Testpassword2008@",
        }
        user = User.objects.create_user(**user_dict)
        return user

    def verified_user():
        user_dict = {
            "first_name": "Test",
            "last_name": "Verified",
            "email": "testverifieduser@example.com",
            "is_email_verified": True,
            "password": "Verified2001#",
        }
        user = User.objects.create_user(**user_dict)
        return user

    def other_verified_user():
        user_dict = {
            "first_name": "Test",
            "last_name": "Other",
            "email": "testotheruser@example.com",
            "is_email_verified": True,
            "password": "Testpassword2008@",
        }
        user = User.objects.create_user(**user_dict)
        return user
    
    def another_verified_user():
        user_dict = {
            "first_name": "Test",
            "last_name": "Another",
            "email": "testanotheruser@example.com",
            "is_email_verified": True,
            "password": "Testpassword2008@",
        }
        user = User.objects.create_user(**user_dict)
        return user

    def disabled_user():
        user_dict = {
            "first_name": "Test",
            "last_name": "Disabled",
            "email": "testdisabled@example.com",
            "is_email_verified": True,
            "user_active": False,
            "password": "Testpassword789#",
        }
        user = User.objects.create_user(**user_dict)
        return user
