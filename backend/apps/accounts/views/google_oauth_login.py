from django.shortcuts import redirect
from django.urls import reverse

from rest_framework.views import APIView
from rest_framework import status

from drf_spectacular.utils import extend_schema

from apps.accounts.utils import google_setup
from apps.common.responses import CustomResponse
from apps.accounts.schema_examples import GOOGLE_RESPONSE_EXAMPLE
from .accounts import tags


class GoogleOAuth2LoginView(APIView):
    serializer_class = None

    @extend_schema(
        summary="Google OAuth2 Login",
        description="This endpoint is the login URL for Google OAuth2. It returns an authorization URL that should be used to redirect the user to Google.",
        tags=tags,
        responses=GOOGLE_RESPONSE_EXAMPLE,
        auth=[],
    )
    def get(self, request):
        # The redirect_uri should match the settings shown on the GCP OAuth config page.
        # The call to build_absolute_uri returns the full URL including domain.
        redirect_uri = request.build_absolute_uri(reverse("google_login_callback"))

        authorization_url = google_setup(redirect_uri)
        # return redirect(authorization_url[0])

        return CustomResponse.success(
            message="Authorization URL generated successfully",
            data={
                "authorization_url": authorization_url[0],
            },
            status_code=status.HTTP_200_OK,
        )
