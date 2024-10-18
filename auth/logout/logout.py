from django.shortcuts import redirect
from django.http import JsonResponse
from django.views import View
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken
import logging

logger = logging.getLogger(__name__)


class LogoutView(View):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        session_id = request.COOKIES.get('sessionid')

        if not refresh_token:
            logger.debug("Refresh token mavjud emas")
            return JsonResponse({'messages': [{'message': 'Refresh token mavjud emas.', 'tags': 'error'}]}, status=400)

        try:
            # Refresh tokenni qora ro'yxatga olish
            token = RefreshToken(refresh_token)
            token.blacklist()

            # Javobni tayyorlash va cookie'larni o'chirish
            response = JsonResponse({'messages': [{'message': 'Muvaffaqiyatli logout qilindi.', 'tags': 'success'}]})
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')

            # Session ID cookie'sini o'chirish
            if session_id:
                response.delete_cookie('sessionid')

            # Foydalanuvchini login sahifasiga yo'naltirish
            response['Location'] = '/login/'  # Login sahifasining URL manzilini qo'shing
            response.status_code = 302  # Redirect status kodi

            return response
        except InvalidToken as e:
            logger.error(f"Tokenni qora ro'yxatga olishda xatolik: {str(e)}", exc_info=True)
            return JsonResponse(
                {'messages': [{'message': 'Tokenni qora ro\'yxatga olishda xatolik yuz berdi.', 'tags': 'error'}]},
                status=400)
        except Exception as e:
            logger.error(f"Logout qilishda xatolik: {str(e)}", exc_info=True)
            return JsonResponse({'messages': [{'message': 'Logout qilishda xatolik yuz berdi.', 'tags': 'error'}]},
                                status=500)
