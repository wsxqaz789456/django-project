from django.contrib import admin
from .models import Sales, Question, Answer

# Register your models here.
@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass
