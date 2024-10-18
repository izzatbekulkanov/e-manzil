from django.urls import path
from apps.data.views import DataView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path("hemis/" , (DataView.as_view(template_name="hemis_data.html")), name="hemis-data"),
]
