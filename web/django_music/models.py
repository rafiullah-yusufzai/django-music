from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

class Artist(models.Model):
    name = models.CharField(max_length = 255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    

class Album(models.Model):
    title = models.CharField(max_length = 255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="albums")
    cover = models.ImageField(upload_to="covers/", blank=True, null=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} – {self.artist}"
    

class Song(models.Model):
    title = models.CharField(max_length=255)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="songs")

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} ({self.album.artist})"

    @property
    def artist(self):
        return self.album.artist
    


class User(AbstractUser):
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
        return self.display_name or self.get_full_name() or self.username

    def __str__(self):
        return self.get_display_name()
    
    