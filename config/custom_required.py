from functools import wraps
from django.shortcuts import redirect
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

def is_valid_token(token):
    try:
        AccessToken(token)
        return True
    except (InvalidToken, TokenError):
        return False

def is_blacklisted(token):
    return BlacklistedToken.objects.filter(token=token).exists()

def jwt_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.COOKIES.get('access_token')  # Retrieve the JWT from cookies

        if token and is_valid_token(token) and not is_blacklisted(token):
            return view_func(request, *args, **kwargs)
        else:
            return redirect(settings.LOGIN_URL)  # Redirect to the login page if token is invalid or blacklisted

    return _wrapped_view