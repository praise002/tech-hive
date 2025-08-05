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
    SUCCESS_RESPONSE_STATUS,
    UUID_EXAMPLE,
)
from apps.common.serializers import ErrorDataResponseSerializer, ErrorResponseSerializer
from drf_spectacular.utils import OpenApiExample, OpenApiResponse

PROFILE_EXAMPLE = {
    "id": UUID_EXAMPLE,
    "first_name": "Bob",
    "last_name": "Joe",
    "email": EMAIL_EXAMPLE,
    "updated_at": DATETIME_EXAMPLE,
    "avatar_url": AVATAR_URL,
}
REGISTER_EXAMPLE = {"email": "bob123@example.com"}

LOGIN_EXAMPLE = {
    # "refresh": REFRESH_TOKEN,
    "access": ACCESS_TOKEN,
}

REFRESH_TOKEN_EXAMPLE = {
    "access": ACCESS_TOKEN,
    # "refresh": REFRESH_TOKEN,
}

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
    403: ErrorDataResponseSerializer,
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
        response=ErrorDataResponseSerializer,
        description="Validation Error",
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
        ],
    ),
    422: OpenApiResponse(
        response=ErrorDataResponseSerializer,
        description="Validation Error",
    ),
    498: OpenApiResponse(
        response=VerifyOtpSerializer,
        description="OTP Expired",
        examples=[
            OpenApiExample(
                name="OTP Expired",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "OTP has expired, please request a new one.",
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
        description="Unauthorized User or Invalid Refresh Token",
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
}

PASSWORD_CHANGE_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        response=PasswordChangeSerializer,
        description="Password Change Successful",
        examples=[
            OpenApiExample(
                name="Password Change Successful",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Password changed successfully.",
                },
            ),
        ],
    ),
    401: UNAUTHORIZED_USER_RESPONSE,
    422: OpenApiResponse(
        response=ErrorDataResponseSerializer,
        description="Validation Error",
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
                    "message": "OTP sent successfully.",
                },
            ),
        ],
    ),
    422: OpenApiResponse(
        response=ErrorDataResponseSerializer,
        description="Validation Error",
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
                    "message": "OTP verified, proceed to set new password.",
                },
            ),
        ],
    ),
    422: OpenApiResponse(
        response=ErrorDataResponseSerializer,
        description="Validation Error",
    ),
    498: OpenApiResponse(
        response=VerifyOtpSerializer,
        description="OTP Expired",
        examples=[
            OpenApiExample(
                name="OTP Expired",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "OTP has expired, please request a new one.",
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
    ),
}

REFRESH_TOKEN_RESPONSE_EXAMPLE = {
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
        description="Unauthorized User or Invalid Refresh Token",
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
