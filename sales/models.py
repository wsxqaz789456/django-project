from django.db import models
from common.models import CommonModel


# 판매 게시판에 사용될 게시글과 댓글에 대한 model 작성
class Sales(CommonModel):

    """판매 게시글의 model에 대한 정의"""

    name = models.CharField(
        max_length=150,
    )
    description = models.TextField()
    price = models.IntegerField()
    bought_price = models.IntegerField()
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="sales",
    )
    location = models.CharField(
        max_length=150,
    )
    unopened = models.BooleanField(
        verbose_name="미개봉 상품", default=False, help_text="미개봉 상품입니까?"
    )
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sales",
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "판매"


class Question(CommonModel):

    """판매 게시글의 댓글 model에 대한 정의"""

    author = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="questions",
    )
    question = models.CharField(max_length=200)
    product = models.ForeignKey(
        "sales.Sales",
        on_delete=models.CASCADE,
        related_name="questions",
    )

    # 대댓글 작성시 자신을 모델 key로 지정함
    # 최초 작성시 기본적으로 null값으로 지정됨
    # null 값으로 지정될 경우 최상위 부모 댓글
    # 댓글의 pk값을 전달받을 경우 해당 댓글의 자식 댓글로 구성됨
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reply",
    )
    is_parent = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"질문 : {self.question}"

    class Meta:
        verbose_name_plural = "질문"
