from datetime import timedelta
from unittest.mock import patch

from apps.accounts.models import Otp, User
from apps.common.errors import ErrorCode
from apps.common.schema_examples import ERR_RESPONSE_STATUS, SUCCESS_RESPONSE_STATUS
from apps.common.utils import TestUtil
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase

valid_data = {
    "first_name": "Test",
    "last_name": "User",
    "email": "testuser@example.com",
    "password": "Strong_password124$",
}

invalid_data = {
    "first_name": "",
    "last_name": "User",
    "email": "invalid_email",
    "password": "short",
}

VALIDATION_ERROR = "VALIDATION_ERROR"
EXPIRED = "expired"


class TestAccounts(APITestCase):
    register_url = "/api/v1/auth/register/"
    login_url = "/api/v1/auth/token/"
    token_refresh_url = "/api/v1/auth/token/refresh/"
    logout_url = "/api/v1/auth/sessions/"
    logout_all_url = "/api/v1/auth/sessions/all/"

    send_email_url = "/api/v1/auth/verification/"
    verify_email_url = "/api/v1/auth/verification/verify/"

    password_change_url = "/api/v1/auth/passwords/change/"
    password_reset_request_url = "/api/v1/auth/passwords/reset/"
    password_reset_verify_otp_url = "/api/v1/auth/passwords/reset/verify/"
    password_reset_done_url = "/api/v1/auth/passwords/reset/complete/"

    def setUp(self):
        self.new_user = TestUtil.new_user()
        self.verified_user = TestUtil.verified_user()
        self.disabled_user = TestUtil.disabled_user()

    @patch("apps.accounts.emails.SendEmail.send_email")
    def test_register(self, mock_send_email):
        # Valid Registration
        response = self.client.post(self.register_url, valid_data)

        mock_send_email.assert_called_once()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {
                "status": SUCCESS_RESPONSE_STATUS,
                "message": "OTP sent for email verification.",
                "data": {"email": valid_data["email"]},
            },
        )

        # Invalid Registration - 422
        response = self.client.post(self.register_url, invalid_data)

        self.assertEqual(response.status_code, 422)

    def test_login(self):
        # Disabled account - 403
        response = self.client.post(
            self.login_url,
            {
                "email": self.disabled_user.email,
                "password": "testpassword789#",
            },
        )

        self.assertEqual(response.status_code, 403)

        # Valid Login
        response = self.client.post(
            self.login_url,
            {
                "email": self.verified_user.email,
                "password": "Verified2001#",
            },
        )

        self.assertEqual(response.status_code, 200)

        # Invalid Login - Incorrect Password
        response = self.client.post(
            self.login_url,
            {
                "email": self.verified_user.email,
                "password": "wrongpassword",
            },
        )

        self.assertEqual(response.status_code, 401)

        # Invalid Login - empty Password
        response = self.client.post(
            self.login_url,
            {
                "email": self.verified_user.email,
                "password": "",
            },
        )

        self.assertEqual(response.status_code, 422)

        # invalid login - email not verified
        response = self.client.post(
            self.login_url,
            {
                "email": self.new_user.email,
                "password": "Testpassword2008@",
            },
        )

        self.assertEqual(response.status_code, 403)

    @patch("apps.accounts.emails.SendEmail.send_email")
    def test_resend_verification_email(self, mock_send_email):
        # OTP Sent for Existing User
        response = self.client.post(self.send_email_url, {"email": self.new_user.email})
        mock_send_email.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "status": SUCCESS_RESPONSE_STATUS,
                "message": "OTP sent successfully.",
            },
        )

        # Non-existent User
        response = self.client.post(self.send_email_url, {"email": "user@gmail.com"})
        self.assertEqual(response.status_code, 422)

        self.assertEqual(
            response.json(),
            {
                "status": ERR_RESPONSE_STATUS,
                "message": "No account is associated with this email.",
                "code": ErrorCode.VALIDATION_ERROR,
            },
        )

        # Invalid email
        response = self.client.post(self.send_email_url, {"email": "user"})

        self.assertEqual(response.status_code, 422)

        # email already verified
        response = self.client.post(
            self.send_email_url, {"email": self.verified_user.email}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "status": SUCCESS_RESPONSE_STATUS,
                "message": "Your email is already verified. No OTP sent.",
            },
        )

    @patch("apps.accounts.emails.SendEmail.welcome")
    def test_verify_email(self, mock_send_email):
        new_user = self.new_user
        otp = "111111"

        # Invalid OTP
        response = self.client.post(
            self.verify_email_url, {"email": new_user.email, "otp": "hgtr"}
        )
        self.assertEqual(response.status_code, 422)

        # OTP does not exist
        response = self.client.post(
            self.verify_email_url, {"email": new_user.email, "otp": int(otp)}
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json(),
            {
                "status": ERR_RESPONSE_STATUS,
                "message": "Invalid OTP provided.",
                "code": ErrorCode.VALIDATION_ERROR,
            },
        )

        # Valid OTP Verification
        otp = Otp.objects.create(user_id=new_user.id, otp=int(otp))
        response = self.client.post(
            self.verify_email_url,
            {"email": new_user.email, "otp": otp.otp},
        )
        mock_send_email.assert_called_once()
        self.assertEqual(response.status_code, 200)

        # Clear OTP After Verification
        otp_cleared = not Otp.objects.filter(user_id=new_user.id).exists()

        self.assertTrue(otp_cleared, "OTP should be cleared after verification.")
        self.assertEqual(
            response.json(),
            {
                "status": SUCCESS_RESPONSE_STATUS,
                "message": "Email verified successfully.",
            },
        )

        # Expired OTP
        otp = Otp.objects.create(
            user_id=self.new_user.id,
            otp=int("876547"),
            created_at="2023-10-01T12:00:00Z",
        )
        response = self.client.post(
            self.verify_email_url,
            {"email": new_user.email, "otp": otp.otp},
        )
        self.assertEqual(response.status_code, 498)
        self.assertEqual(
            response.json(),
            {
                "status": ERR_RESPONSE_STATUS,
                "message": "OTP has expired, please request a new one.",
                "code": EXPIRED,
            },
        )

        # Already Verified User
        otp = Otp.objects.create(user_id=self.verified_user.id, otp=int("876547"))
        response = self.client.post(
            self.verify_email_url,
            {"email": self.verified_user.email, "otp": otp.otp},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "status": SUCCESS_RESPONSE_STATUS,
                "message": "Email address already verified. No OTP sent.",
            },
        )

    def test_logout(self):
        # Successful Logout
        if settings.DEBUG:
            verified_user = self.verified_user
            login_response = self.client.post(
                self.login_url,
                {
                    "email": verified_user.email,
                    "password": "Verified2001#",
                },
            )

            # Check login response and refresh token
            self.assertEqual(login_response.status_code, 200)
            refresh_token = login_response.json().get("data").get("refresh")
            self.assertIsNotNone(
                refresh_token, "Refresh token should be provided upon login"
            )

            # Successful Logout using the refresh token
            response = self.client.post(
                self.logout_url,
                {
                    "refresh": refresh_token,
                },
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.json(),
                {
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Logged out successfully.",
                },
            )

            # Invalid Refresh Token
            response = self.client.post(
                self.logout_url,
                {
                    "refresh": f"{refresh_token}_invalid_refresh_token",
                },
            )

            self.assertEqual(response.status_code, 401)

            # Missing Refresh Token
            response = self.client.post(
                self.logout_url,
                {
                    "refresh": "",
                },
            )

            self.assertEqual(response.status_code, 422)

    def test_logout_all(self):
        # Test unauthorized access
        unauthorized_response = self.client.post(self.logout_all_url)

        self.assertEqual(unauthorized_response.status_code, 401)

        # First login to get tokens
        login_response = self.client.post(
            self.login_url,
            {
                "email": self.verified_user.email,
                "password": "Verified2001#",
            },
        )

        self.assertEqual(login_response.status_code, 200)
        access_token = login_response.json()["data"]["access"]

        # Set authorization header for authenticated request
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        # Make logout all request
        response = self.client.post(self.logout_all_url)

        # Assert response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "status": SUCCESS_RESPONSE_STATUS,
                "message": "Successfully logged out from all devices.",
            },
        )

        if settings.DEBUG:
            # Verify tokens are blacklisted by trying to use them
            refresh_token = login_response.json()["data"]["refresh"]
            refresh_response = self.client.post(
                self.token_refresh_url, {"refresh": refresh_token}
            )

            self.assertEqual(refresh_response.status_code, 401)

    def test_password_change(self):
        verified_user = self.verified_user

        # Unauthenticated trying to change password
        response = self.client.post(
            self.password_change_url,
            {"old_password": verified_user.password, "new_password": "Verified2001#"},
        )

        self.assertEqual(response.status_code, 401)

        # Valid Password Change
        # login the user
        login_response = self.client.post(
            self.login_url,
            {"email": verified_user.email, "password": "Verified2001#"},
        )

        access_token = login_response.json().get("data").get("access")
        bearer_headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
        response = self.client.post(
            self.password_change_url,
            {
                "old_password": "Verified2001#",
                "new_password": "Testimony74&",
                "confirm_password": "Testimony74&",
            },
            **bearer_headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "status": SUCCESS_RESPONSE_STATUS,
                "message": "Password changed successfully.",
            },
        )

        # Incorrect Current Password
        response = self.client.post(
            self.password_change_url,
            {
                "old_password": "testpass",
                "confirm_password": "testimony74",
                "new_password": "testimony74",
            },
            **bearer_headers,
        )

        self.assertEqual(response.status_code, 422)

        # Weak New Password
        response = self.client.post(
            self.password_change_url,
            {
                "old_password": "Verified2001#",
                "confirm_password": "test",
                "new_password": "test",
            },
            **bearer_headers,
        )

        self.assertEqual(response.status_code, 422)

    @patch("apps.accounts.emails.SendEmail.send_password_reset_email")
    def test_password_reset_request(self, mock_send_email):
        verified_user = self.verified_user

        # Send OTP to Registered Email
        response = self.client.post(
            self.password_reset_request_url, {"email": verified_user.email}
        )
        mock_send_email.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"status": SUCCESS_RESPONSE_STATUS, "message": "OTP sent successfully."},
        )

        # Non-existent Email
        response = self.client.post(
            self.password_reset_request_url, {"email": "tom@gmail.com"}
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json(),
            {
                "status": ERR_RESPONSE_STATUS,
                "message": "User with this email does not exist.",
                "code": ErrorCode.VALIDATION_ERROR,
            },
        )

    def test_verify_otp(self):
        verified_user = self.verified_user
        otp = "123456"
        otp_obj = Otp.objects.create(user=verified_user, otp=otp)

        # user does not exist
        response = self.client.post(
            self.password_reset_verify_otp_url,
            {"email": "nonexistentuser@example.com", "otp": int(otp)},
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json(),
            {
                "status": ERR_RESPONSE_STATUS,
                "message": "No account is associated with this email.",
                "code": ErrorCode.VALIDATION_ERROR,
            },
        )

        # Otp does not exist
        response = self.client.post(
            self.password_reset_verify_otp_url,
            {"email": verified_user.email, "otp": int("123457")},
        )
        self.assertEqual(response.status_code, 422)

        self.assertEqual(
            response.json(),
            {
                "status": ERR_RESPONSE_STATUS,
                "message": "The OTP could not be found. Please enter a valid OTP or request a new one.",
                "code": ErrorCode.VALIDATION_ERROR,
            },
        )

        # otp is expired
        otp_obj.created_at = timezone.now() - timedelta(hours=2)
        otp_obj.save()
        response = self.client.post(
            self.password_reset_verify_otp_url,
            {"email": verified_user.email, "otp": int(otp)},
        )

        self.assertEqual(response.status_code, 498)
        self.assertEqual(
            response.json(),
            {
                "status": ERR_RESPONSE_STATUS,
                "message": "OTP has expired, please request a new one.",
                "code": EXPIRED,
            },
        )

        # otp exists
        otp_obj.created_at = timezone.now()  # Resetting OTP's timestamp to be valid
        otp_obj.save()
        response = self.client.post(
            self.password_reset_verify_otp_url,
            {"email": verified_user.email, "otp": int(otp)},
        )
        self.assertEqual(response.status_code, 200)
        # otp is cleared after verification
        otp_cleared = not Otp.objects.filter(user_id=verified_user.id).exists()
        self.assertTrue(otp_cleared, "OTP should be cleared after password reset.")
        self.assertEqual(
            response.json(),
            {
                "status": SUCCESS_RESPONSE_STATUS,
                "message": "OTP verified, proceed to set a new password.",
            },
        )

        # otp is a letter or less than min or greater than min value
        response = self.client.post(
            self.password_reset_verify_otp_url,
            {"email": verified_user.email, "otp": "abc123"},
        )
        self.assertEqual(response.status_code, 422)

        response = self.client.post(
            self.password_reset_verify_otp_url,
            {"email": verified_user.email, "otp": int("123456789")},
        )
        self.assertEqual(response.status_code, 422)

    def test_password_reset_done(self):
        verified_user = self.verified_user

        # user does not exist
        response = self.client.post(
            self.password_reset_done_url,
            {
                "email": "nonexistentuser@example.com",
                "new_password": "NewPassword123$",
                "confirm_password": "NewPassword123$",
            },
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json(),
            {
                "status": ERR_RESPONSE_STATUS,
                "message": "No account is associated with this email.",
                "code": ErrorCode.VALIDATION_ERROR,
            },
        )

        # Successful Password Reset
        response = self.client.post(
            self.password_reset_done_url,
            {
                "email": verified_user.email,
                "new_password": "NewPassword123#",
                "confirm_password": "NewPassword123#",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "status": SUCCESS_RESPONSE_STATUS,
                "message": "Your password has been reset, proceed to login.",
            },
        )

        # Weak New Password
        response = self.client.post(
            self.password_reset_done_url,
            {"email": verified_user.email, "new_password": "weak"},
        )

        self.assertEqual(response.status_code, 422)


