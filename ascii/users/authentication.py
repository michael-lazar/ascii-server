from rest_framework.authentication import TokenAuthentication as _TokenAuthentication

from ascii.users.models import AuthToken


class TokenAuthentication(_TokenAuthentication):
    keyword = "Bearer"
    model = AuthToken
