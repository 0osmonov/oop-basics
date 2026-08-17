from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Comment, Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


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
