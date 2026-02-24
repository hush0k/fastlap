from rest_framework.viewsets import ModelViewSet
from apps.common.permissions import IsAuthenticatedReadOnlyOrStaffWrite


# Create your views here.
class NewsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedReadOnlyOrStaffWrite]
