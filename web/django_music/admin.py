from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django_music.models import Album, Artist, Song, User

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ["title", "artist"]
    list_select_related = ["artist"]
    search_fields = ["title", "artist__name"]


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ["title", "get_artist", "album"]
    list_select_related = ["album", "album__artist"]
    search_fields = ["title", "album__title", "album__artist__name"]

    @admin.display(description="Artist", ordering="album__artist__name")
    def get_artist(self, obj):
        return obj.album.artist
    

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["username", "display_name", "slug", "favorite_song", "is_staff"]
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Profile", {"fields": ("slug", "display_name", "favorite_song", "favorite_song_since")}),
    )
    readonly_fields = ["favorite_song_since"]