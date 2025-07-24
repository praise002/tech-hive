import logging

from apps.accounts.emails import SendEmail
from apps.accounts.models import Otp, User
from apps.accounts.permissions import IsUnauthenticated
from apps.accounts.schema_examples import (
    AVATAR_UPDATE_RESPONSE_EXAMPLE,
    LOGIN_RESPONSE_EXAMPLE,
    LOGOUT_ALL_RESPONSE_EXAMPLE,
    LOGOUT_RESPONSE_EXAMPLE,
    PASSWORD_CHANGE_RESPONSE_EXAMPLE,
    PASSWORD_RESET_DONE_RESPONSE_EXAMPLE,
    PASSWORD_RESET_REQUEST_RESPONSE_EXAMPLE,
    PROFILE_RETRIEVE_RESPONSE_EXAMPLE,
    PROFILE_UPDATE_RESPONSE_EXAMPLE,
    REFRESH_TOKEN_RESPONSE_EXAMPLE,
    REGISTER_RESPONSE_EXAMPLE,
    RESEND_VERIFICATION_EMAIL_RESPONSE_EXAMPLE,
    VERIFY_EMAIL_RESPONSE_EXAMPLE,
    VERIFY_OTP_RESPONSE_EXAMPLE,
    build_avatar_request_schema,
)
from apps.accounts.serializers import (
    AvatarSerializer,
    CustomTokenObtainPairSerializer,
    PasswordChangeSerializer,
    RegisterSerializer,
    RequestPasswordResetOtpSerializer,
    SendOtpSerializer,
    SetNewPasswordSerializer,
    UserSerializer,
    VerifyOtpSerializer,
)
from apps.accounts.utils import invalidate_previous_otps
from apps.common.errors import ErrorCode
from apps.common.responses import CustomResponse
from django.conf import settings
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
)

logger = logging.getLogger(__name__)


tags = ["Auth"]


