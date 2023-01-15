from django.db import models
from common.models import CommonModel


# 사진 파일에 대한 mdoel
class Photo(CommonModel):
    """Photo Model에 대한 정의"""

    file = models.URLField()
    sale = models.ForeignKey(
        "sales.Sales",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )

    def __str__(self) -> str:
        return "Photo File"
