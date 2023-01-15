from rest_framework import serializers
from .models import Comment, Board
from users.serializers import TinyUserSerializer

# 게시판 model의 데이터 작성하거나 입력받을 때 검증하는 serializer 작성


class CommentSerializer(serializers.ModelSerializer):

    """댓글 모델의 데이터를 검증하는 serializer의 정의"""

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

    """게시글 모델의 데이터를 검증하는 serializer의 정의"""

    total_comments = serializers.SerializerMethodField()
    # 게시글 모델에 작성된 댓글의 갯수를 구하는 함수를 serializer에 불러옴
    def get_total_comments(self, instance):
        return instance.total_comments()

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
            "views",
            "total_comments",
            "comments",
        )
