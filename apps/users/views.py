# apps/users/views.py
"""
Views for the users app.
"""

# Python modules
from typing import Any

# Django REST Framework
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.utils import extend_schema, OpenApiResponse

# Project modules
from apps.users.serializers import LoginSerializer, RegisterSerializer


@extend_schema(
    summary="User Registration",
    description="Register a new user account with email, username, password, and avatar.",
    request={
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "email": {"type": "string", "format": "email"},
                "username": {"type": "string"},
                "password": {"type": "string"},
                "first_name": {"type": "string"},
                "last_name": {"type": "string"},
                "avatar": {"type": "string", "format": "binary"},
            },
            "required": ["email", "username", "password", "avatar"],
        }
    },
    responses={
        201: OpenApiResponse(
            description="User registered successfully.",
        ),
        400: OpenApiResponse(
            description="Invalid input data.",
        ),
    },
)
class RegisterView(generics.CreateAPIView):
    """
    View for user registration.
    """

    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    parser_classes = [MultiPartParser, FormParser]


@extend_schema(
    summary="User Login",
    description="Authenticate user and return JWT tokens.",
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(
            description="Successful login returns access and refresh tokens.",
            response={
                "type": "object",
                "properties": {
                    "refresh": {"type": "string"},
                    "access": {"type": "string"},
                },
            },
        ),
        400: OpenApiResponse(
            description="Invalid credentials or missing data.",
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
        self,
        request: DRFRequest,
        *args: Any,
        **kwargs: dict[str, Any]
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