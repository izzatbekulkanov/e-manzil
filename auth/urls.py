from django.urls import path

from .hemis_employee.views import OAuthCallbackView, OAuthAuthorizationView
from .login.views import LoginView
from .logout.logout import LogoutView
from .verify_email.views import VerifyEmailTokenView, VerifyEmailView, SendVerificationView
from .views import AuthView

urlpatterns = [
    path('login/', AuthView.as_view(), name='login'),
    path('api/login/', LoginView.as_view(), name='enter'),

    path("logout/", LogoutView.as_view(), name="logout"),

    path("verify_email/", VerifyEmailView.as_view(template_name="auth/verify_email.html"), name="verify-email-page"),

    path("verify/email/<str:token>/", VerifyEmailTokenView.as_view(), name="verify-email"),

    path("send_verification/", SendVerificationView.as_view(), name="send-verification"),


    path('authorize/', OAuthAuthorizationView.as_view(), name='oauth_authorize'),
    path('callback', OAuthCallbackView.as_view(), name='oauth_callback'),



]
