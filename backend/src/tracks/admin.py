from django.contrib import admin

from src.tracks import models


@admin.register(models.Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'duration', 'date')
    list_filter = ('artist',)
    search_fields = ('title', 'artist')


@admin.register(models.Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(models.Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist')
    list_filter = ('artist',)
    search_fields = ('title', 'artist')


@admin.register(models.Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    list_filter = ('user',)


@admin.register(models.License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(models.Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    list_filter = ('user',)
    search_fields = ('title',)