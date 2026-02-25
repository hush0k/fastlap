from logging import getLogger

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Driver, DriverResult

logger = getLogger(__name__)


class DriverListSerializer(ModelSerializer):
    class Meta:
        model = Driver
        fields = ["id", "first_name", "last_name", "slug", "nationality", "number", "profile_image", "is_active"]


class DriverDetailSerializer(ModelSerializer):
    class Meta:
        model = Driver
        fields = "__all__"


class DriverResultSerializer(ModelSerializer):
    driver = SerializerMethodField()
    race = SerializerMethodField()

    def get_driver(self, obj: DriverResult) -> dict[str, int | str]:
        return {"id": obj.driver.id, "name": str(obj.driver)}
    
    def get_race(self, obj: DriverResult) -> dict[str, int | str]:
        return {"id": obj.race.id, "name": obj.race.name}
    
    class Meta:
        model = DriverResult
        fields = "__all__"


class DriverResultCreateSerializer(ModelSerializer):
    class Meta:
        model = DriverResult
        fields = "__all__"
        read_only_fields = ("id",)
