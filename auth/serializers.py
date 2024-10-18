from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        if not (username or email) or not password:
            raise serializers.ValidationError(
                {'non_field_errors': ['Email yoki username va parolni kiriting.']}
            )

        # Foydalanuvchini autentifikatsiya qilish: email yoki username orqali
        user = None
        if username:
            user = authenticate(username=username, password=password)
        if not user and email:
            user = authenticate(username=email, password=password)  # Foydalanuvchi email orqali autentifikatsiya qilinadi

        if user is None:
            raise serializers.ValidationError(
                {'non_field_errors': ['Email/username yoki parol noto‘g‘ri.']}
            )

        validated_data = super().validate(attrs)
        return validated_data
