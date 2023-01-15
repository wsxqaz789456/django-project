from django.contrib import admin

# Django에서 제공하는 기본 유저 admin 모델
from django.contrib.auth.admin import UserAdmin

from .models import User


# Django admin panel에서 표시할 항목들을 지정


@admin.register(User)
# Django에서 제공되는 기본 유저 모델을 상속받아 custom
class CustomUserAdmin(UserAdmin):

    """User admin panel에 표시할 항목들을 지정"""

    fieldsets = (
        (
            "프로필",
            {
                "fields": (
                    "avatar",
                    "username",
                    "password",
                    "name",
                    "email",
                    "gender",
                ),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Important dates",
            {
                "fields": ("last_login", "date_joined"),
            },
        ),
    )
    list_display = (
        "username",
        "email",
        "name",
        "gender",
    )
