from rest_framework import serializers
from django_music.models import Artist


class ArtistSerializer(serializers.ModelSerializer):
    """
    Serializer für das Artist-Model.
    Konvertiert Artist-Objekte in JSON und umgekehrt.
    Gibt nur id und name zurück — keine sensiblen Daten.
    """
    
    class Meta:
        model = Artist
        fields = ["id", "name"]