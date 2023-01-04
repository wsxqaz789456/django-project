from django.db import models
from common.models import CommonModel

# Create your models here.
class Photo(CommonModel):
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
