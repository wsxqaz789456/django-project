from django.db import models

# 모든 model에 공통적으로 상속되는 CommonModel
class CommonModel(models.Model):
    """CommomModel에 대한 정의"""

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    # 상속 전용 모델
    class Meta:
        abstract = True
