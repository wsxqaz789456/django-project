from django.contrib import admin
from .models import Board, Comment

# Register your models here.
@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "title",
        "total_comments",
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "article",
    )
