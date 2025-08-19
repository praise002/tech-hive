from apps.accounts.serializers import (
    CustomTokenObtainPairSerializer,
    PasswordChangeSerializer,
    RefreshTokenResponseSerializer,
    RegisterSerializer,
    RequestPasswordResetOtpSerializer,
    SendOtpSerializer,
    SetNewPasswordSerializer,
    UserSerializer,
    VerifyOtpSerializer,
)
from apps.common.errors import ErrorCode
from apps.common.schema_examples import (
    ACCESS_TOKEN,
    AVATAR_URL,
    DATETIME_EXAMPLE,
    EMAIL_EXAMPLE,
    ERR_RESPONSE_STATUS,
    REFRESH_TOKEN,
    SUCCESS_RESPONSE_STATUS,
    UUID_EXAMPLE,
)
from apps.common.serializers import (
    ErrorDataResponseSerializer,
    ErrorResponseSerializer,
    SuccessResponseSerializer,
)
from django.conf import settings
from drf_spectacular.utils import OpenApiExample, OpenApiResponse

PROFILE_EXAMPLE = {
    "id": UUID_EXAMPLE,
    "first_name": "Bob",
    "last_name": "Joe",
    "username": "bob-joe",
    "email": EMAIL_EXAMPLE,
    "updated_at": DATETIME_EXAMPLE,
    "avatar_url": AVATAR_URL,
}
REGISTER_EXAMPLE = {"email": "bob123@example.com"}


if settings.DEBUG:
    LOGIN_EXAMPLE = {
        "access": ACCESS_TOKEN,
    }
    PASSWORD_CHANGE_EXAMPLE = {
        "access": ACCESS_TOKEN,
    }
    REFRESH_TOKEN_EXAMPLE = {
        "access": ACCESS_TOKEN,
    }
else:
    LOGIN_EXAMPLE = {
        "refresh": REFRESH_TOKEN,
        "access": ACCESS_TOKEN,
    }
    PASSWORD_CHANGE_EXAMPLE = {
        "refresh": REFRESH_TOKEN,
        "access": ACCESS_TOKEN,
    }
    REFRESH_TOKEN_EXAMPLE = {
        "access": ACCESS_TOKEN,
        "refresh": REFRESH_TOKEN,
    }


GOOGLE_OAUTH_EXAMPLE = {"authorization_url": ""}


UNAUTHORIZED_USER_RESPONSE = OpenApiResponse(
    response=ErrorResponseSerializer,
    description="Unauthorized User or Invalid Access Token",
    examples=[
        OpenApiExample(
            name="Unauthorized User",
            value={
                "status": ERR_RESPONSE_STATUS,
                "message": "Authentication credentials were not provided.",
                "err_code": ErrorCode.UNAUTHORIZED,
            },
        ),
        OpenApiExample(
            name="Invalid Access Token",
            value={
                "status": ERR_RESPONSE_STATUS,
                "message": "Token is Invalid or Expired.",
                "err_code": ErrorCode.INVALID_TOKEN,
            },
        ),
    ],
)

GOOGLE_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        response=SuccessResponseSerializer,
        description="Authorization URL Successful",
        examples=[
            OpenApiExample(
                name="Authorization URL Successful",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Authorization URL generated successfully.",
                    "data": GOOGLE_OAUTH_EXAMPLE,
                },
            ),
        ],
    ),
}

REGISTER_RESPONSE_EXAMPLE = {
    201: OpenApiResponse(
        response=RegisterSerializer,
        description="OTP Sent Successful",
        examples=[
            OpenApiExample(
                name="OTP Sent Successful",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "OTP sent for email verification.",
                    "data": REGISTER_EXAMPLE,
                },
            ),
        ],
    ),
    422: OpenApiResponse(
        response=ErrorDataResponseSerializer,
        description="Validation Error",
    ),
}

LOGIN_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        response=CustomTokenObtainPairSerializer,
        description="Login Successful",
        examples=[
            OpenApiExample(
                name="Login Successful",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Login successful.",
                    "data": LOGIN_EXAMPLE,
                },
            ),
        ],
    ),
    401: OpenApiResponse(
        response=CustomTokenObtainPairSerializer,
        description="Unauthorized",
        examples=[
            OpenApiExample(
                name="Unauthorized",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "No active account found with the given credentials.",
                    "code": ErrorCode.UNAUTHORIZED,
                },
            ),
        ],
    ),
    403: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Permission Denied",
        examples=[
            OpenApiExample(
                name="Email not verified",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Email not verified. Please verify your email before logging in.",
                    "code": ErrorCode.FORBIDDEN,
                },
            ),
            OpenApiExample(
                name="Account disabled",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Your account has been disabled. Please contact support for assistance.",
                    "code": ErrorCode.FORBIDDEN,
                },
            ),
        ],
    ),
    422: OpenApiResponse(
        response=ErrorDataResponseSerializer,
        description="Validation Error",
    ),
}

RESEND_VERIFICATION_EMAIL_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        response=SendOtpSerializer,
        description="OTP Resent Successful",
        examples=[
            OpenApiExample(
                name="OTP Resent Successful",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "OTP sent successfully.",
                },
            ),
            OpenApiExample(
                name="Email already verified",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Your email is already verified. No OTP sent.",
                },
            ),
        ],
    ),
    422: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Validation Error",
        examples=[
            OpenApiExample(
                name="No account found",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "No account is associated with this email.",
                    "code": ErrorCode.VALIDATION_ERROR,
                },
            ),
            OpenApiExample(
                name="Field Validation Error",
                value={
                    "status": "failure",
                    "message": "Validation error",
                    "code": "validation_error",
                    "data": {"email": "This field is required."},
                },
            ),
        ],
    ),
}

VERIFY_EMAIL_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        response=VerifyOtpSerializer,
        description="Email Verification Successful",
        examples=[
            OpenApiExample(
                name="Email Verification Successful",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Email verified successfully.",
                },
            ),
            OpenApiExample(
                name="Email already verified",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Email address already verified. No OTP sent.",
                },
            ),
        ],
    ),
    422: OpenApiResponse(
        response=ErrorDataResponseSerializer,
        description="Validation Error",
        examples=[
            OpenApiExample(
                name="No account found",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "No account is associated with this email.",
                    "code": ErrorCode.VALIDATION_ERROR,
                },
            ),
            OpenApiExample(
                name="Invalid OTP",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Invalid or expired OTP. Please enter a valid OTP or request a new one.",
                    "code": ErrorCode.VALIDATION_ERROR,
                },
            ),
            OpenApiExample(
                name="Field Validation Error",
                value={
                    "status": "failure",
                    "message": "Validation error",
                    "code": "validation_error",
                    "data": {"otp": "This field is required."},
                },
            ),
        ],
    ),
}

LOGOUT_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        response=PasswordChangeSerializer,
        description="Logout Successful",
        examples=[
            OpenApiExample(
                name="Logout Successful",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Logged out successfully.",
                },
            ),
        ],
    ),
    401: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Invalid Refresh Token",
        examples=[
            OpenApiExample(
                name="Invalid Refresh Token",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Token is Invalid or Expired.",
                    "err_code": ErrorCode.INVALID_TOKEN,
                },
            ),
        ],
    ),
    422: OpenApiResponse(
        response=ErrorDataResponseSerializer,
        description="Validation Error",
    ),
}

LOGOUT_ALL_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        response=PasswordChangeSerializer,
        description="Logout Successful",
        examples=[
            OpenApiExample(
                name="Logout Successful",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Successfully logged out from all devices.",
                },
            ),
        ],
    ),
    401: ErrorResponseSerializer,
    500: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Internal Server Error",
        examples=[
            OpenApiExample(
                name="Logout Error",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Error during logout",
                    "code": ErrorCode.SERVER_ERROR,
                },
            ),
        ],
    ),
}

PASSWORD_CHANGE_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        response=PasswordChangeSerializer,
        description="Password Change Successful",
        examples=[
            OpenApiExample(
                name="Password Change Successful (Production)",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Password changed successfully.",
                    "data": PASSWORD_CHANGE_EXAMPLE,
                },
            ),
            OpenApiExample(
                name="Password Change Successful (Debug)",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Password changed successfully.",
                    "data": PASSWORD_CHANGE_EXAMPLE,
                },
            ),
        ],
    ),
    401: UNAUTHORIZED_USER_RESPONSE,
    422: OpenApiResponse(
        response=ErrorDataResponseSerializer,
        description="Validation Error",
        examples=[
            OpenApiExample(
                name="Password mismatch",
                value={
                    "status": "error",
                    "message": "Some fields are invalid.",
                    "code": "validation_error",
                    "data": {
                        "error": ["New password and confirm password do not match."]
                    },
                },
            ),
            OpenApiExample(
                name="Incorrect old password",
                value={
                    "status": "error",
                    "message": "Some fields are invalid.",
                    "code": "validation_error",
                    "data": {
                        "error": [
                            "The current password you entered is incorrect. Please try again."
                        ]
                    },
                },
            ),
        ],
    ),
}

PASSWORD_RESET_REQUEST_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        response=RequestPasswordResetOtpSerializer,
        description="Password Reset Request Successful",
        examples=[
            OpenApiExample(
                name="Password Reset Request Successful",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "If that email address is in our database, we will send you an email to reset your password.",
                },
            ),
        ],
    ),
    422: OpenApiResponse(
        response=ErrorDataResponseSerializer,
        description="Validation Error",
        examples=[
            OpenApiExample(
                name="Field Validation Error",
                value={
                    "status": "error",
                    "message": "Some fields are invalid.",
                    "code": "validation_error",
                    "data": {"email": ["This field is required."]},
                },
            ),
        ],
    ),
}

VERIFY_OTP_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        response=VerifyOtpSerializer,
        description="OTP Verification Successful",
        examples=[
            OpenApiExample(
                name="OTP Verification Successful",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "OTP verified, proceed to set a new password.",
                },
            ),
        ],
    ),
    422: OpenApiResponse(
        response=ErrorDataResponseSerializer,
        description="Validation Error",
        examples=[
            OpenApiExample(
                name="No account found",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "No account is associated with this email.",
                    "code": ErrorCode.VALIDATION_ERROR,
                },
            ),
            OpenApiExample(
                name="Invalid OTP",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Invalid or expired OTP. Please enter a valid OTP or request a new one.",
                    "code": ErrorCode.VALIDATION_ERROR,
                },
            ),
            OpenApiExample(
                name="Field Validation Error",
                value={
                    "status": "failure",
                    "message": "Validation error",
                    "code": "validation_error",
                    "data": {"otp": "This field is required."},
                },
            ),
        ],
    ),
}

PASSWORD_RESET_DONE_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        response=SetNewPasswordSerializer,
        description="Password Reset Successful",
        examples=[
            OpenApiExample(
                name="Password Reset Successful",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Your password has been reset, proceed to login.",
                },
            ),
        ],
    ),
    422: OpenApiResponse(
        response=ErrorDataResponseSerializer,
        description="Validation Error",
        examples=[
            OpenApiExample(
                name="No account found",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "No account is associated with this email.",
                    "code": ErrorCode.VALIDATION_ERROR,
                },
            ),
            OpenApiExample(
                name="Password mismatch",
                value={
                    "status": "failure",
                    "message": "Validation error",
                    "code": "validation_error",
                    "data": {
                        "error": "New password and confirm password do not match."
                    },
                },
            ),
            OpenApiExample(
                name="Field Validation Error",
                value={
                    "status": "failure",
                    "message": "Validation error",
                    "code": "validation_error",
                    "data": {
                        "email": "This field may not be blank.",
                        "new_password": "This password is too short. It must contain at least 8 characters.",
                    },
                },
            ),
        ],
    ),
}

REFRESH_TOKEN_RESPONSE_EXAMPLE = {
    # 200: RefreshTokenResponseSerializer,
    # 401: ErrorResponseSerializer,
    # 422: ErrorDataResponseSerializer,
    200: OpenApiResponse(
        response=RefreshTokenResponseSerializer,
        description="Refresh Token Successful",
        examples=[
            OpenApiExample(
                name="Refresh Token Successful",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Token refreshed successfully.",
                    "data": REFRESH_TOKEN_EXAMPLE,
                },
            ),
        ],
    ),
    401: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Invalid Refresh Token",
        examples=[
            OpenApiExample(
                name="Invalid Refresh Token",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Token is Invalid or Expired.",
                    "err_code": ErrorCode.INVALID_TOKEN,
                },
            ),
        ],
    ),
    422: OpenApiResponse(
        response=ErrorDataResponseSerializer,
        description="Validation Error",
    ),
}


PROFILE_UPDATE_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        response=UserSerializer,
        description="Profile Update Successful",
        examples=[
            OpenApiExample(
                name="Profile Update Successful",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Profile updated successfully.",
                    "data": PROFILE_EXAMPLE,
                },
            ),
        ],
    ),
    401: UNAUTHORIZED_USER_RESPONSE,
    422: ErrorDataResponseSerializer,
}

PROFILE_RETRIEVE_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        description="Profile Retrieve Successful",
        response=UserSerializer,
        examples=[
            OpenApiExample(
                name="Success Response",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Profile retrieved successfully.",
                    "data": PROFILE_EXAMPLE,
                },
            ),
        ],
    ),
    401: UNAUTHORIZED_USER_RESPONSE,
}

PROFILE_DETAIL_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        description="Profile Retrieve Successful",
        response=UserSerializer,
        examples=[
            OpenApiExample(
                name="Success Response",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Profile retrieved successfully.",
                    "data": PROFILE_EXAMPLE,
                },
            ),
        ],
    ),
    404: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Profile not found",
        examples=[
            OpenApiExample(
                name="Profile not found",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "User profile not found.",
                    "code": ErrorCode.NON_EXISTENT,
                },
            ),
        ],
    ),
}

AVATAR_UPDATE_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        description="Avatar Update Successful",
        response=UserSerializer,
        examples=[
            OpenApiExample(
                name="Success Response",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Profile avatar updated successfully.",
                    "data": {
                        "avatar_url": AVATAR_URL,
                    },
                },
            ),
        ],
    ),
    422: ErrorDataResponseSerializer,
    401: UNAUTHORIZED_USER_RESPONSE,
}


def build_avatar_request_schema():
    return {
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "avatar": {
                    "type": "string",
                    "format": "binary",
                    "description": "Profile image file",
                },
            },
            "required": ["avatar"],
        }
    }
