from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from django_music.models import Artist
from django_music.serializers import ArtistSerializer


class ArtistListView(generics.ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [IsAuthenticated]