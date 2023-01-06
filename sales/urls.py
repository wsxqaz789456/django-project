from django.urls import path
from .views import Sale, SaleDetail, Questsions, QuestionDetail, RoomPhotos

urlpatterns = [
    path("", Sale.as_view()),
    path("<int:pk>", SaleDetail.as_view()),
    path("<int:pk>/photos", RoomPhotos.as_view()),
    path("<int:pk>/questions", Questsions.as_view()),
    path("<int:pk>/questions/<int:q_pk>", QuestionDetail.as_view()),
    # path("<int:pk>/questions/<int:q_pk>/answer/<int:a_pk>", Answer.as_view()),
]
