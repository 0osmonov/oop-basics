from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Comment, ConfirmationCode, Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate_username(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Имя пользователя не может быть пустым')
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError('Пользователь с таким именем уже существует')
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            is_active=False,
        )
        return user


class UserConfirmSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField(min_length=6, max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            raise serializers.ValidationError({'username': 'Пользователь не найден'})

        if user.is_active:
            raise serializers.ValidationError({'username': 'Пользователь уже подтверждён'})

        try:
            confirmation = user.confirmation_code
        except ConfirmationCode.DoesNotExist:
            raise serializers.ValidationError({'code': 'Код подтверждения не найден'})

        if confirmation.code != data['code']:
            raise serializers.ValidationError({'code': 'Неверный код подтверждения'})

        data['user'] = user
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'author',
            'body',
            'created_at',
            'updated_at',
            'is_approved',
        ]
        read_only_fields = ['post', 'author', 'created_at', 'updated_at']


class PostListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'title',
            'body',
            'created_at',
            'updated_at',
            'is_published',
        ]


class PostDetailSerializer(PostListSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta(PostListSerializer.Meta):
        fields = PostListSerializer.Meta.fields + ['comments']


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'body', 'is_published']

    def validate_title(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Заголовок не может быть пустым')
        return value

    def validate_body(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Текст не может быть пустым')
        return value


class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['body', 'is_approved']

    def validate_body(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Текст комментария не может быть пустым')
        return value
