from requests_oauthlib import OAuth2Session
from apps.accounts.models import Otp
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework_simplejwt.tokens import BlacklistedToken, OutstandingToken
from rest_framework import serializers
from decouple import config

from backend.apps.common.errors import ErrorCode
from backend.apps.common.responses import CustomResponse

def validate_password_strength(value):
    try:
        validate_password(value)  # This invokes all default password validators
    except DjangoValidationError as e:
        raise serializers.ValidationError(e.messages)  # Raise any validation errors
    return value


def invalidate_previous_otps(user):
    Otp.objects.filter(user=user).delete()
    
def get_otp_record(user, otp):
    """ "Checks for the validity and existence of otp associated with a user"""
    try:
        otp_record = Otp.objects.get(user=user, otp=otp)

        if not otp_record.is_valid:
            return CustomResponse.error(
                message="Invalid or expired OTP. Please enter a valid OTP or request a new one.",
                err_code=ErrorCode.VALIDATION_ERROR,
            )

        return otp_record

    except Otp.DoesNotExist:
        return CustomResponse.error(
            message="Invalid or expired OTP. Please enter a valid OTP or request a new one.",
            err_code=ErrorCode.VALIDATION_ERROR,
        )


def blacklist_token(user):
    for token in OutstandingToken.objects.filter(user=user):
        BlacklistedToken.objects.get_or_create(token=token)


def get_client_ip(request):
    """Extract client IP address from request"""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


client_id = config("GOOGLE_CLIENT_ID")
client_secret = config("GOOGLE_CLIENT_SECRET")
authorization_base_url = config("GOOGLE_AUTH_URL")
token_url = config("GOOGLE_TOKEN_URL")
scope = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

def google_setup(redirect_uri: str):
    # handles the OAuth 2.0 flow
    google = OAuth2Session(
        client_id=client_id,
        scope=scope,
        redirect_uri=redirect_uri,
    )

    # Redirect user to Google for authorization
    authorization_url = google.authorization_url(
        authorization_base_url,
        # offline for refresh token
        # force to always make user click authorize
        access_type="offline",
        prompt="select_account",
    )

    return authorization_url


def google_callback(redirect_uri: str, auth_uri: str, state: str):
    google = OAuth2Session(
        client_id=client_id, scope=scope, redirect_uri=redirect_uri, state=state
    )

    google.fetch_token(
        token_url,
        client_secret=client_secret,
        authorization_response=auth_uri,
    )

    user_data = google.get("https://www.googleapis.com/oauth2/v1/userinfo").json()
    return user_data

