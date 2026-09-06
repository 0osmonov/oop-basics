import json
import urllib.error
import urllib.parse
import urllib.request

from django.conf import settings
from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser


GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
GOOGLE_TOKEN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USERINFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'


def _http_post_form(url, data):
    encoded = urllib.parse.urlencode(data).encode('utf-8')
    request = urllib.request.Request(
        url,
        data=encoded,
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        method='POST',
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.loads(response.read().decode('utf-8'))


def _http_get_json(url, access_token):
    request = urllib.request.Request(
        url,
        headers={'Authorization': f'Bearer {access_token}'},
        method='GET',
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.loads(response.read().decode('utf-8'))


def exchange_code_for_tokens(code):
    return _http_post_form(
        GOOGLE_TOKEN_URL,
        {
            'code': code,
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': settings.GOOGLE_REDIRECT_URI,
            'grant_type': 'authorization_code',
        },
    )


def fetch_google_userinfo(access_token):
    return _http_get_json(GOOGLE_USERINFO_URL, access_token)


def get_or_create_google_user(userinfo):
    email = userinfo.get('email')
    if not email:
        raise serializers.ValidationError({'email': 'Google не вернул email'})

    first_name = userinfo.get('given_name', '') or ''
    last_name = userinfo.get('family_name', '') or ''

    user, created = CustomUser.objects.get_or_create(
        email=email,
        defaults={
            'username': email,
            'first_name': first_name,
            'last_name': last_name,
            'registration_source': 'google',
            'is_active': True,
        },
    )

    if not created:
        user.first_name = first_name or user.first_name
        user.last_name = last_name or user.last_name
        user.registration_source = 'google'

    user.is_active = True
    user.last_login = timezone.now()
    user.save(update_fields=[
        'first_name',
        'last_name',
        'registration_source',
        'is_active',
        'last_login',
    ])
    return user, created


def issue_jwt_for_user(user):
    refresh = RefreshToken.for_user(user)
    birthdate = user.birthdate.isoformat() if user.birthdate else None
    refresh['birthdate'] = birthdate
    refresh.access_token['birthdate'] = birthdate
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'registration_source': user.registration_source,
        },
    }


class GoogleAuthURLAPIView(APIView):
    """Возвращает URL для редиректа на Google OAuth (без готовых OAuth-библиотек)."""

    permission_classes = [AllowAny]

    def get(self, request):
        if not settings.GOOGLE_CLIENT_ID:
            return Response(
                {'detail': 'GOOGLE_CLIENT_ID не настроен. Добавьте его в .env'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        params = {
            'client_id': settings.GOOGLE_CLIENT_ID,
            'redirect_uri': settings.GOOGLE_REDIRECT_URI,
            'response_type': 'code',
            'scope': 'openid email profile',
            'access_type': 'offline',
            'prompt': 'consent',
        }
        auth_url = f'{GOOGLE_AUTH_URL}?{urllib.parse.urlencode(params)}'
        return Response({'auth_url': auth_url})


class GoogleAuthCallbackAPIView(APIView):
    """
    Callback / login через Google:
    1) получает code
    2) вручную обменивает code на access_token
    3) получает given_name / family_name
    4) создаёт/логинит пользователя
    """

    permission_classes = [AllowAny]

    def get(self, request):
        code = request.query_params.get('code')
        return self._login_with_code(code)

    def post(self, request):
        code = request.data.get('code')
        return self._login_with_code(code)

    def _login_with_code(self, code):
        if not code:
            return Response(
                {'detail': 'Параметр code обязателен'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            tokens = exchange_code_for_tokens(code)
            access_token = tokens.get('access_token')
            if not access_token:
                return Response(
                    {'detail': 'Не удалось получить access_token от Google', 'google': tokens},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            userinfo = fetch_google_userinfo(access_token)
            user, created = get_or_create_google_user(userinfo)
            data = issue_jwt_for_user(user)
            data['created'] = created
            return Response(data, status=status.HTTP_200_OK)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode('utf-8')
            return Response(
                {'detail': 'Ошибка Google OAuth', 'google_error': body},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as exc:
            return Response(
                {'detail': str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )
