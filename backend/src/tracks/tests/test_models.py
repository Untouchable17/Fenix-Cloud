from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from unittest.mock import patch, Mock
from django.core.validators import ValidationError
from django.contrib.auth import get_user_model
from datetime import date

from src.tracks.models import Audio, Artist, Favorite, Album, Playlist


class AudioModelTestCase(TestCase):
    def setUp(self):

        self.PATH = "src/tracks/tests/test_data"
        self.artist = Artist.objects.create(
            name="Test Artist",
            slug="test-artist",
            bio="Test bio",
            image=SimpleUploadedFile(
                name="Z0Y5cl1C15I.jpg",
                content=open(f"{self.PATH}/Z0Y5cl1C15I.jpg", "rb").read(),
                content_type="image/jpeg"
            )
        )
        self.audio = Audio.objects.create(
            title="Test Audio",
            artist=self.artist,
            file=SimpleUploadedFile(
                name="Под проливным дождем.mp3",
                content=open(f"{self.PATH}/Под проливным дождем.mp3", "rb").read(),
                content_type="audio/mpeg"
            ),
            date="2022-01-01"
        )

    def test_str(self):
        self.assertEqual(str(self.audio), "Test Audio")

    def test_format_duration(self):
        self.audio.duration = 90
        self.assertEqual(self.audio.format_duration(), "01:30")

    def test_save(self):
        self.assertEqual(self.audio.duration, 131.36975)
        self.audio.save()
        self.assertNotEqual(self.audio.duration, 0)

    def test_audio_file_validators(self):
        # Test valid audio file
        self.audio.file = SimpleUploadedFile(
            name="Январькая вьюга.mp3",
            content=open(f"{self.PATH}/Январькая вьюга.mp3", "rb").read(),
            content_type="audio/mpeg"
        )
        self.audio.full_clean()
        
        # Test invalid file extension
        with self.assertRaises(ValidationError):
            self.audio.file = SimpleUploadedFile(
                name="NotCurrectFile.txt",
                content=open(f"{self.PATH}/NotCurrectFile.txt", "rb").read(),
                content_type="text/plain"
            )
            self.audio.full_clean()
        
        # тест на большой размер файла
        # with self.assertRaises(ValidationError):
        #     self.audio.file = SimpleUploadedFile(
        #         name="Январькая вьюга.mp3",
        #         content=open(f"{self.PATH}/Январькая вьюга.mp3", "rb").read(),
        #         content_type="audio/mpeg"
        #     )
        #     self.audio.full_clean()





class FavoriteModelTest(TestCase):

    def setUp(self):
        
        self.PATH = "src/tracks/tests/test_data"
        
        self.user = get_user_model().objects.create_user(
            first_name="SecDet", 
            last_name="Samurai", 
            email='testuser@test.com',
            password='secret'
        )
        self.artist = Artist.objects.create(
            name="Test Artist",
            slug="test-artist",
            bio="Test bio",
            image=SimpleUploadedFile(
                name="Z0Y5cl1C15I.jpg",
                content=open(f"{self.PATH}/Z0Y5cl1C15I.jpg", "rb").read(),
                content_type="image/jpeg"
            )
        )
        self.audio = Audio.objects.create(
            title="Test Audio",
            artist=self.artist,
            file=SimpleUploadedFile(
                name="Под проливным дождем.mp3",
                content=open(f"{self.PATH}/Под проливным дождем.mp3", "rb").read(),
                content_type="audio/mpeg"
            ),
            date="2022-01-01"
        )
    def test_favorite_creation(self):
        favorite = Favorite.objects.create(user=self.user)
        self.assertEqual(favorite.audio.count(), 0)
        self.assertEqual(str(favorite), f'Избранное {self.user}')

    def test_add_audio_to_favorite(self):
        favorite = Favorite.objects.create(user=self.user)
        favorite.audio.add(self.audio)
        self.assertEqual(favorite.audio.count(), 1)

    def test_remove_audio_from_favorite(self):
        favorite = Favorite.objects.create(user=self.user)
        favorite.audio.add(self.audio)
        self.assertEqual(favorite.audio.count(), 1)
        favorite.audio.remove(self.audio)
        self.assertEqual(favorite.audio.count(), 0)

    def test_favorite_related_name(self):
        Favorite.objects.create(user=self.user)
        self.assertEqual(self.user.favorite.user, self.user)

    

class AlbumModelTest(TestCase):

    def setUp(self):
        self.PATH = "src/tracks/tests/test_data"
        
        self.user = get_user_model().objects.create_user(
            first_name="SecDet", 
            last_name="Samurai", 
            email='testuser@test.com',
            password='secret'
        )
        self.artist = Artist.objects.create(
            name="Test Artist",
            slug="test-artist",
            bio="Test bio",
            image=SimpleUploadedFile(
                name="Z0Y5cl1C15I.jpg",
                content=open(f"{self.PATH}/Z0Y5cl1C15I.jpg", "rb").read(),
                content_type="image/jpeg"
            )
        )
        self.audio = Audio.objects.create(
            title="Test Audio",
            artist=self.artist,
            file=SimpleUploadedFile(
                name="Под проливным дождем.mp3",
                content=open(f"{self.PATH}/Под проливным дождем.mp3", "rb").read(),
                content_type="audio/mpeg"
            ),
            date="2022-01-01"
        )
        self.album = Album.objects.create(
            title="test_album",
            artist=self.artist,
            cover=SimpleUploadedFile(
                name="AlbumCover.jpeg",
                content=open(f"{self.PATH}/AlbumCover.jpeg", "rb").read(),
                content_type="image/jpeg"
            ),
            description="test_description",
            release_date=date(2022, 3, 8),
        )

        self.album.audios.add(self.audio)
        self.album.save()
        

    def test_album_fields(self):
        # проверяем, что поля альбома заполнены верно
        album = self.album
        self.assertEqual(album.title, "test_album")
        self.assertEqual(album.artist, self.artist)
        self.assertEqual(album.description, "test_description")
        self.assertEqual(album.release_date, date(2022, 3, 8))
        
    def test_album_str(self):
        # проверяем, что метод __str__ возвращает верную строку
        album = self.album
        self.assertEqual(str(album), "test_album")
        
    def test_album_audios(self):
        # проверяем, что трек добавлен в альбом
        album = self.album
        self.assertEqual(album.audios.count(), 1)
        self.assertEqual(album.audios.first(), self.audio)
        
    def test_album_cover_upload(self):
        # проверяем, что обложка успешно загружена
        album = self.album
        self.assertTrue(album.cover)



class PlaylistModelTest(TestCase):

    def setUp(self):
        self.PATH = "src/tracks/tests/test_data"
        
        self.user = get_user_model().objects.create_user(
            first_name="SecDet", 
            last_name="Samurai", 
            email='testuser@test.com',
            password='secret'
        )
        self.artist = Artist.objects.create(
            name="Test Artist",
            slug="test-artist",
            bio="Test bio",
            image=SimpleUploadedFile(
                name="Z0Y5cl1C15I.jpg",
                content=open(f"{self.PATH}/Z0Y5cl1C15I.jpg", "rb").read(),
                content_type="image/jpeg"
            )
        )
        self.audio1 = Audio.objects.create(
            title="Test Audio",
            artist=self.artist,
            file=SimpleUploadedFile(
                name="Под проливным дождем.mp3",
                content=open(f"{self.PATH}/Под проливным дождем.mp3", "rb").read(),
                content_type="audio/mpeg"
            ),
            date="2022-01-01"
        )
        self.audio2 = Audio.objects.create(
            title="Test Audio",
            artist=self.artist,
            file=SimpleUploadedFile(
                name="Январькая вьюга.mp3",
                content=open(f"{self.PATH}/Январькая вьюга.mp3", "rb").read(),
                content_type="audio/mpeg"
            ),
            date="2022-01-01"
        )

    def test_playlist_creation(self):
        # Создаем плейлист и проверяем, что он создался
        playlist = Playlist.objects.create(
            user=self.user,
            title='Test Playlist'
        )
        self.assertEqual(str(playlist), f"{self.user} - Test Playlist")

    def test_playlist_audios(self):
        # Создаем плейлист и добавляем к нему несколько аудиофайлов
        playlist = Playlist.objects.create(
            user=self.user,
            title='Test Playlist'
        )
        playlist.audios.add(self.audio1, self.audio2)
        
        """
            Проверяем, что аудиофайлы добавились
            Параметр transform указывает функцию для преобразования каждого объекта в наборе запросов 
            в строковое представление, которое можно сравнить с ожидаемыми результатами. 
            В этом случае мы используем атрибут pk.
        """
        self.assertQuerysetEqual(
            playlist.audios.all().order_by('id'), 
            [str(self.audio1.pk), str(self.audio2.pk)],
            transform=lambda x: str(x.pk)
        )