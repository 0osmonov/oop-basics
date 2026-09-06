import random

from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from .models import Comment, Post
from .pagination import PostPagination
from .permissions import IsAuthorOrReadOnly
from .redis_client import delete_confirmation_code, save_confirmation_code
from .serializers import (
    CommentCreateUpdateSerializer,
    CommentSerializer,
    PostCreateUpdateSerializer,
    PostDetailSerializer,
    PostListSerializer,
    UserConfirmSerializer,
    UserLoginSerializer,
    UserRegisterSerializer,
)
from .tasks import log_user_registered, send_confirmation_email


class CustomAuthToken(ObtainAuthToken):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if not user.is_active:
            return Response(
                {'detail': 'Пользователь не подтверждён'},
                status=status.HTTP_403_FORBIDDEN,
            )
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        code = f'{random.randint(0, 999999):06d}'
        save_confirmation_code(user.email, code)
        # Пример Celery .delay()
        log_user_registered.delay(user.email)
        # Пример Celery + SMTP
        send_confirmation_email.delay(user.email, code)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {'message': 'Пользователь зарегистрирован. Подтвердите аккаунт кодом из 6 цифр.'},
            status=status.HTTP_201_CREATED,
        )


class UserConfirmAPIView(generics.CreateAPIView):
    serializer_class = UserConfirmSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        email = serializer.validated_data['email']
        user.is_active = True
        user.save(update_fields=['is_active'])
        delete_confirmation_code(email)
        return Response({'message': 'Пользователь успешно подтверждён'})


class PostListCreateAPIView(generics.ListCreateAPIView):
    pagination_class = PostPagination

    def get_queryset(self):
        queryset = Post.objects.select_related('author')
        if not self.request.user.is_authenticated:
            return queryset.filter(is_published=True)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateUpdateSerializer
        return PostListSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        queryset = Post.objects.select_related('author').prefetch_related(
            'comments__author',
        )
        if not self.request.user.is_authenticated:
            return queryset.filter(is_published=True)
        return queryset

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return PostCreateUpdateSerializer
        return PostDetailSerializer


class PostCommentListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_post(self):
        queryset = Post.objects.all()
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_published=True)
        return generics.get_object_or_404(queryset, id=self.kwargs['id'])

    def get_queryset(self):
        post = self.get_post()
        queryset = Comment.objects.filter(post=post).select_related('author')
        if not self.request.user.is_authenticated:
            return queryset.filter(is_approved=True)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateUpdateSerializer
        return CommentSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.select_related('author', 'post')
    serializer_class = CommentCreateUpdateSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return CommentCreateUpdateSerializer
        return CommentSerializer
