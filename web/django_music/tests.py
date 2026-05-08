from django.test import TestCase, Client
from django.urls import reverse

from django_music.models import Artist, Album, Song, User
from django_music.forms import LoginForm, ProfileForm, RegistrationForm

class BaseTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.artist = Artist.objects.create(name="The Beatles")
        self.album = Album.objects.create(title="Abbey Road", artist=self.artist)
        self.song = Song.objects.create(title="Come Together", album=self.album)

        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            display_name="Test User",
        )
        self.user.favorite_song = self.song
        self.user.save()


class UserModelTest(BaseTestCase):

    def test_slug_auto_generated(self):
        """Slug wird automatisch aus dem Benutzernamen generiert."""
        self.assertEqual(self.user.slug, "testuser")

    def test_slug_is_unique(self):
        """Zwei Nutzer mit gleichem Benutzernamen bekommen unterschiedliche Slugs."""
        user2 = User.objects.create_user(username="testuser2", password="testpass123")
        self.assertNotEqual(self.user.slug, user2.slug)

    def test_get_display_name_returns_display_name(self):
        """get_display_name gibt den Anzeigenamen zurück wenn gesetzt."""
        self.assertEqual(self.user.get_display_name(), "Test User")

    def test_get_display_name_falls_back_to_username(self):
        """get_display_name gibt den Benutzernamen zurück wenn kein Anzeigename gesetzt."""
        user2 = User.objects.create_user(username="noname", password="testpass123")
        self.assertEqual(user2.get_display_name(), "noname")


class SongModelTest(BaseTestCase):

    def test_artist_property(self):
        """Song.artist gibt den Künstler über das Album zurück."""
        self.assertEqual(self.song.artist, self.artist)

    def test_song_str(self):
        """Song __str__ enthält Titel und Künstler."""
        self.assertIn("Come Together", str(self.song))
        self.assertIn("The Beatles", str(self.song))


