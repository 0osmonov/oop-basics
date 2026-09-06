from django.urls import path

from .views import GoogleAuthCallbackAPIView, GoogleAuthURLAPIView

urlpatterns = [
    path('auth/google/', GoogleAuthURLAPIView.as_view()),
    path('auth/google/callback/', GoogleAuthCallbackAPIView.as_view()),
]
