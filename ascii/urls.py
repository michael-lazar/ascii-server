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
from ascii.textmode.views import (
    TextmodeArtfileView,
    TextmodeArtistTagDetailView,
    TextmodeArtistTagListView,
    TextmodeContentTagDetailView,
    TextmodeContentTagListView,
    TextmodeGroupTagDetailView,
    TextmodeGroupTagListView,
    TextmodeIndexView,
    TextmodePackView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("textmode/", TextmodeIndexView.as_view(), name="textmode-index"),
    path("textmode/pack/<slug:pack>/", TextmodePackView.as_view(), name="textmode-pack"),
    path(
        "textmode/pack/<slug:pack>/a/<str:artfile>",
        TextmodeArtfileView.as_view(),
        name="textmode-artfile",
    ),
    path(
        "textmode/tags/group/",
        TextmodeGroupTagListView.as_view(),
        name="textmode-grouptag-list",
    ),
    path(
        "textmode/tags/group/<str:name>/",
        TextmodeGroupTagDetailView.as_view(),
        name="textmode-grouptag-detail",
    ),
    path(
        "textmode/tags/artist/",
        TextmodeArtistTagListView.as_view(),
        name="textmode-artisttag-list",
    ),
    path(
        "textmode/tags/artist/<str:name>/",
        TextmodeArtistTagDetailView.as_view(),
        name="textmode-artisttag-detail",
    ),
    path(
        "textmode/tags/content/",
        TextmodeContentTagListView.as_view(),
        name="textmode-contenttag-list",
    ),
    path(
        "textmode/tags/content/<str:name>/",
        TextmodeContentTagDetailView.as_view(),
        name="textmode-contenttag-detail",
    ),
    path("fudan/assets/<slug:slug>", FudanAssetFileView.as_view(), name="fudan-asset"),
    path("fudan/scratch/<slug:slug>", FudanScratchFileView.as_view(), name="fudan-scratch"),
    path("fudan/bbs/<path:path>/", FudanBBSMenuView.as_view(), name="fudan-bbs-menu"),
    path("fudan/bbs/<path:path>", FudanBBSDocumentView.as_view(), name="fudan-bbs-document"),
    path("admin/", admin.site.urls),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    *staticfiles_urlpatterns(),
]
