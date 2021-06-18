from django.urls import path
from HackerNewsApi import views

urlpatterns = [
    path("posts/", views.PostsList.as_view(), name="posts"),
    path("posts/<int:pk>/", views.PostDetail.as_view()),
    path("posts/<int:pk>/vote/", views.VotesView.as_view()),
    path("posts/<int:pk>/comments/", views.CommentsList.as_view()),
    path("posts/<int:pk>/comments/<int:id>/", views.CommentsDetail.as_view()),
    path("users/<int:pk>/", views.UserDetail.as_view()),
    path("register/", views.UserCreate.as_view()),
]
