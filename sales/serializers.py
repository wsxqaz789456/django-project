from rest_framework import serializers


from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from photos.serializers import PhotoSerializer

from .models import Sales, Question


# 판매 게시글과 댓글 model의 대한 데이터 검증에 필요한 serialzier 작성


class QuestionSerializer(serializers.ModelSerializer):
    author = TinyUserSerializer(read_only=True)
    reply = serializers.SerializerMethodField()

    def get_reply(self, instance):
        serializer = self.__class__(instance.reply, many=True)
        serializer.bind("", self)
        return serializer.data

    class Meta:
        model = Question
        fields = (
            "id",
            "author",
            "question",
            "parent",
            "is_parent",
            "created_at",
            "reply",
        )


class SalesSerializers(serializers.ModelSerializer):
    owner = TinyUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    questions = QuestionSerializer(read_only=True, many=True)
    photos = PhotoSerializer(many=True, read_only=True)
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Sales
        fields = "__all__"

    def get_is_owner(self, instance):
        request = self.context.get("request")
        if request:
            return instance.owner == request.user
        return False


class SalesTitleSerializers(serializers.ModelSerializer):
    owner = TinyUserSerializer(read_only=True)
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Sales
        fields = (
            "pk",
            "owner",
            "name",
            "price",
            "location",
            "photos",
        )
