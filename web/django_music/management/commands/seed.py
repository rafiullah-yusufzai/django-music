"""
Management Command: seed

Befüllt die Datenbank mit Beispieldaten für Entwicklung und Tests.
Erstellt Künstler, Alben, Songs und Demo-Nutzer.

Verwendung:
    python manage.py seed
"""

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from django_music.models import Album, Artist, Song, User


# Beispieldaten für Künstler, Alben und Songs
SAMPLE_DATA = [
    {
        "artist": "The Beatles",
        "albums": [
            {
                "title": "Abbey Road",
                "songs": ["Come Together", "Something", "Here Comes the Sun"],
            },
            {
                "title": "Sgt. Pepper's Lonely Hearts Club Band",
                "songs": ["Lucy in the Sky with Diamonds", "With a Little Help from My Friends"],
            },
        ],
    },
    {
        "artist": "Pink Floyd",
        "albums": [
            {
                "title": "The Dark Side of the Moon",
                "songs": ["Money", "Time", "Breathe"],
            },
        ],
    },
    {
        "artist": "David Bowie",
        "albums": [
            {
                "title": "Heroes",
                "songs": ["Heroes", "Beauty and the Beast"],
            },
            {
                "title": "Ziggy Stardust",
                "songs": ["Starman", "Suffragette City"],
            },
        ],
    },
    {
        "artist": "Radiohead",
        "albums": [
            {
                "title": "OK Computer",
                "songs": ["Paranoid Android", "Karma Police", "No Surprises"],
            },
        ],
    },
]

# Demo-Nutzer mit Passwort demo1234
DEMO_USERS = [
    {"username": "alice", "display_name": "Alice Müller"},
    {"username": "bob", "display_name": "Bob Schmidt"},
    {"username": "carol", "display_name": "Carol Weber"},
]


class Command(BaseCommand):
    """
    Befüllt die Datenbank mit Beispieldaten.
    Bereits vorhandene Einträge werden übersprungen (get_or_create).
    """

    help = "Datenbank mit Beispieldaten befüllen"

    def handle(self, *args, **options):
        self.stdout.write("Befülle Datenbank mit Beispieldaten...")

        all_songs = []

        # Künstler, Alben und Songs erstellen
        for entry in SAMPLE_DATA:
            artist, _ = Artist.objects.get_or_create(name=entry["artist"])

            for album_data in entry["albums"]:
                album, _ = Album.objects.get_or_create(
                    title=album_data["title"],
                    artist=artist,
                )

                for song_title in album_data["songs"]:
                    song, _ = Song.objects.get_or_create(
                        title=song_title,
                        album=album,
                    )
                    all_songs.append(song)

        self.stdout.write(f"  ✓ {len(all_songs)} Songs erstellt.")

        # Demo-Nutzer erstellen
        self.stdout.write("Erstelle Demo-Nutzer...")

        for i, user_data in enumerate(DEMO_USERS):
            user, created = User.objects.get_or_create(
                username=user_data["username"],
                defaults={
                    "display_name": user_data["display_name"],
                    "password": make_password("demo1234"),
                },
            )

            if created:
                # Jedem Nutzer einen anderen Lieblingssong zuweisen
                user.favorite_song = all_songs[i % len(all_songs)]
                user.save()
                self.stdout.write(
                    f"  ✓ Nutzer '{user.username}' erstellt (Passwort: demo1234)"
                )
            else:
                self.stdout.write(
                    f"  – Nutzer '{user.username}' existiert bereits, wird übersprungen."
                )

        self.stdout.write(
            self.style.SUCCESS("\nDatenbank erfolgreich befüllt! ✓")
        )