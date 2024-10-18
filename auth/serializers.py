from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['name'] = user.get_full_name()
        return token

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')
        password = attrs.get('password')

        if not (email or username) or not password:
            raise serializers.ValidationError(
                {'non_field_errors': ['Email yoki username va parolni kiriting.']}
            )

        user = authenticate(request=self.context.get('request'), username=username, email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                {'non_field_errors': ['Email/username yoki parol noto‘g‘ri.']}
            )

        validated_data = super().validate(attrs)
        return validated_data

class UserSerializer(serializers.Serializer):
    access_token = serializers.CharField()