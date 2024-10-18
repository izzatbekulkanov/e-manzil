from django.contrib.auth.backends import BaseBackend
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import CustomUser  # CustomUser modelini import qiling

class CustomBackend(BaseBackend):
    """
    Custom authentication backend that allows users to log in with their email or username.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        print("CustomBackend: authenticate metodi ishga tushdi")
        print(f"Received username: {username}, password: {'*' * len(password) if password else None}")

        # Username yoki parol bo'sh bo'lsa, hech narsa qilmaymiz
        if not username or not password:
            print("Username yoki parol bo'sh.")
            return None

        try:
            # Elektron pochta yoki foydalanuvchi nomi asosida foydalanuvchini qidiradi
            if '@' in username:
                print("Elektron pochta orqali foydalanuvchini qidirish")
                user = CustomUser.objects.get(email=username)
            else:
                print("Foydalanuvchi nomi orqali foydalanuvchini qidirish")
                user = CustomUser.objects.get(username=username)
            print(f"Foydalanuvchi topildi: {user}")
        except ObjectDoesNotExist:
            print("Foydalanuvchi topilmadi")
            return None

        # Parolni tekshiradi va to'g'ri bo'lsa foydalanuvchini qaytaradi
        if user is not None and user.check_password(password) and self.user_can_authenticate(user):
            print("Parol to'g'ri, foydalanuvchi autentifikatsiya qilindi")
            return user
        print("Parol noto'g'ri yoki foydalanuvchi faol emas")
        return None

    def get_user(self, user_id):
        """
        Foydalanuvchi ID orqali foydalanuvchini qaytaradi.
        """
        print(f"get_user: user_id {user_id} bilan foydalanuvchini olishga harakat qilmoqda")
        try:
            user = CustomUser.objects.get(pk=user_id)
            print(f"Foydalanuvchi topildi: {user}")
        except CustomUser.DoesNotExist:
            print("Foydalanuvchi topilmadi")
            return None

        return user if self.user_can_authenticate(user) else None

    def user_can_authenticate(self, user):
        """
        Foydalanuvchi faol yoki nofaol ekanligini tekshiradi.
        """
        is_active = user.is_active
        print(f"user_can_authenticate: Foydalanuvchi {'faol' if is_active else 'nofaal'}")
        return is_active