class RegisterView(APIView):
    serializer_class = RegisterSerializer
    permission_classes = (IsUnauthenticated,)

    @extend_schema(
        summary="Register a new user",
        description="This endpoint registers new users into our application",
        tags=tags,
        responses=REGISTER_RESPONSE_EXAMPLE,
        auth=[],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializer.validated_data

        # Send OTP for email verification
        SendEmail.send_email(request, user)

        return CustomResponse.success(
            message="OTP sent for email verification.",
            data={"email": data["email"]},
            status_code=status.HTTP_201_CREATED,
        )


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @extend_schema(
        summary="Login a user",
        description="This endpoint generates new access and refresh tokens for authentication",
        responses=LOGIN_RESPONSE_EXAMPLE,
        tags=tags,
        auth=[],
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)

            user = User.objects.get(email=request.data.get("email"))
            # Check if the user's email is verified
            if not user.is_email_verified:
                # If email is not verified, prompt them to request an OTP

                return CustomResponse.error(
                    message="Email not verified. Please verify your email before logging in.",
                    status_code=status.HTTP_403_FORBIDDEN,
                    err_code=ErrorCode.FORBIDDEN,
                )

            if not user.user_active:
                return CustomResponse.error(
                    message="Your account has been disabled. Please contact support for assistance.",
                    status_code=status.HTTP_403_FORBIDDEN,
                    err_code=ErrorCode.FORBIDDEN,
                )

        except TokenError as e:
            raise InvalidToken(e.args[0])

        if settings.DEBUG:
            response = CustomResponse.success(
                message="Login successful.",
                data=serializer.validated_data,
                status_code=status.HTTP_200_OK,
            )
        else:
            # Extract the refresh token from the response
            refresh = serializer.validated_data["refresh"]
            access = serializer.validated_data["access"]

            # Set the refresh token as an HTTP-only cookie
            response = CustomResponse.success(
                message="Login successful.",
                data={
                    "access": access,
                },
                status_code=status.HTTP_200_OK,
            )
            response.set_cookie(
                key="refresh",
                value=refresh,
                httponly=True,  # Prevent JavaScript access
                secure=True,  # Only send over HTTPS
                samesite="None",  # Allow cross-origin requests if frontend and backend are on different domains
            )

        return response


class ResendVerificationEmailView(APIView):
    serializer_class = SendOtpSerializer
    permission_classes = (IsUnauthenticated,)

    @extend_schema(
        summary="Send OTP to a user's email",
        description="This endpoint sends OTP to a user's email for verification",
        responses=RESEND_VERIFICATION_EMAIL_RESPONSE_EXAMPLE,
        tags=tags,
        auth=[],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return CustomResponse.error(
                message="No account is associated with this email.",
                err_code=ErrorCode.VALIDATION_ERROR,
            )

        if user.is_email_verified:
            return CustomResponse.success(
                message="Your email is already verified. No OTP sent.",
                status_code=status.HTTP_200_OK,
            )

        # Invalidate/clear any previous OTPs
        invalidate_previous_otps(user)

        # Send OTP to user's email
        SendEmail.send_email(request, user)

        return CustomResponse.success(
            message="OTP sent successfully.",
            status_code=status.HTTP_200_OK,
        )


class VerifyEmailView(APIView):
    serializer_class = VerifyOtpSerializer
    permission_classes = (IsUnauthenticated,)

    @extend_schema(
        summary="Verify a user's email",
        description="This endpoint verifies a user's email",
        responses=VERIFY_EMAIL_RESPONSE_EXAMPLE,
        tags=tags,
        auth=[],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return CustomResponse.error(
                message="No account is associated with this email.",
                err_code=ErrorCode.VALIDATION_ERROR,
            )

        # Check if the OTP is valid for this user
        try:
            otp_record = Otp.objects.get(user=user, otp=otp)
        except Otp.DoesNotExist:
            return CustomResponse.error(
                message="Invalid OTP provided.",
                err_code=ErrorCode.VALIDATION_ERROR,
            )

        # Check if OTP is expired
        if not otp_record.is_valid:
            return CustomResponse.error(
                message="OTP has expired, please request a new one.",
                status_code=498,
                err_code=ErrorCode.EXPIRED,
            )

        # Check if user is already verified
        if user.is_email_verified:
            # Clear the OTP
            invalidate_previous_otps(user)
            return CustomResponse.success(
                message="Email address already verified. No OTP sent.",
                status_code=status.HTTP_200_OK,
            )

        user.is_email_verified = True
        user.save()

        # Clear OTP after verification
        invalidate_previous_otps(user)

        SendEmail.welcome(request, user)

        return CustomResponse.success(
            message="Email verified successfully.",
            status_code=status.HTTP_200_OK,
        )


class LogoutView(TokenBlacklistView):
    @extend_schema(
        summary="Logout a user",
        description="This endpoint logs a user out from our application",
        responses=LOGOUT_RESPONSE_EXAMPLE,
        tags=tags,
        auth=[],
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        if settings.DEBUG:
            response = CustomResponse.success(
                message="Logged out successfully.", status_code=status.HTTP_200_OK
            )
        else:
            # Clear the HTTP-only cookie containing the refresh token
            response.delete_cookie("refresh")
        return response


class LogoutAllView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None

    @extend_schema(
        summary="Logout from all devices",
        description="Blacklists all refresh tokens for the user",
        tags=tags,
        responses=LOGOUT_ALL_RESPONSE_EXAMPLE,
    )
    def post(self, request):
        try:
            # Get all valid tokens for the user
            tokens = OutstandingToken.objects.filter(
                user=request.user, expires_at__gt=timezone.now(), blacklistedtoken=None
            )

            # Blacklist all tokens
            for token in tokens:
                RefreshToken(token.token).blacklist()

            return CustomResponse.success(
                message="Successfully logged out from all devices.",
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
            return CustomResponse.error(
                message="Error during logout",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                err_code=ErrorCode.SERVER_ERROR,
            )


class PasswordChangeView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordChangeSerializer

    @extend_schema(
        summary="Change user password",
        description="This endpoint allows authenticated users to update their account password. The user must provide their current password for verification along with the new password they wish to set. If successful, the password will be updated, and a response will confirm the change.",
        responses=PASSWORD_CHANGE_RESPONSE_EXAMPLE,
        tags=tags,
    )
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.success(
            message="Password changed successfully.", status_code=status.HTTP_200_OK
        )


class PasswordResetRequestView(APIView):
    permission_classes = (IsUnauthenticated,)
    serializer_class = RequestPasswordResetOtpSerializer

    @extend_schema(
        summary="Send Password Reset Otp",
        description="This endpoint sends new password reset otp to the user's email",
        responses=PASSWORD_RESET_REQUEST_RESPONSE_EXAMPLE,
        tags=tags,
        auth=[],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return CustomResponse.error(
                message="User with this email does not exist.",
                err_code=ErrorCode.VALIDATION_ERROR,
            )

        # Clear otps if another otp is requested
        invalidate_previous_otps(user)

        # Send OTP to user's email
        SendEmail.send_password_reset_email(request, user)

        return CustomResponse.success(
            message="OTP sent successfully.", status_code=status.HTTP_200_OK
        )


class VerifyOtpView(APIView):
    permission_classes = (IsUnauthenticated,)
    serializer_class = VerifyOtpSerializer

    @extend_schema(
        summary="Verify password reset otp",
        description="This endpoint verifies the password reset OTP.",
        responses=VERIFY_OTP_RESPONSE_EXAMPLE,
        tags=tags,
        auth=[],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return CustomResponse.error(
                message="No account is associated with this email.",
                err_code=ErrorCode.VALIDATION_ERROR,
            )

        # Check if the OTP is valid for this user
        try:
            otp_record = Otp.objects.get(user=user, otp=otp)
        except Otp.DoesNotExist:
            return CustomResponse.error(
                message="The OTP could not be found. Please enter a valid OTP or request a new one.",
                err_code=ErrorCode.VALIDATION_ERROR,
            )

        # Check if OTP is expired
        if not otp_record.is_valid:
            return CustomResponse.error(
                message="OTP has expired, please request a new one.",
                status_code=498,
                err_code=ErrorCode.EXPIRED,
            )

        # Clear OTP after verification
        invalidate_previous_otps(user)

        return CustomResponse.success(
            message="OTP verified, proceed to set a new password.",
            status_code=status.HTTP_200_OK,
        )


class PasswordResetDoneView(APIView):
    permission_classes = (IsUnauthenticated,)
    serializer_class = SetNewPasswordSerializer

    @extend_schema(
        summary="Set New Password",
        description="This endpoint sets a new password if the OTP is valid.",
        responses=PASSWORD_RESET_DONE_RESPONSE_EXAMPLE,
        tags=tags,
        auth=[],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        new_password = serializer.validated_data["new_password"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return CustomResponse.error(
                message="No account is associated with this email.",
                err_code=ErrorCode.VALIDATION_ERROR,
            )

        # Update the user's password
        user.set_password(new_password)
        user.save()

        SendEmail.password_reset_success(request, user)

        return CustomResponse.success(
            message="Your password has been reset, proceed to login.",
            status_code=status.HTTP_200_OK,
        )


class RefreshTokensView(TokenRefreshView):

    @extend_schema(
        summary="Refresh user access token",
        description="This endpoint allows users to refresh their access token using a valid refresh token. It returns a new access token, which can be used for further authenticated requests.",
        tags=tags,
        responses=REFRESH_TOKEN_RESPONSE_EXAMPLE,
        auth=[],
    )
    def post(self, request, *args, **kwargs):
        """
        Handle POST request to refresh the JWT token
        """
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        if settings.DEBUG:
            response = CustomResponse.success(
                message="Token refreshed successfully.",
                data=serializer.validated_data,
                status_code=status.HTTP_200_OK,
            )
        else:
            # Extract the new refresh token from the response
            refresh = serializer.validated_data["refresh"]
            access = serializer.validated_data("access")

            # Set the new refresh token as an HTTP-only cookie
            response = CustomResponse.success(
                message="Token refreshed successfully.",
                data={"access": access},
                status_code=status.HTTP_200_OK,
            )

            response.set_cookie(
                key="refresh",
                value=refresh,
                httponly=True,  # Prevent JavaScript access
                secure=True,  # Only send over HTTPS
                samesite="None",  # Allow cross-origin requests if frontend and backend are on different domains
            )

        return response


class ProfileView(APIView):
    """
    View to retrieve the authenticated user's profile.
    """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="View a user profile",
        description="This endpoint allows authenticated users to view their profile details. Users can retrieve their account information. Only the account owner can access their profile.",
        tags=tags,
        responses=PROFILE_RETRIEVE_RESPONSE_EXAMPLE,
    )
    def get(self, request):
        profile = request.user.profile
        serializer = self.serializer_class(profile)
        return CustomResponse.success(
            message="Profile retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Update user profile",
        description="This endpoint allows authenticated users to edit their profile details. Users can update their personal information. Only the account owner can modify their profile.",
        tags=tags,
        responses=PROFILE_UPDATE_RESPONSE_EXAMPLE,
    )
    def patch(self, request):
        profile = request.user.profile
        serializer = self.serializer_class(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()

        return CustomResponse.success(
            message="Profile updated successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


class ProfileViewGeneric(RetrieveUpdateAPIView):
    """
    View to retrieve and update the authenticated user's profile.
    """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = [
        "get",
        "patch",
        "head",
        "options",
    ]  # to remove the put method inherited from RetrieveUpdate

    def get_object(self):
        """
        Return the profile of the authenticated user.
        """
        return self.request.user.profile

    @extend_schema(
        summary="View a user profile",
        description="This endpoint allows authenticated users to view their profile details. Users can retrieve their account information. Only the account owner can access their profile.",
        tags=tags,
        responses=PROFILE_RETRIEVE_RESPONSE_EXAMPLE,
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieve the authenticated user's profile.
        """
        return self.retrieve(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse.success(
            message="Profile retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Update user profile",
        description="This endpoint allows authenticated users to edit their profile details. Users can update their personal information. Only the account owner can modify their profile.",
        tags=tags,
        responses=PROFILE_UPDATE_RESPONSE_EXAMPLE,
    )
    def patch(self, request, *args, **kwargs):
        """
        Partially update the authenticated user's profile.
        """
        return self.partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Override the update method to customize the response format.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return CustomResponse.success(
            message="Profile updated successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


class AvatarUpdateView(APIView):
    serializer_class = AvatarSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Update user avatar",
        description="This endpoint allows authenticated users to upload or update their profile avatar.",
        tags=tags,
        request=build_avatar_request_schema(),
        responses=AVATAR_UPDATE_RESPONSE_EXAMPLE,
    )
    def patch(self, request):
        profile = request.user.profile
        serializer = self.serializer_class(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()

        return CustomResponse.success(
            message="Profile avatar updated successfully.",
            data={
                "avatar_url": profile.avatar_url,
            },
            status_code=status.HTTP_200_OK,
        )
