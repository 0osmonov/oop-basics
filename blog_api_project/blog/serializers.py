from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

from .models import Comment, Post
from .redis_client import get_confirmation_code

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number']


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=6,
        style={'input_type': 'password'},
    )
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate_email(self, value):
        value = value.strip().lower()
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('Пользователь с таким email уже существует')
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False,
        )


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(label='Email')
    password = serializers.CharField(
        label='Password',
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True,
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError('Email и пароль обязательны')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )

        if not user:
            raise serializers.ValidationError('Неверный email или пароль')

        attrs['user'] = user
        return attrs


class UserConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(min_length=6, max_length=6)

    def validate(self, data):
        email = data['email'].strip().lower()
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'email': 'Пользователь не найден'})

        if user.is_active:
            raise serializers.ValidationError({'email': 'Пользователь уже подтверждён'})

        stored_code = get_confirmation_code(email)
        if not stored_code:
            raise serializers.ValidationError(
                {'code': 'Код подтверждения не найден или истёк (TTL 5 минут)'},
            )

        if stored_code != data['code']:
            raise serializers.ValidationError({'code': 'Неверный код подтверждения'})

        data['user'] = user
        data['email'] = email
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
