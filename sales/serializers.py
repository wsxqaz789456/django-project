from rest_framework import serializers

from .models import Sales, Question, Answer

from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer


class AnswerSerializer(serializers.ModelSerializer):
    author = TinyUserSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = (
            "pk",
            "author",
            "answer",
            "updated_at",
        )


class QuestionSerializer(serializers.ModelSerializer):
    author = TinyUserSerializer(read_only=True)
    answers = AnswerSerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        model = Question
        fields = (
            "id",
            "author",
            "question",
            "created_at",
            "answers",
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
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Sales
        fields = (
            "pk",
            "name",
            "price",
            "location",
        )
