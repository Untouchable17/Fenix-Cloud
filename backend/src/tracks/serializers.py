from rest_framework import serializers

from src.tracks import models




class AlbumSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Album
        fields = "__all__"


class AudioSerializer(serializers.ModelSerializer):

    duration = serializers.SerializerMethodField()

    def get_duration(self, obj):
        return obj.format_duration()

    class Meta:
        model = models.Audio
        fields = ('id', 'title', 'artist', 'duration', 'file', 'date')


class ArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Artist
        fields = ("id", "name", "slug", "bio", "image")


class PlayListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Playlist
        fields = "__all__"


class RemoveAudioSerializer(serializers.Serializer):
    audio_id = serializers.IntegerField()


class FavoriteSerializer(serializers.ModelSerializer):
    audio = serializers.PrimaryKeyRelatedField(
        queryset=models.Audio.objects.all(),
        many=True
    )

    class Meta:
        model = models.Favorite
        fields = ('id', 'user', 'audio')


