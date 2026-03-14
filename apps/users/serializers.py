import re

from drf_spectacular.utils import extend_schema_field
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .utils.avatar_utils import AvatarProcessor
from .services.firestore_service import FirestoreUserService

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    avatar = serializers.ImageField(required=True, allow_empty_file=False)

    @extend_schema_field({"type": "string", "format": "binary"})
    def get_avatar(self, obj):
        pass

    class Meta:
        model = User
        fields = ("email", "username", "password", "first_name", "last_name", "avatar")

    def validate_password(self, value: str) -> str:
        validate_password(value)

        if not re.search(r"[^\w\s]", value):
            raise serializers.ValidationError(
                _(
                    "Password must contain at least one special character (e.g. @, &, /, !)."
                )
            )

        has_letter = any(c.isalpha() for c in value)
        has_digit = any(c.isdigit() for c in value)
        if not (has_letter and has_digit):
            raise serializers.ValidationError(
                _("Password must contain both letters and numbers.")
            )

        return value

    def validate_avatar(self, value):
        if isinstance(value, str):
            raise serializers.ValidationError(
                _("Avatar must be uploaded as a file (multipart/form-data).")
            )

        if not value:
            raise serializers.ValidationError(_("Avatar is required."))

        is_valid, error = AvatarProcessor.validate_image(value)
        if not is_valid:
            raise serializers.ValidationError(_(error))

        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        avatar_file = validated_data.pop("avatar")
        user = User.objects.create_user(password=password, **validated_data)

        firestore_service = FirestoreUserService()

        base64_avatar, error = AvatarProcessor.process_avatar(avatar_file)
        if error:
            user.delete()
            raise serializers.ValidationError({"avatar": error})

        avatar_id = firestore_service.create_user_avatar(user.id, base64_avatar)

        if avatar_id:
            user.firestore_avatar_id = avatar_id
            user.use_firestore_avatar = True
            user.save(update_fields=["firestore_avatar_id", "use_firestore_avatar"])
        else:
            user.delete()
            raise serializers.ValidationError(
                {"avatar": "Failed to store avatar. Please try again."}
            )

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        request = self.context.get("request")
        if request is None:
            raise serializers.ValidationError(
                _("Internal error: request context is missing.")
            )

        user = authenticate(request=request, username=email, password=password)

        if user is None:
            raise serializers.ValidationError(_("Invalid email or password."))

        if not user.is_active:
            raise serializers.ValidationError(_("User account is disabled."))

        refresh = RefreshToken.for_user(user)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}
