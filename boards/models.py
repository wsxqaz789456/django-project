from django.db import models
from common.models import CommonModel

# Create your models here.


class Board(CommonModel):
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

    def __str__(self) -> str:
        return self.title


class Comment(CommonModel):
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
