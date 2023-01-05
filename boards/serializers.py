from rest_framework import serializers
from .models import Comment, Board
from users.serializers import TinyUserSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = TinyUserSerializer(
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = (
            "pk",
            "author",
            "body",
            "created_at",
        )


class BoardSerializer(serializers.ModelSerializer):
    author = TinyUserSerializer(
        read_only=True,
    )
    comments = CommentSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Board
        fields = (
            "pk",
            "title",
            "author",
            "content",
            "created_at",
            "updated_at",
            "comments",
        )
