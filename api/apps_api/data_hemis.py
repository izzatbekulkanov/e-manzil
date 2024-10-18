import requests
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from accounts.edu_models import University, EducationType, Department, Specialty, EducationForm, Curriculum, \
    EducationLang, GroupUniver
from django.http import JsonResponse


class UpdateUniversityView(View):

    def get(self, request, *args, **kwargs):
        url = 'https://student.namspi.uz/rest/v1/public/university-list?page=20&limit=200'
        headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer cbdfefbb283db3a219a7e7dcefd620b4'
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            universities = data.get('data', [])
            updated_count = 0  # Yangilangan universitetlar soni

            for university_data in universities:
                code = university_data.get('code', '')
                name = university_data.get('name', '')
                api_url = university_data.get('api_url', '')
                student_url = university_data.get('student_url', '')
                employee_url = university_data.get('employee_url', '')

                # Universitet mavjudligini tekshirish
                existing_university = University.objects.filter(code=code).first()
                if existing_university:
                    # Universitetni yangilash
                    existing_university.name = name
                    existing_university.api_url = api_url
                    existing_university.student_url = student_url
                    existing_university.employee_url = employee_url
                    existing_university.save()
                    updated_count += 1  # Yangilangan universitetlar sonini oshirish
                else:
                    # Yangi universitet yaratish
                    University.objects.create(
                        code=code,
                        name=name,
                        api_url=api_url,
                        student_url=student_url,
                        employee_url=employee_url
                    )
                    updated_count += 1  # Yangi universitet qo‘shilganligi uchun sonini oshirish

            return JsonResponse({"message": "Universitetlar ro'yxati yangilandi.", "updated_count": updated_count})
        else:
            return JsonResponse(
                {"message": "Universitetlar ro'yxatini yangilashda xatolik yuz berdi.", "updated_count": 0},
                status=response.status_code)


class SaveHemisKeyView(View):
    def post(self, request, *args, **kwargs):
        university_id = request.POST.get('university_id')
        api_token = request.POST.get('api_token')

        if university_id and api_token:
            try:
                university = University.objects.get(id=university_id)
                university.api_token = api_token
                university.save()
                return JsonResponse({'status': 'success', 'message': 'API kalit muvaffaqiyatli saqlandi.'})
            except University.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Universitet topilmadi.'}, status=404)
        else:
            return JsonResponse({'status': 'error', 'message': 'Universitet ID yoki API token yetishmaydi.'},
                                status=400)


class UniversityWithApiTokenView(View):
    def get(self, request, *args, **kwargs):
        # Fetch universities with a non-null and non-empty api_token
        universities = University.objects.filter(api_token__isnull=False).exclude(api_token='none')

        # Prepare data for JSON response
        data = list(universities.values('code', 'name', 'api_token', 'is_active'))

        return JsonResponse(data, safe=False)


@csrf_exempt
def delete_university_api_token(request):
    if request.method == 'POST':
        university_code = request.POST.get('university_code')
        data = request.POST.get('data')

        print(university_code, data)
        if university_code:
            try:
                university = University.objects.get(code=university_code)
                university.api_token = 'none'
                university.save()
                return JsonResponse({'status': 'success', 'message': 'API token successfully deleted.'})
            except University.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'University not found.'}, status=404)
        return JsonResponse({'status': 'error', 'message': 'Invalid university ID.'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


class SetUniversityActiveView(View):
    def post(self, request, *args, **kwargs):
        university_code = request.POST.get('university_code')

        if university_code:
            try:
                # Deactivate all currently active universities
                University.objects.filter(is_active=True).update(is_active=False)

                # Activate the selected university
                university = University.objects.get(code=university_code)
                university.is_active = True
                university.save()

                return JsonResponse({'success': True, 'message': 'University status updated to active.'})
            except University.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'University not found.'}, status=404)
        return JsonResponse({'success': False, 'message': 'Invalid request.'}, status=400)


class DataFetchAndSaveView(View):
    def fetch_data_from_api(self, endpoint):
        try:
            university = University.objects.get(is_active=True)
            api_url = university.api_url
            api_token = university.api_token
            url = f'{api_url}{endpoint}'
            headers = {
                'accept': 'application/json',
                'Authorization': f'Bearer {api_token}'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except University.DoesNotExist:

            raise Exception("Active university not found.")
        except requests.RequestException as e:

            raise Exception(f"Failed to fetch data from the API: {e}")

    def update_or_create_department(self, data):
        codeID = data.get('id')
        name = data.get('name')

        department, created = Department.objects.update_or_create(
            codeID=codeID,
            defaults={'name': name}
        )
        return department, created

    def save_departments(self):
        try:
            data = self.fetch_data_from_api('data/department-list?page=20&limit=200')
            items = data.get('data', {}).get('items', [])
            for item in items:
                self.update_or_create_department(item)
            return JsonResponse({'success': True, 'message': 'Departments saved successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    def save_specialty(self):
        try:
            data = self.fetch_data_from_api('data/specialty-list?page=20&limit=200')
            items = data.get('data', {}).get('items', [])
            for item in items:
                education_type_name = item.get('educationType', {}).get('name')
                education_type_code = item.get('educationType', {}).get('code')
                EducationType.objects.update_or_create(
                    name=education_type_name,
                    defaults={'code': education_type_code}
                )
                department_id = item.get('department', {}).get('id')
                department, _ = Department.objects.get_or_create(codeID=department_id)
                education_type, _ = EducationType.objects.get_or_create(code=education_type_code)
                Specialty.objects.update_or_create(
                    codeID=item.get('id'),
                    defaults={
                        'code': item.get('code'),
                        'name': item.get('name'),
                        'department': department,
                        'educationType': education_type
                    }
                )
            return JsonResponse({'success': True, 'message': 'Specialties saved successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    def save_curriculum(self):
        try:
            data = self.fetch_data_from_api('data/curriculum-list?page=20&limit=200')
            items = data.get('data', {}).get('items', [])
            for item in items:
                education_form_name = item.get('educationForm', {}).get('name')
                education_form_code = item.get('educationForm', {}).get('code')
                EducationForm.objects.get_or_create(
                    name=education_form_name,
                    defaults={'code': education_form_code}
                )
                specialty_id = item.get('specialty', {}).get('id')
                specialty, _ = Specialty.objects.get_or_create(codeID=specialty_id)
                education_type_code = item.get('educationType', {}).get('code')
                education_type, _ = EducationType.objects.get_or_create(code=education_type_code)
                education_form = EducationForm.objects.get(code=education_form_code)
                Curriculum.objects.update_or_create(
                    codeID=item.get('id'),
                    defaults={
                        'name': item.get('name'),
                        'specialty': specialty,
                        'educationType': education_type,
                        'educationForm': education_form,
                        'semester_count': item.get('semester_count'),
                        'education_period': item.get('education_period'),
                    }
                )
            return JsonResponse({'success': True, 'message': 'Curriculums saved successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    def save_groups(self):
        try:
            page_number = 1
            while True:
                data = self.fetch_data_from_api(f'data/group-list?page={page_number}&limit=200')
                items = data.get('data', {}).get('items', [])
                pagination_data = data.get('data', {}).get('pagination')
                page_count = pagination_data.get('pageCount')

                for item in items:
                    education_lang_name = item.get('educationLang', {}).get('name')
                    education_lang_code = item.get('educationLang', {}).get('code')
                    defaults = {'code': education_lang_code}
                    obj, created = EducationLang.objects.get_or_create(
                        name=education_lang_name,
                        defaults=defaults
                    )
                    department_code = item.get('department', {}).get('id')
                    department, _ = Department.objects.get_or_create(codeID=department_code)
                    specialty_id = item.get('specialty', {}).get('id')
                    specialty, _ = Specialty.objects.get_or_create(codeID=specialty_id)
                    GroupUniver.objects.update_or_create(
                        codeID=item.get('id'),
                        defaults={
                            'name': item.get('name'),
                            'educationLang': obj,
                            'department': department,
                            'specialty': specialty,
                        }
                    )

                if page_number >= page_count:
                    break
                else:
                    page_number += 1

            return JsonResponse({'success': True, 'message': 'Groups saved successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        if action == 'save_departments':
            return self.save_departments()
        elif action == 'save_specialty':
            return self.save_specialty()
        elif action == 'save_curriculum':
            return self.save_curriculum()
        elif action == 'save_groups':
            return self.save_groups()
        else:
            return JsonResponse({'success': False, 'message': 'Invalid action.'}, status=400)


class UniversityDataView(View):
    def get(self, request, *args, **kwargs):
        universities = list(University.objects.filter(is_active=True).values('name', 'code', 'employee_url'))
        curriculums = list(Curriculum.objects.all().values('name', 'codeID'))
        specialties = list(Specialty.objects.all().values('name', 'code'))
        groups = list(GroupUniver.objects.all().values('name', 'codeID'))
        departments = list(Department.objects.all().values('name', 'code'))

        data = {
            'universities': {
                'count': len(universities),
                'items': universities
            },
            'curriculums': {
                'count': len(curriculums),
                'items': curriculums
            },
            'specialties': {
                'count': len(specialties),
                'items': specialties
            },
            'academic_groups': {
                'count': len(groups),
                'items': groups
            },
            'departments': {
                'count': len(departments),
                'items': departments
            }
        }

        return JsonResponse(data)