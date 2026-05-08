from django.conf import settings
from django.contrib import admin
from django.urls import path

from django_music.views import HomeView, PublicProfileView, ProfileView, logout_view, RegistrationView
from django_music.api_views import ArtistListView

urlpatterns = [
    # Startseite — Anmeldeformular und Top-Songs
    path("", HomeView.as_view(), name="home"),

    # Öffentliche Profilseite — erreichbar über den Slug des Nutzers
    path("u/<slug:slug>/", PublicProfileView.as_view(), name="public_profile"),

    # Eingeloggter Bereich — Profil bearbeiten (Login erforderlich)
    path("profile/", ProfileView.as_view(), name="profile"),

    # Registrierung — neues Konto erstellen
    path("register/", RegistrationView.as_view(), name="register"),

    # Abmelden — Session beenden und zur Startseite weiterleiten
    path("logout/", logout_view, name="logout"),

    # Django Admin-Bereich
    path("admin/", admin.site.urls),

    # REST API — Künstlerliste (nur für angemeldete Nutzer)
    path("api/artists/", ArtistListView.as_view(), name="api_artists"),
]

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += debug_toolbar_urls()
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)