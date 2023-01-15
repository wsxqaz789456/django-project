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
    # 기본적으로 username은 unique
    # email 필드에도 unique=True옵션을 지정하여 가입시 중복이 불가능하게 설정
    email = models.EmailField(
        unique=True,
    )
