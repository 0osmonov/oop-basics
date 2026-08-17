from django.urls import path

from . import views

urlpatterns = [
    path('posts/', views.PostListCreateAPIView.as_view()),
    path('posts/<int:id>/', views.PostDetailAPIView.as_view()),
    path('posts/<int:id>/comments/', views.PostCommentListCreateAPIView.as_view()),
    path('comments/<int:id>/', views.CommentDetailAPIView.as_view()),
    path('auth/token/', views.CustomAuthToken.as_view()),
]
