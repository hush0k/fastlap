from drf_spectacular.openapi import AutoSchema
from drf_spectacular.plumbing import force_instance


class RaceTrackAutoSchema(AutoSchema):
  def _map_serializer(self, serializer, direction, bypass_extensions=False):
    serializer_instance = force_instance(serializer)
    if hasattr(serializer_instance, 'Meta') and hasattr(serializer_instance.Meta, 'model'):
      if serializer_instance.Meta.model.__name__ == 'Track':
        original_fields = list(serializer_instance.fields.keys())
        for field_name in original_fields:
          if field_name == 'timezone':
            serializer_instance.fields.pop(field_name, None)
    return super()._map_serializer(serializer_instance, direction, bypass_extensions)