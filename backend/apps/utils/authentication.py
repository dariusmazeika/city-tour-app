from functools import cached_property

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User


class TokenUser:
    is_active = True
    is_anonymous = False
    user = None

    def __getattribute__(self, name):
        if not hasattr(TokenUser, name) and hasattr(User, name):
            if not self.user:
                self.user = User.objects.filter(id=self.id).first()
                if not self.user:
                    raise InvalidToken('user_does_not_exist')
            return getattr(self.user, name)
        return super().__getattribute__(name)

    def __init__(self, token):
        self.token = token

    def __str__(self):
        return 'TokenUser {}'.format(self.id)

    @cached_property
    def id(self):
        return self.token["user_id"]

    @cached_property
    def pk(self):
        return self.id

    @cached_property
    def is_staff(self):
        return self.token.get('is_staff', False)

    @cached_property
    def is_superuser(self):
        return self.token.get('is_superuser', False)

    @cached_property
    def email(self):
        return self.token.get('email', '')

    @property
    def is_authenticated(self):
        return True


class JWTTokenUserAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        if api_settings.USER_ID_CLAIM not in validated_token:
            raise InvalidToken('error_user_id_is_not_in_token')
        return TokenUser(validated_token)


class JWTRefreshToken(RefreshToken):

    @classmethod
    def for_user(cls, user: User):
        token = super().for_user(user)
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser
        return token
