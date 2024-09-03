from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

from ascii.core.views import IndexView
from ascii.fudan.views import (
    FudanAssetFileView,
    FudanBBSDocumentView,
    FudanBBSMenuView,
    FudanScratchFileView,
)
from ascii.textmode.views import (
    TextmodeArtfileView,
    TextmodeIndexView,
    TextmodePackListView,
    TextmodePackView,
    TextmodeTagCategoryListView,
    TextmodeTagListView,
    TextmodeTagView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("textmode/", TextmodeIndexView.as_view(), name="textmode-index"),
    path("textmode/pack/", TextmodePackListView.as_view(), name="textmode-pack-list"),
    path("textmode/pack/<slug:pack>/", TextmodePackView.as_view(), name="textmode-pack"),
    path("textmode/tags/", TextmodeTagListView.as_view(), name="textmode-tag-list"),
    path(
        "textmode/tags/<slug:category>/",
        TextmodeTagCategoryListView.as_view(),
        name="textmode-tag-category-list",
    ),
    path(
        "textmode/tags/<slug:category>/<str:name>/",
        TextmodeTagView.as_view(),
        name="textmode-tag",
    ),
    path(
        "textmode/pack/<slug:pack>/a/<str:artfile>",
        TextmodeArtfileView.as_view(),
        name="textmode-artfile",
    ),
    path("fudan/assets/<slug:slug>", FudanAssetFileView.as_view(), name="fudan-asset"),
    path("fudan/scratch/<slug:slug>", FudanScratchFileView.as_view(), name="fudan-scratch"),
    path("fudan/bbs/<path:path>/", FudanBBSMenuView.as_view(), name="fudan-bbs-menu"),
    path("fudan/bbs/<path:path>", FudanBBSDocumentView.as_view(), name="fudan-bbs-document"),
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    *staticfiles_urlpatterns(),
]
