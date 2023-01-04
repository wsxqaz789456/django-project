from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Django에서 제공하는 기본 유저 admin 모델

# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
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
