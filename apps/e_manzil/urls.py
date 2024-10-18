from django.contrib.auth.decorators import login_required
from django.urls import path
from config.custom_required import jwt_login_required  # Ensure correct import path
from apps.e_manzil.views import E_manzilView

urlpatterns = [
    path(
        "dormitory/",
        login_required(E_manzilView.as_view(template_name="dormitoryAdress.html")),
        name="e-manzil-dormitory",
    ),
    path(
        "building/",
        login_required(E_manzilView.as_view(template_name="building.html")),
        name="e-manzil-building",
    ),
]