from django.urls import path
from .views import Boards, BoardDetail, BoardComments, Comments

urlpatterns = [
    path("", Boards.as_view()),
    path("<int:pk>", BoardDetail.as_view()),
    path("<int:pk>/comments", BoardComments.as_view()),
    path("comments/<int:pk>", Comments.as_view()),
]
