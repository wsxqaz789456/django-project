from django.db import models
from django.contrib.auth.models import AbstractUser

# Django에서 제공하는 기본 유저 모델


class User(AbstractUser):
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
        max_length=10,
        choices=GenderChoices.choices,
    )
