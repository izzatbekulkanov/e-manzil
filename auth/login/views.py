from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken
from django.contrib.auth import get_user_model, login
from auth.serializers import CustomTokenObtainPairSerializer

import logging
logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email_or_username = request.data.get("email-username")
        password = request.data.get("password")

        if not (email_or_username and password):
            logger.debug("Email yoki parol kiritilmagan")
            return Response({'messages': [{'message': 'Email yoki parolni kiriting.', 'tags': 'error'}]},
                            status=status.HTTP_400_BAD_REQUEST)

        # To'g'ri ma'lumotlarni yuborish
        data = {"password": password}
        if '@' in email_or_username:
            data["email"] = email_or_username
        else:
            data["username"] = email_or_username

        try:
            serializer = CustomTokenObtainPairSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            tokens = serializer.validated_data

            response = Response({'messages': [{'message': 'Kirish muvaffaqiyatli.', 'tags': 'success'}]})
            response.set_cookie("access_token", tokens["access"], httponly=True, secure=True)
            response.set_cookie("refresh_token", tokens["refresh"], httponly=True, secure=True)

            decoded_token = AccessToken(tokens["access"])
            user_id = decoded_token['user_id']
            user = get_user_model().objects.get(id=user_id)
            if user:
                login(request, user, backend='auth.custom_backend.CustomBackend')

            return response
        except AuthenticationFailed as e:
            logger.debug(f"AuthenticationFailed occurred - {str(e)}")
            return Response({'messages': [{'message': 'Login yoki parol xato.', 'tags': 'error'}]},
                            status=status.HTTP_401_UNAUTHORIZED)
        except InvalidToken as e:
            logger.debug(f"InvalidToken occurred - {str(e)}")
            return Response({'messages': [{'message': 'Token olishda xatolik.', 'tags': 'error'}]},
                            status=status.HTTP_401_UNAUTHORIZED)
