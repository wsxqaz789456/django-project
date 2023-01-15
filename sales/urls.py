from django.urls import path
from .views import Sale, SaleDetail, Questsions, QuestionDetail, SalePhotos

# 특정 url로 접근시 수행할 view지정

urlpatterns = [
    path("", Sale.as_view()),
    path("<int:pk>", SaleDetail.as_view()),
    path("<int:pk>/photos", SalePhotos.as_view()),
    path("<int:pk>/questions", Questsions.as_view()),
    path("<int:pk>/questions/<int:q_pk>", QuestionDetail.as_view()),
]
