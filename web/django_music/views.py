from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import FormView, TemplateView, UpdateView
from django.urls import reverse_lazy

from django_music.forms import LoginForm, ProfileForm, RegistrationForm
from django_music.models import Song, User

class HomeView(FormView):
    """
    Startseite der Anwendung.

    Zeigt das Anmeldeformular und die 5 beliebtesten Songs (nach Anzahl der Fans).
    Bereits angemeldete Nutzer werden direkt zur Profilseite weitergeleitet.
    Die Suche nach Nutzern erfolgt über den GET-Parameter 'q'.
    """

    template_name = "home.html"
    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):
        """Bereits angemeldete Nutzer zur Profilseite weiterleiten."""
        if request.user.is_authenticated:
            return redirect("profile")
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        """
        Das request-Objekt an das Formular übergeben.
        AuthenticationForm benötigt dies zur Nutzerverifizierung.
        """
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs
    
    def form_valid(self, form):
        """Bei erfolgreicher Anmeldung den Nutzer einloggen und weiterleiten."""
        login(self.request, form.get_user())
        return redirect("profile")

    def get_context_data(self, **kwargs):
        """
        Kontext um die Top-5-Songs und Suchergebnisse erweitern.
        fan_count wird per annotate in einer einzigen SQL-Abfrage berechnet,
        um N+1 Datenbankabfragen zu vermeiden.
        """

        ctx = super().get_context_data(**kwargs)
        ctx["top_songs"] = (
            Song.objects.annotate(fan_count=Count("fans"))
            .select_related("album", "album__artist")
            .order_by("-fan_count")[:5]
        )
        query = self.request.GET.get("q", "").strip()
        ctx["query"] = query
        if query:
            ctx["search_results"] = (
                User.objects.filter(display_name__icontains=query)
                .exclude(is_superuser=True)
                .select_related("favorite_song", "favorite_song__album__artist")
            )
        else:
            ctx["search_results"] = None
        return ctx
    


class PublicProfileView(TemplateView):
    """
    Öffentliche Profilseite eines Nutzers.

    Erreichbar unter /u/<slug>/
    Zeigt den Lieblingssong des Nutzers mit Künstler- und Albumangaben.
    Bei unbekanntem Slug wird automatisch eine 404-Seite angezeigt.
    select_related lädt alle verknüpften Objekte in einer einzigen Datenbankabfrage.
    """

    template_name = "public_profile.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        profile_user = get_object_or_404(
            User.objects.select_related(
                "favorite_song",
                "favorite_song__album",
                "favorite_song__album__artist",
            ),
            slug=kwargs["slug"],
        )
        ctx["profile_user"] = profile_user
        return ctx
    

class ProfileView(LoginRequiredMixin, UpdateView):
    """
    Eingeloggter Bereich zum Bearbeiten des eigenen Profils.

    Erreichbar unter /profile/ — nur für angemeldete Nutzer.
    Nicht angemeldete Nutzer werden zur Startseite weitergeleitet (login_url).
    get_object gibt immer den aktuell eingeloggten Nutzer zurück,
    anstatt eine ID aus der URL zu erwarten.
    """

    model = User
    form_class = ProfileForm
    template_name = "profile.html"
    success_url = reverse_lazy("profile")
    login_url = "/"

    def get_object(self, queryset=None):
        """Immer den aktuell eingeloggten Nutzer zurückgeben."""
        return self.request.user

    def form_valid(self, form):
        """
        Profil speichern und favorite_song_since aktualisieren.
        commit=False speichert das Objekt im Speicher ohne Datenbankschreibung,
        damit wir favorite_song_since vor dem endgültigen Speichern setzen können.
        """

        user = form.save(commit=False)

        # Prüfen ob der Lieblingssong geändert wurde
        old_song_id = User.objects.filter(pk=user.pk).values_list(
            "favorite_song_id", flat=True
        ).first()
        
        if user.favorite_song_id != old_song_id:
            # Zeitstempel nur aktualisieren wenn sich der Song geändert hat
            user.favorite_song_since = timezone.now() if user.favorite_song else None
        
        user.save()
        messages.success(self.request, "Your profile has been updated.")
        return redirect("profile")
    

class RegistrationView(FormView):
    template_name = "registration.html"
    form_class = RegistrationForm

    def dispatch(self, request, *args, **kwargs):
        """Bereits angemeldete Nutzer zur Profilseite weiterleiten."""
        if request.user.is_authenticated:
            return redirect("profile")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Neuen Nutzer erstellen, automatisch einloggen und weiterleiten.
        form.save() erstellt den Nutzer mit gehashtem Passwort.
        """
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Willkommen bei Django Music! Dein Konto wurde erfolgreich erstellt.")
        return redirect("profile")
    
    

def logout_view(request):
    """Nutzer abmelden und zur Startseite weiterleiten."""
    logout(request)
    return redirect("home")