from django.http import FileResponse
from django.views.decorators.cache import cache_page
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions

from src.tracks.permissions import IsOwner
from src.tracks import serializers
from src.tracks import models
from services.validators import delete_old_file


@cache_page(60 * 15)
class AlbumViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Album.objects.all()
    serializer_class = serializers.AlbumSerializer
    permission_classes = (permissions.AllowAny, )


class ArtistViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Artist.objects.all()
    serializer_class = serializers.ArtistSerializer
    permission_classes = (permissions.AllowAny, )


class AudioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Audio.objects.all()
    serializer_class = serializers.AudioSerializer
    permission_classes = (permissions.AllowAny, )

    def get_serializer_class(self):
        if self.action == "favorite" and self.request.method == "POST":
            return serializers.FavoriteSerializer
        return self.serializer_class
    
    @action(methods=["POST"], detail=True, permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk=None):
        audio = self.get_object()
        favorite, created = models.Favorite.objects.get_or_create(user=request.user)
        favorite.audio.add(audio)
        serializer = serializers.FavoriteSerializer(favorite)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    def download(self, request, pk=None):
        audio = self.get_object()
        file = audio.file
        response = FileResponse(file, as_attachment=True, filename=f"{audio.title}.mp3")
        return response


class FavoriteViewSet(viewsets.ReadOnlyModelViewSet):
    
    queryset = models.Favorite.objects.all()
    serializer_class = serializers.FavoriteSerializer
    permission_classes = (IsOwner, )

    def list(self, request):
        queryset = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=False)
    def add_audio(self, request):
        audio_ids = request.data.get("audio")
        if not audio_ids:
            return Response({'audio_id': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        audio = models.Audio.objects.filter(id__in=audio_ids)
        if audio.count() != len(audio_ids):
            return Response({'audio_id': 'One or more audio ids do not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        favorite, _ = models.Favorite.objects.get_or_create(user=request.user)
        favorite.audio.add(*audio)

        serializer = self.get_serializer(favorite)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True, url_path='remove_audio/(?P<audio_id>[^/.]+)')
    def remove_audio(self, request, pk=None, audio_id=None):
        favorite = self.get_object()
        if int(audio_id) not in favorite.audio.values_list('id', flat=True):
            return Response(
                {'audio_id': 'Audio with this id is not in favorites.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        favorite.audio.remove(int(audio_id))
        if not favorite.audio.exists():
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            favorite.save()
            serializer = self.get_serializer(favorite)
            return Response(serializer.data)

    def retrieve(self, request, pk=None):
        favorite = self.get_object()
        audio_id = request.query_params.get('audio_id', None)
        if audio_id and audio_id in favorite.audio.values_list('id', flat=True):
            audio = favorite.audio.get(id=audio_id)
            serializer = serializers.AudioSerializer(audio)
            return Response(serializer.data)
        serializer = self.get_serializer(favorite)
        return Response(serializer.data)


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = models.Playlist.objects.all()
    serializer_class = serializers.PlayListSerializer
    permission_classes = (IsOwner, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.user == self.request.user:
            instance.delete()
        else:
            raise permissions.PermissionDenied(
                "You are not allowed to delete this playlist."
            )