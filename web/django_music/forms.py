from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django_music.models import Song, User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginForm(AuthenticationForm):
    """
    Anmeldeformular, das Djangos eingebautes AuthenticationForm erweitert.
    Die gesamte Authentifizierungslogik (Passwortprüfung, inaktive Konten usw.)
    wird von Django übernommen — wir fügen nur Bootstrap-CSS-Klassen hinzu.
    """

    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
    )


class ProfileForm(forms.ModelForm):
    """
    Formular zum Bearbeiten des Nutzerprofils.
    Ermöglicht das Ändern des Anzeigenamens und des Lieblingssongs.
    favorite_song wird manuell definiert, um select_related für
    effiziente Datenbankabfragen zu nutzen und Bootstrap-Styling hinzuzufügen.
    """

    favorite_song = forms.ModelChoiceField(
        queryset=Song.objects.select_related("album", "album__artist").all(),
        required=False,
        label="Favorite song",
        widget=forms.Select(attrs={"class": "form-select"}),
        empty_label="— No favorite song —",
    )

    class Meta:
        model = User
        fields = ["display_name", "favorite_song"]
        widgets = {
            "display_name": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "display_name": "Display name",
        }



class RegistrationForm(UserCreationForm):
    """
    Registrierungsformular, das Djangos UserCreationForm erweitert.
    Übernimmt automatisch: Passwort-Hashing, Passwortbestätigung,
    Passwortstärke-Validierung und Prüfung auf doppelte Benutzernamen.
    Zusätzlich wird ein optionaler Anzeigename abgefragt.
    """

    display_name = forms.CharField(
        label="Anzeigename",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Anzeigename"}),
    )

    class Meta:
        model = User
        fields = ["username", "display_name", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Benutzername",
        })
        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Passwort",
        })
        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Passwort bestätigen",
        })