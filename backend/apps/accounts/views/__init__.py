from .accounts import (
    LoginView,
    LogoutAllView,
    LogoutView,
    PasswordChangeView,
    PasswordResetDoneView,
    PasswordResetRequestView,
    RefreshTokensView,
    RegisterView,
    ResendVerificationEmailView,
    VerifyEmailView,
    VerifyOtpView,
)
from .google_oauth_login import GoogleOAuth2LoginView
from .google_oauth_login_callback import GoogleOAuth2LoginCallbackView
from .google_oauth_signup import GoogleOAuth2SignUpView
from .google_oauth_signup_callback import GoogleOAuth2SignUpCallbackView

__all__ = [
    # Account views
    "RegisterView",
    "LoginView",
    "LogoutView",
    "LogoutAllView",
    "VerifyEmailView",
    "ResendVerificationEmailView",
    "PasswordChangeView",
    "PasswordResetRequestView",
    "VerifyOtpView",
    "PasswordResetDoneView",
    "RefreshTokensView",
    # OAuth views
    "GoogleOAuth2SignUpView",
    "GoogleOAuth2SignUpCallbackView",
    "GoogleOAuthSignUpCallbackView",
    "GoogleOAuth2LoginView",
    "GoogleOAuth2LoginCallbackView",
]
