from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView

from drf_spectacular.utils import extend_schema

from .serializers import RegisterSerializer, LoginSerializer


@extend_schema(request=RegisterSerializer)
class RegisterView(generics.CreateAPIView):
  permission_classes = [AllowAny]
  serializer_class = RegisterSerializer
  parser_classes = [MultiPartParser, FormParser]


@extend_schema(
  request=LoginSerializer,
  responses={
    200: {
      "type": "object",
      "properties": {
          "refresh": {"type": "string"},
          "access": {"type": "string"},
      },
    }
  },
)
class LoginView(GenericAPIView):
  permission_classes = [AllowAny]
  serializer_class = LoginSerializer

  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)  # includes request in context
    serializer.is_valid(raise_exception=True)
    return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RefreshView(TokenRefreshView):
  permission_classes = [AllowAny]