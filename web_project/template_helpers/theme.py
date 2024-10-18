from django.conf import settings
from pprint import pprint
import os
from importlib import import_module, util


# Asosiy TemplateHelper sinfi
class TemplateHelper:
    # TEMPLATE_CONFIG yordamida Template kontekstini ishga tushirish
    def init_context(context):
        context.update(
            {
                "layout": settings.TEMPLATE_CONFIG.get("layout"),  # Sayt tartibini o'rnatish (masalan, gorizontal yoki vertikal)
                "theme": settings.TEMPLATE_CONFIG.get("theme"),  # Sayt mavzusini o'rnatish (masalan, quyuq yoki yorqin)
                "style": settings.TEMPLATE_CONFIG.get("style"),  # Sayt uslubini o'rnatish (CSS uslublari)
                "rtl_support": settings.TEMPLATE_CONFIG.get("rtl_support"),  # O'ngdan chapga (RTL) qo'llab-quvvatlash
                "rtl_mode": settings.TEMPLATE_CONFIG.get("rtl_mode"),  # RTL rejimi
                "has_customizer": settings.TEMPLATE_CONFIG.get("has_customizer"),  # Mavzu sozlash moslamasi mavjudligini tekshirish
                "display_customizer": settings.TEMPLATE_CONFIG.get("display_customizer"),  # Mavzu sozlash moslamasini ko'rsatish yoki yashirish
                "content_layout": settings.TEMPLATE_CONFIG.get("content_layout"),  # Kontent tartibini o'rnatish (masalan, keng yoki ixcham)
                "navbar_type": settings.TEMPLATE_CONFIG.get("navbar_type"),  # Navbar turi (statik yoki mahkamlangan)
                "header_type": settings.TEMPLATE_CONFIG.get("header_type"),  # Sarlavha turi (statik yoki mahkamlangan)
                "menu_fixed": settings.TEMPLATE_CONFIG.get("menu_fixed"),  # Menyu mahkamlanganligini tekshirish
                "menu_collapsed": settings.TEMPLATE_CONFIG.get("menu_collapsed"),  # Menyu qisqartirilganligini tekshirish
                "footer_fixed": settings.TEMPLATE_CONFIG.get("footer_fixed"),  # Footer mahkamlanganligini tekshirish
                "show_dropdown_onhover": settings.TEMPLATE_CONFIG.get(
                    "show_dropdown_onhover"
                ),  # Dropdownni hoverda ko'rsatish
                "customizer_controls": settings.TEMPLATE_CONFIG.get(
                    "customizer_controls"
                ),  # Mavzuni sozlash moslamasi boshqaruv elementlari
            }
        )
        return context

    # ? Kontekst o'zgaruvchilarini shablonlar uchun mos sinf/qiymat/o'zgaruvchilarga xaritalash
    def map_context(context):
        #! Sarlavha turi (faqat gorizontal rejimda)
        if context.get("layout") == "horizontal":
            if context.get("header_type") == "fixed":
                context["header_type_class"] = "layout-menu-fixed"
            elif context.get("header_type") == "static":
                context["header_type_class"] = ""
            else:
                context["header_type_class"] = ""
        else:
            context["header_type_class"] = ""

        #! Navbar turi (faqat vertikal/front rejimda)
        if context.get("layout") != "horizontal":
            if context.get("navbar_type") == "fixed":
                context["navbar_type_class"] = "layout-navbar-fixed"
            elif context.get("navbar_type") == "static":
                context["navbar_type_class"] = ""
            else:
                context["navbar_type_class"] = "layout-navbar-hidden"
        else:
            context["navbar_type_class"] = ""

        # Menyu qisqartirilgan
        context["menu_collapsed_class"] = (
            "layout-menu-collapsed" if context.get("menu_collapsed") else ""
        )

        #! Menyu mahkamlangan (faqat vertikal rejimda)
        if context.get("layout") == "vertical":
            if context.get("menu_fixed") is True:
                context["menu_fixed_class"] = "layout-menu-fixed"
            else:
                context["menu_fixed_class"] = ""

        # Footer mahkamlangan
        context["footer_fixed_class"] = (
            "layout-footer-fixed" if context.get("footer_fixed") else ""
        )

        # RTL qo'llab-quvvatlanadigan shablon
        context["rtl_support_value"] = "/rtl" if context.get("rtl_support") else ""

        # RTL rejimi/tartibi
        context["rtl_mode_value"], context["text_direction_value"] = (
            ("rtl", "rtl") if context.get("rtl_mode") else ("ltr", "ltr")
        )

        #! Hoverda dropdownni ko'rsatish (Gorizontal menyu)
        context["show_dropdown_onhover_value"] = (
            "true" if context.get("show_dropdown_onhover") else "false"
        )

        # Mavzu sozlash moslamasini ko'rsatish
        context["display_customizer_class"] = (
            "" if context.get("display_customizer") else "customizer-hide"
        )

        # Kontent tartibi
        if context.get("content_layout") == "wide":
            context["container_class"] = "container-fluid"
            context["content_layout_class"] = "layout-wide"
        else:
            context["container_class"] = "container-xxl"
            context["content_layout_class"] = "layout-compact"

        # Ajratilgan Navbar
        if context.get("navbar_detached") == True:
            context["navbar_detached_class"] = "navbar-detached"
        else:
            context["navbar_detached_class"] = ""

    # Mavzu o'zgaruvchilarini doira bo'yicha olish
    def get_theme_variables(scope):
        return settings.THEME_VARIABLES[scope]

    # Mavzu konfiguratsiyasini doira bo'yicha olish
    def get_theme_config(scope):
        return settings.TEMPLATE_CONFIG[scope]

    # Joriy sahifa tartibini o'rnatish va tartibning bootstrap faylini ishga tushirish
    def set_layout(view, context={}):
        # Ko'rinish yo'lidan tartibni chiqarish
        layout = os.path.splitext(view)[0].split("/")[0]

        # Modul yo'lini olish
        module = f"templates.{settings.THEME_LAYOUT_DIR.replace('/', '.')}.bootstrap.{layout}"

        # Bootstrap fayli mavjudligini tekshirish
        if util.find_spec(module) is not None:
            # Avtomatik import qilish va mavzudan default bootstrap.py faylini ishga tushirish
            TemplateBootstrap = TemplateHelper.import_class(
                module, f"TemplateBootstrap{layout.title().replace('_', '')}"
            )
            TemplateBootstrap.init(context)
        else:
            module = f"templates.{settings.THEME_LAYOUT_DIR.replace('/', '.')}.bootstrap.default"

            TemplateBootstrap = TemplateHelper.import_class(
                module, "TemplateBootstrapDefault"
            )
            TemplateBootstrap.init(context)

        return f"{settings.THEME_LAYOUT_DIR}/{view}"

    # Modulli sinfni satr orqali import qilish
    def import_class(fromModule, import_className):
        pprint(f"{import_className} sinfi {fromModule} dan yuklanmoqda")
        module = import_module(fromModule)
        return getattr(module, import_className)