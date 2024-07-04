# Define urlpatterns in project/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView


urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", include("web.urls", namespace="web")),
        path("accounts/", include("registration.backends.simple.urls")),

        path("accounts/", include("accounts.urls", namespace="accounts")),

        path("sitemap.xml", TemplateView.as_view(template_name="sitemap.xml", content_type="text/xml")),
        path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),

        # dash
        path("login/", include("core.urls", namespace="core")),
        path("login/", include("user_sessions.urls", "user_sessions")),

        path("products/", include("product.urls", "product")),

        # path("orders/", include("order.urls", "order")),

    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

PROJECT_NAME = settings.APP_SETTINGS.get("site_name")
admin.site.site_header = _("%(project_name)s Administration") % {"project_name": PROJECT_NAME}
admin.site.site_title = _("%(project_name)s Admin Portal") % {"project_name": PROJECT_NAME}
admin.site.index_title = _("Welcome to %(project_name)s Admin Portal") % {"project_name": PROJECT_NAME}
