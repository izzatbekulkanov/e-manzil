from django.contrib import admin
from django.urls import include, path
from web_project.views import SystemView

urlpatterns = [
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path("admin/", admin.site.urls),

    path("api/", include("api.urls")),
    path("data/", include("apps.data.urls")),
    # path("data/", include("apps.data.urls")),
    path("e-manzil/", include("apps.e_manzil.urls")),
    # path("data/", include("apps.data.urls")),


    # Dashboard urls
    path("", include("other.dashboards.urls")),

    # layouts urls
    path("", include("other.layouts.urls")),

    # FrontPages urls
    path("", include("other.front_pages.urls")),

    # FrontPages urls
    path("", include("other.mail.urls")),

    # Chat urls
    path("", include("other.chat.urls")),

    # Calendar urls
    path("", include("other.my_calendar.urls")),

    # kanban urls
    path("", include("other.kanban.urls")),

    # eCommerce urls
    path("", include("other.ecommerce.urls")),

    # Academy urls
    path("", include("other.academy.urls")),

    # Logistics urls
    path("", include("other.logistics.urls")),

    # Invoice urls
    path("", include("other.invoice.urls")),

    # User urls
    path("", include("other.users.urls")),

    # Access urls
    path("", include("other.access.urls")),

    # Pages urls
    path("", include("other.pages.urls")),

    # Auth urls
    path("", include("other.authentication.urls")),

    # Wizard urls
    path("", include("other.wizard_examples.urls")),

    # ModalExample urls
    path("", include("other.modal_examples.urls")),

    # Card urls
    path("", include("other.cards.urls")),

    # UI urls
    path("", include("other.ui.urls")),

    # Extended UI urls
    path("", include("other.extended_ui.urls")),

    # Icons urls
    path("", include("other.icons.urls")),

    # Forms urls
    path("", include("other.forms.urls")),

    # FormLayouts urls
    path("", include("other.form_layouts.urls")),

    # FormWizard urls
    path("", include("other.form_wizard.urls")),

    # FormValidation urls
    path("", include("other.form_validation.urls")),

    # Tables urls
    path("", include("other.tables.urls")),

    # Chart urls
    path("", include("other.charts.urls")),

    # Map urls
    path("", include("other.maps.urls")),

    # auth urls
    path("", include("auth.urls")),

    # transaction urls
    path("", include("other.transactions.urls")),
]

handler404 = SystemView.as_view(template_name="pages_misc_error.html", status=404)
handler403 = SystemView.as_view(template_name="pages_misc_not_authorized.html", status=403)
handler400 = SystemView.as_view(template_name="pages_misc_error.html", status=400)
handler500 = SystemView.as_view(template_name="pages_misc_error.html", status=500)
