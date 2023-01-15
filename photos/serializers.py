from rest_framework import serializers
from .models import Photo

# Photo Model에 대한 검증에 사용되는 serializer


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            "pk",
            "file",
        )
