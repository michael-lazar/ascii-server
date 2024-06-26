from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from ascii.core.views import IndexView
from ascii.fudan.views import (
    FudanAssetFileView,
    FudanBBSDocumentView,
    FudanBBSMenuView,
    FudanScratchFileView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("fudan/assets/<slug:slug>", FudanAssetFileView.as_view(), name="fudan-asset"),
    path("fudan/scratch/<slug:slug>", FudanScratchFileView.as_view(), name="fudan-scratch"),
    path("fudan/bbs/<path:path>/", FudanBBSMenuView.as_view(), name="fudan-bbs-menu"),
    path("fudan/bbs/<path:path>", FudanBBSDocumentView.as_view(), name="fudan-bbs-document"),
    path("admin/", admin.site.urls),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    *staticfiles_urlpatterns(),
]
