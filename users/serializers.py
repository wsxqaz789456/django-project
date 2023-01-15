from rest_framework import serializers
from .models import User


# User model의 대한 데이터 검증에 필요한 serialzier 작성


class TinyUserSerializer(serializers.ModelSerializer):
    # name, username , avatar만 보여주는 serailizer
    class Meta:
        model = User
        fields = (
            "name",
            "username",
            "avatar",
        )


class PrivateUserSerializer(serializers.ModelSerializer):
    # password, superuser여부 등 공개되어선 안되는 정보들을 제외한 serailizer
    class Meta:
        model = User
        exclude = (
            "password",
            "is_superuser",
            "id",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions",
        )
