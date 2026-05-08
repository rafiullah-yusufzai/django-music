from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

class Artist(models.Model):
    """Repräsentiert einen Musikkünstler oder eine Band."""

    name = models.CharField(max_length = 255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    

class Album(models.Model):

    """
    Repräsentiert ein Musikalbum eines Künstlers.
    Das Coverbild ist optional — Alben ohne Cover
    verwenden in den Templates einen Platzhalter.
    """

    title = models.CharField(max_length = 255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="albums")
    cover = models.ImageField(upload_to="covers/", blank=True, null=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} – {self.artist}"
    

class Song(models.Model):

    """
    Repräsentiert einen einzelnen Song auf einem Album.
    Die artist-Property bietet eine Abkürzung, um
    song.album.artist im gesamten Code zu vermeiden.
    """

    title = models.CharField(max_length=255)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="songs")

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} ({self.album.artist})"

    @property
    def artist(self):
        """Abkürzung für den direkten Zugriff auf den Künstler eines Songs."""
        return self.album.artist
    


class User(AbstractUser):
    
    """
    Benutzerdefiniertes User-Model, das Djangos AbstractUser erweitert.

    Zusätzliche Felder:
    - slug: automatisch aus dem Benutzernamen generiert, für öffentliche Profil-URLs (/u/<slug>/)
    - display_name: optionaler Anzeigename auf dem Profil
    - favorite_song: der aktuell gewählte Lieblingssong des Nutzers
    - favorite_song_since: Zeitstempel der letzten Änderung des Lieblingssongs
    """

    slug = models.SlugField(unique=True, blank=True)
    display_name = models.CharField(max_length=150, blank=True)
    favorite_song = models.ForeignKey(
        Song,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="fans",
    )
    favorite_song_since = models.DateTimeField(null=True, blank=True)


    # save() function auto-generates a unique slug from the username when the user is first created.
    def save(self, *args, **kwargs):
        """
        Generiert beim ersten Speichern automatisch einen eindeutigen Slug aus dem Benutzernamen.
        Falls der Slug bereits vergeben ist, wird ein Zähler angehängt (z.B. john-2).
        """
        if not self.slug:
            base_slug = slugify(self.username)
            slug = base_slug
            counter = 1
            while User.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_display_name(self):
        """
        Gibt den bestmöglichen Anzeigenamen zurück.
        Priorität: display_name → vollständiger Name → Benutzername.
        """
        return self.display_name or self.get_full_name() or self.username

    def __str__(self):
        return self.get_display_name()
    
    