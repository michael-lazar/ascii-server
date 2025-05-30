from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, register_converter
from django.views.generic.base import RedirectView

from ascii.core.converters import DateConverter
from ascii.core.views import IndexView
from ascii.fudan.views import (
    FudanAssetFileView,
    FudanBBSDocumentView,
    FudanBBSMenuView,
    FudanScratchFileView,
)
from ascii.huku.views import (
    HukuIndexView,
    HukuMLTArtworkView,
    HukuMLTDirectoryView,
    HukuMLTFileDownloadView,
    HukuMLTFileView,
)
from ascii.mozz.views import MozzArtPostView, MozzIndexView, MozzScrollFileView
from ascii.textmode.views import (
    TextModeArtCollectionListView,
    TextModeArtCollectionView,
    TextmodeArtFileView,
    TextModeArtistAutocomplete,
    TextModeContentAutocomplete,
    TextModeGroupAutocomplete,
    TextmodeIndexView,
    TextModePackAutocomplete,
    TextmodePackListView,
    TextmodePackView,
    TextmodePackYearListView,
    TextModeSearchView,
    TextmodeTagCategoryListView,
    TextmodeTagListView,
    TextmodeTagView,
)

register_converter(DateConverter, "date")


urlpatterns = [
    path(
        "",
        IndexView.as_view(),
        name="index",
    ),
    path(
        "textmode/",
        TextmodeIndexView.as_view(),
        name="textmode-index",
    ),
    path(
        "textmode/search/",
        TextModeSearchView.as_view(),
        name="textmode-search",
    ),
    path(
        "textmode/pack/",
        TextmodePackListView.as_view(),
        name="textmode-pack-list",
    ),
    path(
        "textmode/pack/<int:year>/",
        TextmodePackYearListView.as_view(),
        name="textmode-pack-year-list",
    ),
    path(
        "textmode/pack/<int:year>/<str:pack>/",
        TextmodePackView.as_view(),
        name="textmode-pack",
    ),
    path(
        "textmode/tags/",
        TextmodeTagListView.as_view(),
        name="textmode-tag-list",
    ),
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
        "textmode/pack/<int:year>/<str:pack>/a/<str:artfile>",
        TextmodeArtFileView.as_view(),
        name="textmode-artfile",
    ),
    path(
        "textmode/collection/",
        TextModeArtCollectionListView.as_view(),
        name="textmode-collection-list",
    ),
    path(
        "textmode/collection/<slug:slug>/",
        TextModeArtCollectionView.as_view(),
        name="textmode-collection",
    ),
    path(
        "textmode/autocomplete/artist/",
        TextModeArtistAutocomplete.as_view(),
        name="textmode-artist-autocomplete",
    ),
    path(
        "textmode/autocomplete/group/",
        TextModeGroupAutocomplete.as_view(),
        name="textmode-group-autocomplete",
    ),
    path(
        "textmode/autocomplete/content/",
        TextModeContentAutocomplete.as_view(),
        name="textmode-content-autocomplete",
    ),
    path(
        "textmode/autocomplete/pack/",
        TextModePackAutocomplete.as_view(),
        name="textmode-pack-autocomplete",
    ),
    path(
        "fudan/",
        RedirectView.as_view(url="bbs/groups/rec.faq/ANSI/"),
        name="fudan-index",
    ),
    path(
        "fudan/assets/<slug:slug>",
        FudanAssetFileView.as_view(),
        name="fudan-asset",
    ),
    path(
        "fudan/scratch/<slug:slug>",
        FudanScratchFileView.as_view(),
        name="fudan-scratch",
    ),
    path(
        "fudan/bbs/<path:path>/",
        FudanBBSMenuView.as_view(),
        name="fudan-bbs-menu",
    ),
    path(
        "fudan/bbs/<path:path>",
        FudanBBSDocumentView.as_view(),
        name="fudan-bbs-document",
    ),
    path(
        "huku/",
        HukuIndexView.as_view(),
        name="huku-index",
    ),
    path(
        "huku/mlt/",
        HukuMLTDirectoryView.as_view(),
        name="huku-mlt-directory-index",
    ),
    path(
        "huku/mlt/<path:path>/",
        HukuMLTDirectoryView.as_view(),
        name="huku-mlt-directory",
    ),
    path(
        "huku/mlt/<path:path>",
        HukuMLTFileView.as_view(),
        name="huku-mlt-file",
    ),
    path(
        "huku/artwork/<slug:slug>/",
        HukuMLTArtworkView.as_view(),
        name="huku-mlt-artwork",
    ),
    path(
        "huku/raw/<path:path>",
        HukuMLTFileDownloadView.as_view(),
        name="huku-mlt-file-download",
    ),
    path(
        "mozz/",
        MozzIndexView.as_view(),
        name="mozz-index",
    ),
    path(
        "mozz/posts/<date:date>/<slug:slug>/",
        MozzArtPostView.as_view(),
        name="mozz-art-post",
    ),
    path(
        "mozz/scroll/<slug:slug>.txt",
        MozzScrollFileView.as_view(),
        name="mozz-scroll-file",
    ),
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    *staticfiles_urlpatterns(),
]

if not settings.TESTING:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
