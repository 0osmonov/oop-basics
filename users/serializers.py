from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        birthdate = user.birthdate.isoformat() if user.birthdate else None
        token['birthdate'] = birthdate
        token['username'] = user.username
        # явно кладём claim и в access token
        token.access_token['birthdate'] = birthdate
        token.access_token['username'] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['birthdate'] = self.user.birthdate.isoformat() if self.user.birthdate else None
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
