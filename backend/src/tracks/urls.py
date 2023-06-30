from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import path, include

from src.tracks import views


router = DefaultRouter()
router.register(r'artists', views.ArtistViewSet, basename='artist')
router.register(r'audios', views.AudioViewSet, basename='audio')
router.register(r'albums', views.AlbumViewSet, basename='album')
router.register(r'playlists', views.PlaylistViewSet, basename='playlist')
router.register(r'favorites', views.FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('', include(router.urls)),
]