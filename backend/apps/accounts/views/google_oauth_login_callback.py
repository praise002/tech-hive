from apps.accounts.models import User
from apps.accounts.utils import google_callback
from apps.common.errors import ErrorCode
from apps.common.responses import CustomResponse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from drf_spectacular.utils import extend_schema

# from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


@extend_schema(exclude=True)
class GoogleOAuth2LoginCallbackView(APIView):

    def get(self, request):
        redirect_uri = request.build_absolute_uri(reverse("google_login_callback"))

        auth_uri = request.build_absolute_uri()

        state = request.query_params.get("state")

        user_data = google_callback(redirect_uri, auth_uri, state)

        try:
            user = User.objects.get(email=user_data["email"])
        except User.DoesNotExist:
            return CustomResponse.error(
                message="No account is associated with this email.",
                err_code=ErrorCode.VALIDATION_ERROR,
            )

        # Create the jwt token for the frontend to use.
        refresh = RefreshToken.for_user(user)

        access = str(refresh.access_token)
        refresh = str(refresh)

        frontend_callback_url = settings.FRONTEND_LOGIN_CALLBACK_URL
        redirect_url = (
            f"{frontend_callback_url}" f"?access={access}" f"&refresh={refresh}"
        )

        return HttpResponseRedirect(redirect_url)

        # return CustomResponse.success(
        #     message="Login successful.",
        #     data={
        #         "refresh": refresh,
        #         "access": access_token,
        #     },
        #     status_code=status.HTTP_200_OK,
        # )
