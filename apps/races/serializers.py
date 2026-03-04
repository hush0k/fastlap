from rest_framework.serializers import ModelSerializer

from .models import Series


class SeriesSerializer(ModelSerializer):
    class Meta:
        model = Series
        fields = ("id", "name", "category", "logo")
