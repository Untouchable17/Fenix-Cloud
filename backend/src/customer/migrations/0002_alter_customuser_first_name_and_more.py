# Generated by Django 4.1.7 on 2023-03-03 21:36

import django.core.validators
from django.db import migrations, models
import imagekit.models.fields
import services.validators


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(max_length=30, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, upload_to=services.validators.get_path_upload_profile_image, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg', 'webp']), services.validators.check_size_image], verbose_name='Изображение'),
        ),
    ]
