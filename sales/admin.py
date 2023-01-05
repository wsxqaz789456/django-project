from django.contrib import admin
from .models import Sales, Question, Answer

# Register your models here.
@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
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


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass
