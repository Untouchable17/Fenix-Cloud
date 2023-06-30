import uuid

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

from services import validators
from src.customer.managers import CustomUserManager


User = settings.AUTH_USER_MODEL



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("Пользователь"))
    bio = models.TextField(max_length=500, blank=True, verbose_name=_("О себе"))
    image = ProcessedImageField(
        upload_to=validators.get_path_upload_profile_image,
        processors=[ResizeToFit(500)], format='JPEG', options={'quality': 90},
        validators=[FileExtensionValidator(
            allowed_extensions=["jpg", "png", "jpeg", "webp"]
        ), validators.check_size_image],
        blank=True,
        verbose_name=_("Изображение")
    )
    location = models.CharField(max_length=30, blank=True, verbose_name=_("Локация"))

    def __str__(self):
        return f"{self.user} Profile"

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


class CustomUser(AbstractBaseUser, PermissionsMixin):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True, verbose_name=_("Почта"))
    first_name = models.CharField(max_length=30, verbose_name=_("Имя"))
    last_name = models.CharField(max_length=30, verbose_name=_("Фамилия"))
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("first_name", "last_name")
    EMAIL_FIELD = "email"

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
