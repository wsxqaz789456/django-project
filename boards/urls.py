from django.urls import path
from .views import Boards, BoardDetail, BoardComments, Comments

# 작성한 경로에 대한 나타낼 view 지정

urlpatterns = [
    path("", Boards.as_view()),
    path("<int:pk>", BoardDetail.as_view()),
    path("<int:pk>/comments", BoardComments.as_view()),
    path("comments/<int:pk>", Comments.as_view()),
]