class HomeViewTest(BaseTestCase):

    def test_home_page_loads(self):
        """Startseite lädt korrekt."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_home_page_contains_top_songs(self):
        """Startseite zeigt die beliebtesten Songs."""
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Come Together")

    def test_login_success(self):
        """Erfolgreiche Anmeldung leitet zur Profilseite weiter."""
        response = self.client.post(reverse("home"), {
            "username": "testuser",
            "password": "testpass123",
        })
        self.assertRedirects(response, reverse("profile"))

    def test_login_wrong_password(self):
        """Falsche Anmeldedaten zeigen Fehler."""
        response = self.client.post(reverse("home"), {
            "username": "testuser",
            "password": "wrongpassword",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], None, "Bitte Benutzername und Passwort eingeben. Beide Felder berücksichtigen die Groß-/Kleinschreibung.")
        
    def test_authenticated_user_redirected_from_home(self):
        """Bereits angemeldete Nutzer werden von der Startseite weitergeleitet."""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("home"))
        self.assertRedirects(response, reverse("profile"))

    def test_search_returns_results(self):
        """Suche findet Nutzer nach Anzeigenamen."""
        response = self.client.get(reverse("home"), {"q": "Test"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test User")

    def test_search_no_results(self):
        """Suche gibt keine Ergebnisse für unbekannte Namen zurück."""
        response = self.client.get(reverse("home"), {"q": "niemand"})
        self.assertNotContains(response, "Test User")


class PublicProfileViewTest(BaseTestCase):

    def test_public_profile_loads(self):
        """Öffentliches Profil lädt korrekt."""
        response = self.client.get(reverse("public_profile", kwargs={"slug": self.user.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "public_profile.html")

    def test_public_profile_shows_song(self):
        """Öffentliches Profil zeigt den Lieblingssong."""
        response = self.client.get(reverse("public_profile", kwargs={"slug": self.user.slug}))
        self.assertContains(response, "Come Together")

    def test_public_profile_404_for_unknown_slug(self):
        """Unbekannter Slug gibt 404 zurück."""
        response = self.client.get(reverse("public_profile", kwargs={"slug": "gibts-nicht"}))
        self.assertEqual(response.status_code, 404)


class ProfileViewTest(BaseTestCase):

    def test_profile_requires_login(self):
        """Profilseite leitet nicht angemeldete Nutzer weiter."""
        response = self.client.get(reverse("profile"))
        self.assertRedirects(response, "/?next=/profile/")

    def test_profile_loads_for_logged_in_user(self):
        """Profilseite lädt korrekt für angemeldete Nutzer."""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")

    def test_profile_update_display_name(self):
        """Anzeigename kann erfolgreich geändert werden."""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(reverse("profile"), {
            "display_name": "Neuer Name",
            "favorite_song": self.song.pk,
        })
        self.assertRedirects(response, reverse("profile"))
        self.user.refresh_from_db()
        self.assertEqual(self.user.display_name, "Neuer Name")


class RegistrationViewTest(BaseTestCase):

    def test_registration_page_loads(self):
        """Registrierungsseite lädt korrekt."""
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration.html")

    def test_registration_creates_user(self):
        """Registrierung erstellt einen neuen Nutzer."""
        response = self.client.post(reverse("register"), {
            "username": "neuernutzer",
            "display_name": "Neuer Nutzer",
            "password1": "sicheres_passwort_123",
            "password2": "sicheres_passwort_123",
        })
        self.assertRedirects(response, reverse("profile"))
        self.assertTrue(User.objects.filter(username="neuernutzer").exists())

    def test_registration_mismatched_passwords(self):
        """Registrierung schlägt fehl bei unterschiedlichen Passwörtern."""
        response = self.client.post(reverse("register"), {
            "username": "neuernutzer",
            "password1": "sicheres_passwort_123",
            "password2": "anderes_passwort_123",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="neuernutzer").exists())

    def test_authenticated_user_redirected_from_register(self):
        """Bereits angemeldete Nutzer werden von der Registrierungsseite weitergeleitet."""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("register"))
        self.assertRedirects(response, reverse("profile"))



class LoginFormTest(BaseTestCase):

    def test_valid_login_form(self):
        """LoginForm ist gültig mit korrekten Daten."""
        form = LoginForm(data={
            "username": "testuser",
            "password": "testpass123",
        }, request=self.client.request())
        self.assertTrue(form.is_valid())

    def test_invalid_login_form_empty(self):
        """LoginForm ist ungültig wenn Felder leer sind."""
        form = LoginForm(data={}, request=self.client.request())
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertIn("password", form.errors)


class RegistrationFormTest(BaseTestCase):

    def test_valid_registration_form(self):
        """RegistrationForm ist gültig mit korrekten Daten."""
        form = RegistrationForm(data={
            "username": "neuernutzer",
            "display_name": "Neuer Nutzer",
            "password1": "sicheres_passwort_123",
            "password2": "sicheres_passwort_123",
        })
        self.assertTrue(form.is_valid())

    def test_registration_form_mismatched_passwords(self):
        """RegistrationForm ist ungültig bei unterschiedlichen Passwörtern."""
        form = RegistrationForm(data={
            "username": "neuernutzer",
            "password1": "sicheres_passwort_123",
            "password2": "anderes_passwort_123",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_registration_form_duplicate_username(self):
        """RegistrationForm ist ungültig bei bereits vergebenem Benutzernamen."""
        form = RegistrationForm(data={
            "username": "testuser",
            "password1": "sicheres_passwort_123",
            "password2": "sicheres_passwort_123",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)


class ProfileFormTest(BaseTestCase):

    def test_valid_profile_form(self):
        """ProfileForm ist gültig mit korrekten Daten."""
        form = ProfileForm(data={
            "display_name": "Neuer Name",
            "favorite_song": self.song.pk,
        })
        self.assertTrue(form.is_valid())

    def test_profile_form_without_song(self):
        """ProfileForm ist gültig ohne Lieblingssong."""
        form = ProfileForm(data={
            "display_name": "Neuer Name",
            "favorite_song": "",
        })
        self.assertTrue(form.is_valid())

    def test_profile_form_without_display_name(self):
        """ProfileForm ist gültig ohne Anzeigenamen."""
        form = ProfileForm(data={
            "display_name": "",
            "favorite_song": self.song.pk,
        })
        self.assertTrue(form.is_valid())