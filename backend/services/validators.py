import os
import uuid

from django.core.validators import ValidationError


def get_path_upload_artist_image(instance, file):
    return f"artists/artist_{instance.name}/{file}"

def get_path_upload_album_cover(instance, file):
    return f"albums/{instance}/{file}"

def get_path_upload_audio_file(instance, filename):

    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"audios/{instance}/{filename}"

def validate_audio_file_size(file_object):

    megabyte_limit = 100 * 1024 * 1024
    if file_object.size > megabyte_limit:
        raise ValidationError("Audio file size cannot exceed 100 MB")

def get_path_upload_product_image(instance, file):
    return f"products/product_{instance.id}/{file}"


def get_path_upload_product_sub_image(instance, file):
    return f"products/product_{str(instance.product.id)}/{file}"

def get_path_upload_profile_image(instance, file):
    return f"profiles/user_{instance.id}/{file}"


def check_size_image(file_object):
    
    MAX_SIZE = 2 * 1024 * 1024
    if file_object.size > MAX_SIZE:
        raise ValidationError(
            f"Максимальный размер файла не должен превышать {MAX_SIZE}MB"
        )

def delete_old_file(path_file):
    if os.path.exists(path_file):
        os.remove(path_file)