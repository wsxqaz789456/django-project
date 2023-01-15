from django.contrib import admin
from .models import Board, Comment


# Django admin panel에서 표시할 항목들을 지정


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "title",
        "total_comments",
    )
    # 게시글의 작성자와 제목, 댓글 갯수를 표시함


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "article",
    )
    # 댓글의 작성자와 댓글이 작성된 게시글을 표시함
