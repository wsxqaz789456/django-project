from django.db import models
from common.models import CommonModel


# 게시판에 사용될 게시글과 댓글의 모델을 작성함.


class Board(CommonModel):

    """게시글 모델의 정의"""

    author = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="boards",
    )
    title = models.CharField(
        max_length=60,
    )
    content = models.TextField()

    views = models.IntegerField(default=0)

    # 게시글에 작성된 댓글의 갯수를 구함
    def total_comments(self):
        return self.comments.count()

    def __str__(self) -> str:
        return self.title


class Comment(CommonModel):

    """댓글 모델의 정의"""

    author = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    body = models.CharField(
        max_length=300,
    )
    article = models.ForeignKey(
        "boards.Board",
        on_delete=models.CASCADE,
        related_name="comments",
    )

    def __str__(self) -> str:
        return f"{self.article} / {self.author}"
