from django.shortcuts import redirect
from django.views.generic import TemplateView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper
import logging
from django.contrib.auth import get_user_model, login

logger = logging.getLogger(__name__)

class AuthView(TemplateView):
    def get_template_names(self):
        return ['auth/login.html']

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context.update({"layout_path": TemplateHelper.set_layout("layout_blank.html", context)})
        return context

    def dispatch(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access_token')

        if access_token:
            try:
                decoded_token = AccessToken(access_token)
                user_id = decoded_token['user_id']
                user = get_user_model().objects.get(id=user_id)

                if user:
                    from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

                    if BlacklistedToken.objects.filter(token=access_token).exists():
                        logger.debug("Token qora ro'yxatda mavjud")
                        return redirect("login")

                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect("index")
            except InvalidToken as e:
                logger.debug(f"Tokenni tekshirishda xatolik: {str(e)}")
            except Exception as e:
                logger.debug(f"Xatolik: {str(e)}")

        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        return redirect("index")
