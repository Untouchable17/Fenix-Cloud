from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from mutagen.mp3 import MP3

from services import validators


class Artist(models.Model):

	name = models.CharField(max_length=255, verbose_name="Артист")
	slug = models.SlugField(unique=True, verbose_name="Ссылка")
	bio = models.TextField(blank=True, verbose_name="Биография")
	image = ProcessedImageField(
        upload_to=validators.get_path_upload_artist_image,
        processors=[ResizeToFit(800)], format='JPEG', options={'quality': 90},
        validators=[FileExtensionValidator(
            allowed_extensions=["jpg", "png", "jpeg", "webp"]
        ), validators.check_size_image],
        verbose_name="Изображение"
	)
	created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

	def __str__(self):
		return f"{self.name}"

	class Meta:
		verbose_name = "Артист"
		verbose_name_plural = "Артисты"

class Audio(models.Model):

	title = models.CharField(max_length=255, verbose_name="Название")
	artist = models.ForeignKey(
		Artist, 
		on_delete=models.SET_NULL, 
		related_name="audios", 
		blank=True, 
		null=True,
		verbose_name="Артист"
	)
	duration = models.PositiveIntegerField(verbose_name="Длительность", blank=True)
	file = models.FileField(
		upload_to=validators.get_path_upload_audio_file, 
		validators=[
			FileExtensionValidator(allowed_extensions=["mp3", "ogg", "wav"]), 
			validators.validate_audio_file_size
		]
	)
	date = models.DateField(blank=True, verbose_name="Дата выпуска")

	def __str__(self):
		return f"{self.title}"

	def format_duration(self):
		minutes, seconds = divmod(self.duration, 60)
		return f"{minutes:02d}:{seconds:02d}"

	def save(self, *args, **kwargs):
		audio_file = MP3(self.file)
		self.duration = audio_file.info.length
		super(Audio, self).save(*args, **kwargs)

	class Meta:
		verbose_name = "Аудио"
		verbose_name_plural = "Аудио"


class Album(models.Model):
	""" Модель альбома """

	title = models.CharField(max_length=255, verbose_name="Название")
	artist = models.ForeignKey(
		Artist, 
		on_delete=models.SET_NULL, 
		related_name="albums", 
		blank=True, 
		null=True,
		verbose_name="Группа/Музыкант"
	)
	cover = ProcessedImageField(
        upload_to=validators.get_path_upload_album_cover,
        processors=[ResizeToFit(800)], format='JPEG', options={'quality': 90},
        validators=[FileExtensionValidator(
            allowed_extensions=["jpg", "png", "jpeg", "webp"]
        ), validators.check_size_image],
        verbose_name="Обложка"
    )
	description = models.TextField(blank=True, verbose_name="Описание")
	release_date = models.DateField(verbose_name="Дата релиза")
	audios = models.ManyToManyField(
		Audio,
		related_name="album_audios",
		verbose_name="Треки"
	)

	def __str__(self):
		return f"{self.title}"


	class Meta:
		verbose_name = "Альбом"
		verbose_name_plural = "Альбомы"

class Playlist(models.Model):

	user = models.ForeignKey(
    	settings.AUTH_USER_MODEL, 
    	on_delete=models.CASCADE, 
    	related_name='playlists', 
    	verbose_name="Владелец"
	)
	title = models.CharField(max_length=255, verbose_name="Название")
	audios = models.ManyToManyField(
		Audio,
		related_name="playlist_audios",
		verbose_name="Треки"
	)
	created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

	def __str__(self):
		return f"{self.user} - {self.title}"

	class Meta:
		verbose_name = "Плейлист"
		verbose_name_plural = "Плейлисты"


class Favorite(models.Model):

	audio = models.ManyToManyField(Audio, verbose_name="Трек")
	user = models.OneToOneField(
		settings.AUTH_USER_MODEL, 
		on_delete=models.CASCADE, 
		related_name='favorite',
		verbose_name="Пользователь"
	)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Избранное {self.user}"

	class Meta:
		verbose_name = "Избранное"
		verbose_name_plural = "Избранные"



class License(models.Model):

	title = models.CharField(max_length=255, verbose_name="Лицензия")

	class Meta:
		verbose_name = "Лицензия"
		verbose_name_plural = "Лицензии"





