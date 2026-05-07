from django.conf import settings
from django.contrib import admin
from django.urls import path

from django_music.views import HomeView, PublicProfileView, ProfileView, logout_view
from django_music.api_views import ArtistListView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("u/<slug:slug>/", PublicProfileView.as_view(), name="public_profile"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("logout/", logout_view, name="logout"),
    path("admin/", admin.site.urls),
    path("api/artists/", ArtistListView.as_view(), name="api_artists"),
]

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += debug_toolbar_urls()
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)