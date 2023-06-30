import uuid

from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

from services import validators


class Category(models.Model):

    name = models.CharField(max_length=50, verbose_name=_("Название"))
    slug = models.SlugField(unique=True, verbose_name=_("Ссылка"))

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.name}"


class Tag(models.Model):

    name = models.CharField(max_length=30, verbose_name=_("Название"))
    slug = models.SlugField(unique=True, verbose_name=_("Ссылка"))

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    """ Модель продукта """

    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="products_category",
        verbose_name="Категория"
    )
    title = models.CharField(max_length=255, verbose_name=_("Название"))
    slug = models.SlugField(unique=True, verbose_name=_("Ссылка"))
    image = ProcessedImageField(
        upload_to=validators.get_path_upload_product_image,
        processors=[ResizeToFit(800)], format='JPEG', options={'quality': 90},
        validators=[FileExtensionValidator(
            allowed_extensions=["jpg", "png", "jpeg", "webp", "gif"]
        ), validators.check_size_image],
        verbose_name=_("Изображение")
    )
    description = models.TextField(verbose_name=_("Описание"))
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=_("Цена"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    tags = models.ManyToManyField(
        Tag,
        related_name="product_tags",
        blank=True,
        verbose_name=_("Тэги")
    )
    available = models.BooleanField(default=True, verbose_name=_("Доступность"))

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_("Товар")
    )
    image = ProcessedImageField(
        upload_to=validators.get_path_upload_product_sub_image,
        processors=[ResizeToFit(800)], format='JPEG', options={'quality': 90},
        validators=[FileExtensionValidator(
            allowed_extensions=["jpg", "png", "jpeg", "webp", ]
        ), validators.check_size_image],
        blank=True,
        verbose_name=_("Изображение")
    )

    def __str__(self):
        return f"{self.product.title} Image"
