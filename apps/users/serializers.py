"""
Serializers for the users app.
"""

# Python modules
import re
from typing import Any

from asgiref.sync import async_to_sync
from drf_spectacular.utils import extend_schema_field
from rest_framework_simplejwt.tokens import RefreshToken

# Django modules
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _

# Django REST Framework
from rest_framework import serializers
from rest_framework.request import Request

from .services.firestore_service import FirestoreUserService

# Project modules
from .utils.avatar_utils import AvatarProcessor

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """

    password = serializers.CharField(write_only=True, min_length=8)
    avatar = serializers.ImageField(required=False, allow_empty_file=True)

    @extend_schema_field({"type": "string", "format": "binary"})
    def get_avatar(self, obj: Any) -> None:
        """Avatar field for schema generation."""
        pass

    class Meta:
        model = User
        fields = ("email", "username", "password", "first_name", "last_name", "avatar")

    def validate_password(self, value: str) -> str:
        """
        Validate password strength.

        Checks:
        - Minimum length: 8 characters
        - Maximum length: 128 characters
        - Contains both uppercase and lowercase letters
        - Contains at least one number
        - Contains at least one special character
        - Passes Django's built-in validators
        """
        if len(value) < 8:
            raise serializers.ValidationError(
                _("Password must be at least 8 characters long.")
            )

        if len(value) > 128:
            raise serializers.ValidationError(
                _("Password must be no more than 128 characters long.")
            )

        has_upper = any(c.isupper() for c in value)
        has_lower = any(c.islower() for c in value)
        if not (has_upper and has_lower):
            raise serializers.ValidationError(
                _("Password must contain both uppercase and lowercase letters.")
            )

        has_digit = any(c.isdigit() for c in value)
        if not has_digit:
            raise serializers.ValidationError(
                _("Password must contain at least one number.")
            )

        if not re.search(r"[^\w\s]", value):
            raise serializers.ValidationError(
                _(
                    "Password must contain at least one special character (e.g. @, &, /, !)."  # noqa: E501
                )
            )

        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)

        return value

    def validate_avatar(self, value):
        """
        Validate avatar file if provided.
        """
        if value is None:
            return value

        if isinstance(value, str):
            raise serializers.ValidationError(
                _("Avatar must be uploaded as a file (multipart/form-data).")
            )

        is_valid, error = AvatarProcessor.validate_image(value)
        if not is_valid:
            raise serializers.ValidationError(_(error))

        return value

    def create(self, validated_data):
        """
        Create a new user with optional avatar.
        """
        password = validated_data.pop("password")
        avatar_file = validated_data.pop("avatar", None)
        user = User.objects.create_user(password=password, **validated_data)

        if avatar_file:
            firestore_service = FirestoreUserService()
            base64_avatar, error = AvatarProcessor.process_avatar(avatar_file)

            if error:
                user.delete()
                raise serializers.ValidationError({"avatar": error})

            avatar_id = async_to_sync(firestore_service.create_user_avatar)(user.id, base64_avatar)

            if avatar_id:
                user.firestore_avatar_id = avatar_id
                user.use_firestore_avatar = True
                user.save(update_fields=["firestore_avatar_id", "use_firestore_avatar"])
            else:
                user.delete()
                raise serializers.ValidationError(
                    {"avatar": "Failed to store avatar. Please try again."}
                )
        else:
            user.use_firestore_avatar = False
            user.save(update_fields=["use_firestore_avatar"])

        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs: dict[str, Any]) -> dict[str, str]:
        """
        Validate login credentials and return JWT tokens.
        """
        email: str = attrs.get("email")
        password: str = attrs.get("password")

        request: Request | None = self.context.get("request")
        if request is None:
            raise serializers.ValidationError(
                _("Internal error: request context is missing.")
            )

        user = authenticate(request=request, username=email, password=password)

        if user is None:
            raise serializers.ValidationError(_("Invalid email or password."))

        if not user.is_active:
            raise serializers.ValidationError(_("User account is disabled."))

        refresh: RefreshToken = RefreshToken.for_user(user)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}
