from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from django_music.models import Artist
from django_music.serializers import ArtistSerializer


class ArtistListView(generics.ListAPIView):
    """
    REST API Endpunkt — Gibt eine Liste aller Künstler zurück.

    Erreichbar unter: /api/artists/
    Methode: GET
    Authentifizierung: erforderlich (nur für angemeldete Nutzer)

    Beispielantwort:
    [
        {"id": 1, "name": "The Beatles"},
        {"id": 2, "name": "Pink Floyd"}
    ]
    """

    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    # Nur angemeldete Nutzer dürfen die API verwenden
    permission_classes = [IsAuthenticated]