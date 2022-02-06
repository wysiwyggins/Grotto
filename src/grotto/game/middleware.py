from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from characterBuilder.models import Character

def character_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # get character detail
        request.character = None
        if request.user.is_authenticated:
            request.character = request.user.character

        response = get_response(request)
        return response

    return middleware


def token_auth_middleware(get_response):
    # auth the user with token

    def middleware(request):
        if getattr(request, "user") is not None:
            if request.user.is_authenticated:
                response = get_response(request)
                return response
        auth_header = request.headers.get("authorization")
        if auth_header is None:
            response = get_response(request)
            return response

        try:
            prefix, key = auth_header.split()
            if prefix.lower() != "token":
                raise ValueError
        except ValueError:
            response = get_response(request)
            return response

        try:
            token = Token.objects.select_related("user").get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed("Invalid token!")
        if not token.user.is_active:
            raise AuthenticationFailed("User is inactive!")
        request.user = token.user
        response = get_response(request)
        return response

    return middleware
