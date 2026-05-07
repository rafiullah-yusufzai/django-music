from django import forms
from django.contrib.auth.forms import AuthenticationForm

from django_music.models import Song, User

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
    )


class ProfileForm(forms.ModelForm):
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