from django.db import models

# Django에서 제공하는 기본 유저 모델
from django.contrib.auth.models import AbstractUser


# Django에서 제공하는 기본 유저 모델을 상속 받음
class User(AbstractUser):

    """User model에 대한 정의"""

    class GenderChoices(models.TextChoices):

        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    first_name = models.CharField(
        max_length=150,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )
    name = models.CharField(
        max_length=150,
        default="",
    )
    avatar = models.URLField(
        blank=True,
    )
    gender = models.CharField(
        blank=True,
        max_length=10,
        choices=GenderChoices.choices,
    )
