from datetime import datetime

from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Roles
from config.settings import (
    CLIENT_SECRET,
    CLIENT_ID,
    REDIRECT_URI,
    RESOURCE_OWNER_URL,
    TOKEN_URL,
    AUTHORIZE_URL,
)
from accounts.edu_models import University
from auth.client import oAuth2Client


class OAuthAuthorizationView(APIView):
    def get(self, request, *args, **kwargs):
        client = oAuth2Client(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            authorize_url=AUTHORIZE_URL,
            token_url=TOKEN_URL,
            resource_owner_url=RESOURCE_OWNER_URL
        )
        authorization_url = client.get_authorization_url()

        return redirect(authorization_url)
    # Foydalanuvchini avtorizatsiya sahifasiga yo'naltirish


class OAuthCallbackView(APIView):
    def get(self, request, *args, **kwargs):
        full_info = {}
        auth_code = request.query_params.get('code')
        if not auth_code:
            return Response(
                {
                    'status': False,
                    'error': 'Authorization code is missing'
                },
                status=status.HTTP_400_BAD_REQUEST)

        client = oAuth2Client(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            authorize_url=AUTHORIZE_URL,
            token_url=TOKEN_URL,
            resource_owner_url=RESOURCE_OWNER_URL
        )
        access_token_response = client.get_access_token(auth_code)

        if 'access_token' in access_token_response:
            access_token = access_token_response['access_token']
            user_details = client.get_user_details(access_token)
            full_info['details'] = user_details
            full_info['token'] = access_token
            # Foydalanuvchi modeliga foydalanuvchi ma'lumotlarini qo'shish
            CustomUser = get_user_model()
            # Foydalanuvchi ma'lumotlarini olish
            employee_id_number = user_details.get('employee_id_number', None)
            old_date_str = user_details.get('birth_date', '')
            if old_date_str:
                # Convert the old date string to datetime object
                old_date = datetime.strptime(old_date_str, '%d-%m-%Y')

                # Convert datetime object to new string format 'YYYY-MM-DD'
                new_date_str = old_date.strftime('%Y-%m-%d')
            else:
                new_date_str = None
            existing_user = CustomUser.objects.filter(employee_id_number=employee_id_number).first()
            if existing_user:
                # Tekshirish: employee_id_number ga teng foydalanuvchi mavjudmi?
                id_number = user_details.get('id', '')  # id bilan
                username = ('hodim' + str(id_number)).lower()
                # Foydalanuvchi malumotlarini yangilash
                existing_user.full_name = user_details.get('name', '')
                existing_user.first_name = user_details.get('firstname', '')
                existing_user.second_name = user_details.get('surname', '')
                existing_user.username = username
                existing_user.third_name = user_details.get('patronymic', '')
                existing_user.birth_date = new_date_str
                existing_user.phone_number = user_details.get('phone', '')
                existing_user.token = access_token
                existing_user.image = user_details.get('picture', '')

                # Rollarni yangilash
                if 'roles' in user_details:
                    existing_user.hemis_role.clear()  # Avvalgi rollarni olib tashlash
                    roles = user_details['roles']
                    for role in roles:
                        role_code = role.get('code', '')
                        role_name = role.get('name', '')
                        role_instance, created = Roles.objects.get_or_create(code=role_code, name=role_name)
                        existing_user.hemis_role.add(role_instance)

                existing_user.save()
                oauth_login(request, existing_user.email, existing_user)  # Faydalanuvchini login qiling
            else:
                # Yangi foydalanuvchi yaratish
                university_code = user_details.get('university_id', '')
                university = University.objects.get(code=university_code)
                id_number = user_details.get('id', '')  # id bilan
                username = ('hodim' + str(id_number)).lower()
                email = user_details.get('email', None)

                if not email:
                    email = f'hodim{id_number}@namdpi.uz'.lower()
                user_type = user_details.get('type', '')
                if user_type == 'teacher':
                    user_type = '3'  # o'qituvchi
                elif user_type == 'employee':
                    user_type = '2'  # Hodim
                elif user_type == 'student':
                    user_type = '1'  # Talaba
                user, created = CustomUser.objects.update_or_create(
                    email=email,
                    defaults={
                        'email': email,  # Foydalanuvchining email manzili
                        'employee_id_number': employee_id_number,
                        'university': university,
                        'full_id': employee_id_number,
                        'full_name': user_details.get('name', ''),
                        'first_name': user_details.get('firstname', ''),
                        'second_name': user_details.get('surname', ''),
                        'username': username,
                        'third_name': user_details.get('patronymic', ''),
                        'birth_date': new_date_str,
                        'phone_number': user_details.get('phone', ''),
                        'token': access_token,
                        'image': user_details.get('picture', ''),
                        'now_role': 'Employee',
                        'user_type': user_type,
                        'is_followers_book': True,
                        'is_student': False,
                        'is_employee': True,
                        # Boshqa ma'lumotlar
                    }
                )

                # Ro'larni qo'shish
                if 'roles' in user_details:
                    roles = user_details['roles']
                    for role in roles:
                        role_code = role.get('code', '')
                        role_name = role.get('name', '')
                        role_instance, created = Roles.objects.get_or_create(code=role_code, name=role_name)
                        user.hemis_role.add(role_instance)

                # Foydalanuvchini "employee" guruhiga qo'shish
                employee_group, created = Group.objects.get_or_create(name='Employee')
                user.groups.add(employee_group)

                oauth_login(request, email, user)  # Faydalanuvchini login qiling

            # return Response(full_info, status=status.HTTP_200_OK)
            return redirect('studentPageView')
        else:
            return Response(
                {
                    'status': False,
                    'error': 'Failed to obtain access token'
                },
                status=status.HTTP_400_BAD_REQUEST
            )


def oauth_login(request, email, user):
    # Faydalanuvchi obyektini olish
    # user = get_object_or_404(CustomUser, email=email)

    # Faydalanuvchini avtorizatsiya qilish
    user.backend = 'django.contrib.auth.backends.ModelBackend'  # Faydalanuvchi uchun kerakli backendni aniqlash
    login(request, user)
