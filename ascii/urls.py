from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from ascii.core.views import IndexView
from ascii.fudan.views import FudanBBSView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("fudan/bbs/<path:path>", FudanBBSView.as_view(), name="fudan-bbs"),
    path("admin/", admin.site.urls),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    *staticfiles_urlpatterns(),
]
