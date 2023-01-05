from django.db import models
from common.models import CommonModel

# Create your models here.
class Sales(CommonModel):
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

    def __str__(self) -> str:
        return "질문"

    class Meta:
        verbose_name_plural = "질문"


class Answer(CommonModel):
    author = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="answers",
    )
    answer = models.CharField(max_length=200)
    post = models.ForeignKey(
        "sales.Question",
        on_delete=models.CASCADE,
        related_name="answers",
    )

    def __str__(self) -> str:
        return "답변"

    class Meta:
        verbose_name_plural = "답변"
