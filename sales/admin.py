from django.contrib import admin
from .models import Sales, Question


# Django admin panel에서 표시할 항목들을 지정


@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    """admin panel에서 나타낼 항목들과 필터 요소들을 지정"""

    list_display = (
        "name",
        "price",
        "bought_price",
        "owner",
        "unopened",
        "category",
        "created_at",
    )
    list_filter = (
        "price",
        "bought_price",
        "owner",
        "category",
        "created_at",
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """admin panel에서 나타낼 항목들과 필터 요소들을 지정"""

    list_display = (
        "author",
        "product",
        "created_at",
    )
    list_filter = (
        "author",
        "product",
        "created_at",
    )


""" @admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass """
