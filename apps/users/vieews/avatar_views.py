from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from ..services.firestore_service import FirestoreUserService
from ..utils.avatar_utils import AvatarProcessor


@extend_schema(
    methods=["POST"],
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
    responses={200: {"type": "object", "properties": {"message": {"type": "string"}}}},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_avatar(request):
    """Upload user avatar to Firestore"""
    avatar_file = request.FILES.get("avatar")

    if not avatar_file:
        return Response(
            {"error": "No avatar file provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    base64_avatar, error = AvatarProcessor.process_avatar(avatar_file)

    if error:
        return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

    firestore_service = FirestoreUserService()
    success = firestore_service.update_user_avatar(request.user.id, base64_avatar)

    if success:
        request.user.use_firestore_avatar = True
        request.user.save(update_fields=["use_firestore_avatar"])

        return Response(
            {"message": "Avatar uploaded successfully", "avatar": base64_avatar}
        )
    else:
        return Response(
            {"error": "Failed to upload avatar"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@extend_schema(
    methods=["GET"],
    responses={200: {"type": "object", "properties": {"avatar": {"type": "string"}}}},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_avatar(request):
    """Get user's current avatar from Firestore"""
    firestore_service = FirestoreUserService()
    avatar_base64 = firestore_service.get_user_avatar(request.user.id)

    if avatar_base64:
        return Response({"avatar": avatar_base64})
    else:
        return Response({"error": "Avatar not found"}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(
    methods=["DELETE"],
    responses={200: {"type": "object", "properties": {"message": {"type": "string"}}}},
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_avatar(request):
    """Delete user's avatar from Firestore"""
    firestore_service = FirestoreUserService()
    success = firestore_service.delete_user_avatar(request.user.id)

    if success:
        request.user.use_firestore_avatar = False
        request.user.firestore_avatar_id = None
        request.user.save(update_fields=["use_firestore_avatar", "firestore_avatar_id"])

        return Response({"message": "Avatar deleted successfully"})
    else:
        return Response(
            {"error": "Failed to delete avatar"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
