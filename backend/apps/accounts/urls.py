from django.urls import path

from . import views



urlpatterns = [
    # Authentication
    path("register/", views.RegisterView.as_view()),
    path("token/", views.LoginView.as_view()),
    path("token/refresh/", views.RefreshTokensView.as_view()),
    
    # Sessions (for logout)
    path("sessions/", views.LogoutView.as_view()),
    path("sessions/all/", views.LogoutAllView.as_view()),
    
    # Verification
    path("verification/", views.ResendVerificationEmailView.as_view()),
    path("verification/verify/", views.VerifyEmailView.as_view()),
    
    # Password management
    path("passwords/change/", views.PasswordChangeView.as_view()),
    path("passwords/reset/", views.PasswordResetRequestView.as_view()),
    path("passwords/reset/verify/", views.VerifyOtpView.as_view()),
    path("passwords/reset/complete/", views.PasswordResetDoneView.as_view()),
    
    # Oauth
    path(
        "signup/google/", views.GoogleOAuth2SignUpView.as_view(), name="google_signup"
    ),
    path(
        "google/callback/signup",
        views.GoogleOAuth2SignUpCallbackView.as_view(),
        name="google_signup_callback",
    ),
    path("login/google/", views.GoogleOAuth2LoginView.as_view(), name="google_login"),
    path(
        "google/callback/login",
        views.GoogleOAuth2LoginCallbackView.as_view(),
        name="google_login_callback",
    ),
]
