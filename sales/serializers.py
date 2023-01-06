from rest_framework import serializers

from .models import Sales, Question

from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer


""" class AnswerSerializer(serializers.ModelSerializer):
    author = TinyUserSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = (
            "pk",
            "author",
            "answer",
            "updated_at",
        ) """


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

    class Meta:
        model = Sales
        fields = "__all__"


class SalesTitleSerializers(serializers.ModelSerializer):
    owner = TinyUserSerializer(read_only=True)

    class Meta:
        model = Sales
        fields = (
            "pk",
            "owner",
            "name",
            "price",
            "location",
        )
