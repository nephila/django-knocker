import django.views.i18n
import django.views.static
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path

from .views import PostDetailView, PostListView, PostMixinDetailView

admin.autodiscover()

urlpatterns = [
    re_path(
        r"^media/(?P<path>.*)$",
        django.views.static.serve,  # NOQA
        {"document_root": settings.MEDIA_ROOT, "show_indexes": True},
    ),
    re_path(r"^admin/", admin.site.urls),  # NOQA
    re_path(r"^jsi18n/(?P<packages>\S+?)/$", django.views.i18n.JavaScriptCatalog.as_view()),  # NOQA
    re_path(
        r"^mixin/(?P<slug>\w[-\w]*)/$",
        PostMixinDetailView.as_view(),
        name="post-detail-mixinx",
    ),
    re_path(r"^(?P<slug>\w[-\w]*)/$", PostDetailView.as_view(), name="post-detail"),
    path("", PostListView.as_view(), name="post-list"),
]
