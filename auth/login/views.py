from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect
import logging

from auth.serializers import CustomTokenObtainPairSerializer

logger = logging.getLogger(__name__)

class LoginView(APIView):
    def get(self, request):
        access_token = request.COOKIES.get('access_token')

        if access_token:
            try:
                decoded_token = AccessToken(access_token)
                user_id = decoded_token['user_id']
                user = get_user_model().objects.get(id=user_id)
                if user:
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect("index")
            except InvalidToken:
                logger.debug("Invalid token found in cookies")

        if request.user.is_authenticated:
            return redirect("index")

        return Response({'messages': []}, status=status.HTTP_200_OK)

    def post(self, request):
        email_or_username = request.data.get("email-username")
        password = request.data.get("password")

        if not (email_or_username and password):
            logger.debug("Email or password not provided")
            return Response({'messages': [{'message': 'Email yoki parolni kiriting.', 'tags': 'error'}]}, status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer = CustomTokenObtainPairSerializer(data={
                "username": email_or_username,
                "password": password,
                "email": email_or_username
            })
            serializer.is_valid(raise_exception=True)
            tokens = serializer.validated_data

            response = Response({'messages': [{'message': 'Kirish muvaffaqiyatli.', 'tags': 'success'}]})
            response.set_cookie("access_token", tokens["access"], httponly=True, secure=True)
            response.set_cookie("refresh_token", tokens["refresh"], httponly=True, secure=True)

            decoded_token = AccessToken(tokens["access"])
            user_id = decoded_token['user_id']
            user = get_user_model().objects.get(id=user_id)
            if user:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return response
        except AuthenticationFailed as e:
            logger.debug(f"AuthenticationFailed occurred - {str(e)}")
            return Response({'messages': [{'message': 'Login yoki parol xato.', 'tags': 'error'}]}, status=status.HTTP_401_UNAUTHORIZED)
        except InvalidToken as e:
            logger.debug(f"InvalidToken occurred - {str(e)}")
            return Response({'messages': [{'message': 'Token olishda xatolik.', 'tags': 'error'}]}, status=status.HTTP_401_UNAUTHORIZED)
