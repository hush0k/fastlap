"""
ViewSet for user avatar management.
"""

# Python modules

# Django modules
from asgiref.sync import async_to_sync

from drf_spectacular.utils import OpenApiResponse, extend_schema

# Django REST Framework
from drf_spectacular.utils import OpenApiResponse, extend_schema

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse

# Project modules
from apps.users.services.firestore_service import FirestoreUserService
from apps.users.utils.avatar_utils import AvatarProcessor


@extend_schema(tags=["Auth"])
class AvatarViewSet(viewsets.GenericViewSet):
    """
    ViewSet for managing user avatars in Firestore.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Upload Avatar",
        description="Upload user avatar to Firestore.",
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "avatar": {
                        "type": "string",
                        "format": "binary",
                        "description": "Avatar image file (max 2MB)",
                    }
                },
                "required": ["avatar"],
            }
        },
        responses={
            200: OpenApiResponse(
                description="Avatar uploaded successfully.",
                response={
                    "type": "object",
                    "properties": {"message": {"type": "string"}},
                },
            ),
            400: OpenApiResponse(description="Invalid avatar file."),
            500: OpenApiResponse(description="Failed to upload avatar."),
        },
    )
    @action(detail=False, methods=["post"], url_path="upload")
    def upload_avatar(self, request: DRFRequest) -> DRFResponse:
        """
        Upload user avatar to Firestore.
        """
        avatar_file = request.FILES.get("avatar")

        if not avatar_file:
            return DRFResponse(
                {"error": "No avatar file provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        base64_avatar, error = AvatarProcessor.process_avatar(avatar_file)

        if error:
            return DRFResponse(
                {"error": error},
                status=status.HTTP_400_BAD_REQUEST,
            )

        firestore_service = FirestoreUserService()
        success: bool = async_to_sync(firestore_service.update_user_avatar)(
            request.user.id, base64_avatar
        )

        if success:
            request.user.use_firestore_avatar = True
            request.user.save(update_fields=["use_firestore_avatar"])
            return DRFResponse(
                {
                    "message": "Avatar uploaded successfully",
                    "avatar": base64_avatar,
                }
            )

        return DRFResponse(
            {"error": "Failed to upload avatar"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @extend_schema(
        summary="Get Avatar",
        description="Get user's current avatar from Firestore.",
        responses={
            200: OpenApiResponse(
                description="Avatar retrieved successfully.",
                response={
                    "type": "object",
                    "properties": {"avatar": {"type": "string"}},
                },
            ),
            404: OpenApiResponse(description="Avatar not found."),
        },
    )
    @action(detail=False, methods=["get"], url_path="")
    def get_avatar(self, request: DRFRequest) -> DRFResponse:
        """
        Get user's current avatar from Firestore.
        """
        firestore_service = FirestoreUserService()
        avatar_base64: str | None = async_to_sync(firestore_service.get_user_avatar)(
            request.user.id
        )

        if avatar_base64:
            return DRFResponse({"avatar": avatar_base64})

        return DRFResponse(
            {"error": "Avatar not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    @extend_schema(
        summary="Delete Avatar",
        description="Delete user's avatar from Firestore.",
        responses={
            200: OpenApiResponse(
                description="Avatar deleted successfully.",
                response={
                    "type": "object",
                    "properties": {"message": {"type": "string"}},
                },
            ),
            500: OpenApiResponse(description="Failed to delete avatar."),
        },
    )
    @action(detail=False, methods=["delete"], url_path="")
    def delete_avatar(self, request: DRFRequest) -> DRFResponse:
        """
        Delete user's avatar from Firestore.
        """
        firestore_service = FirestoreUserService()
        success: bool = async_to_sync(firestore_service.delete_user_avatar)(
            request.user.id
        )

        if success:
            request.user.use_firestore_avatar = False
            request.user.firestore_avatar_id = None
            request.user.save(
                update_fields=["use_firestore_avatar", "firestore_avatar_id"]
            )
            return DRFResponse({"message": "Avatar deleted successfully"})

        return DRFResponse(
            {"error": "Failed to delete avatar"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )