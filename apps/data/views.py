from django.views.generic import TemplateView

from accounts.edu_models import University
from web_project import TemplateLayout


class DataView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Universitetlar ro'yxatini olish
        universities = University.objects.all()

        # Universitetlar ro'yxatini context ga qo'shish
        context['universities'] = universities

        return context
