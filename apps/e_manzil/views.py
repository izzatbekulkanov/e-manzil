from django.views.generic import TemplateView

from accounts.edu_models import University
from web_project import TemplateLayout


class E_manzilView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context
