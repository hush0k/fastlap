from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(
        self,
        email: str,
        password: str | None = None,
        **extra_fields: object,
    ) -> "User":
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user: "User" = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        password: str | None = None,
        **extra_fields: object,
    ) -> "User":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email: models.EmailField = models.EmailField(unique=True)
    username: models.CharField = models.CharField(max_length=100, unique=True)
    first_name: models.CharField = models.CharField(max_length=100, blank=True)
    last_name: models.CharField = models.CharField(max_length=100, blank=True)
    avatar: models.ImageField = models.ImageField(upload_to="avatars/", blank=True, null=True)
    firestore_avatar_id: models.CharField = models.CharField(max_length=255, blank=True, null=True)
    use_firestore_avatar: models.BooleanField = models.BooleanField(default=False)
    is_active: models.BooleanField = models.BooleanField(default=True)
    is_staff: models.BooleanField = models.BooleanField(default=False)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return self.email

    def get_avatar_url(self) -> str | None:
        if self.use_firestore_avatar and self.firestore_avatar_id:
            return None
        elif self.avatar:
            return self.avatar.url
        return None