class TestProfiles(APITestCase):
    profile_url = "/api/v1/auth/profile/"
    avatar_update_url = "/api/v1/auth/profile/avatar/"

    def setUp(self):
        self.user1 = TestUtil.verified_user()
        self.user2 = TestUtil.other_verified_user()

    def test_profile(self):

        # Test successful retrieval for authenticated users
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)

        user1 = User.objects.get(id=response.data["data"]["id"])
        self.assertEqual(str(user1.id), str(self.user1.id))

        # Test you can only retrieve your own profile
        # Switch to user2 and verify they get their own profile
        self.client.force_authenticate(user=self.user2)

        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)

        user2 = User.objects.get(id=response.data["data"]["id"])
        self.assertEqual(str(user2.id), str(self.user2.id))

        # Test 401 for unauthorized user
        self.client.force_authenticate(user=None)

        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 401)

    def test_avatar_update(self):
        # Test success
        
        self.client.force_authenticate(user=self.user1)

        image_content = b"GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
        image = SimpleUploadedFile(
            "test_image.gif", image_content, content_type="image/gif"
        )

        response = self.client.patch(
            self.avatar_update_url, {"avatar": image}, format="multipart"
        )

        self.assertEqual(response.status_code, 200)
        self.user1.refresh_from_db()
        self.assertTrue(self.user1.avatar)

        # Test 401 for unauthenticated users
        self.client.force_authenticate(user=None)

        response = self.client.patch(
            self.avatar_update_url, {"avatar": image}, format="multipart"
        )

        self.assertEqual(response.status_code, 401)


class TestGoogleOAuth(APITestCase):
    def setUp(self):
        self.signup_url = reverse("google_signup")
        self.login_url = reverse("google_login")

    def test_google_signup(self):
        # Test successful redirect URL generation
        response = self.client.get(self.signup_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], SUCCESS_RESPONSE_STATUS)
        self.assertIn("authorization_url", response.json()["data"])

    def test_google_login(self):
        # Test successful redirect URL generation
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], SUCCESS_RESPONSE_STATUS)
        self.assertIn("authorization_url", response.json()["data"])


# python manage.py test apps.accounts.tests.TestAccounts.test_register
# python manage.py test apps.accounts.tests.TestAccounts.test_register
