"""
Views for the users app.
"""

# Python modules
from typing import Any

from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework_simplejwt.views import TokenRefreshView

from django.utils.translation import gettext_lazy as _

# Django REST Framework
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse

# Project modules
from apps.users.serializers import LoginSerializer, RegisterSerializer


@extend_schema(
    summary="User Registration",
    description="Register a new user account with email, username, and password. Avatar is optional.",
    request={
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "email": {"type": "string", "format": "email"},
                "username": {"type": "string"},
                "password": {"type": "string"},
                "first_name": {"type": "string"},
                "last_name": {"type": "string"},
                "avatar": {"type": "string", "format": "binary", "description": "Optional avatar image (max 2MB)"},
            },
            "required": ["email", "username", "password"],
        }
    },
    responses={
        201: OpenApiResponse(
            description=_("User registered successfully."),
        ),
        400: OpenApiResponse(
            description=_("Invalid input data."),
        ),
    },
)
class RegisterView(generics.CreateAPIView):
    """
    View for user registration.
    
    Creates a new user account. Avatar is optional - users can register
    without uploading an avatar and add it later.
    """

    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    parser_classes = [MultiPartParser, FormParser]


@extend_schema(
    summary=_("User Login"),
    description=_("Authenticate user and return JWT tokens."),
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(
            description=_("Successful login returns access and refresh tokens."),
            response={
                "type": "object",
                "properties": {
                    "refresh": {"type": "string"},
                    "access": {"type": "string"},
                },
            },
        ),
        400: OpenApiResponse(
            description=_("Invalid credentials or missing data."),
        ),
    },
)
class LoginView(GenericAPIView):
    """
    View for user login.
    """

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(
        self, request: DRFRequest, *args: Any, **kwargs: dict[str, Any]
    ) -> DRFResponse:
        """
        Handle POST request for user login.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return DRFResponse(serializer.validated_data, status=status.HTTP_200_OK)


class RefreshView(TokenRefreshView):
    """
    View for refreshing JWT tokens.
    """

    permission_classes = [AllowAny]
