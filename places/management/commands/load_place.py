from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import IntegrityError
from places.models import Place, PlacePhoto
from urllib.parse import urlsplit, unquote
import requests
import logging
import os
import uuid

logger = logging.getLogger(__name__)


def get_filename_from_url(url):
    path = urlsplit(url).path
    path = unquote(path)
    return os.path.split(path)[1]


def get_unique_media_filename(media_path, filename):
    path_to_file = media_path / filename
    while path_to_file.is_file():
        extension = os.path.splitext(filename)[1]
        filename = f'{uuid.uuid4().hex}.{extension}'
        path_to_file = media_path / filename
    return filename


class Command(BaseCommand):
    help = 'Загрузка нового объекта в базу данных'

    def add_arguments(self, parser):
        parser.add_argument('json_urls', nargs='+', type=str)

    def handle(self, *args, **options):
        for json_url in options['json_urls']:
            try:
                new_place_response = requests.get(json_url)
                new_place_response.raise_for_status()
            except requests.exceptions.RequestException:
                logger.warning(f'Не удалось загрузить url {json_url}')
                continue
            try:
                new_place = new_place_response.json()
            except requests.exceptions.JSONDecodeError:
                logger.warning(f'Не удалось считать данные из url {json_url}')
                continue
            logger.warning(f'Создаём объект {new_place.get("title")}')
            try:
                new_place_object, created = Place.objects.get_or_create(
                    title=new_place.get('title'),
                    description_short=new_place.get('description_short'),
                    description_long=new_place.get('description_long'),
                    longitude=new_place.get('coordinates').get('lng'),
                    latitude=new_place.get('coordinates').get('lat')
                )
            except IntegrityError:
                logger.warning(f'Не удалось создать объект из url {json_url}')
                continue
            if not created:
                logger.warning(f'Не удалось создать объект из url {json_url}')
                continue
            for img_url in new_place.get('imgs'):
                filename = get_filename_from_url(img_url)
                filename = get_unique_media_filename(settings.MEDIA_ROOT,
                                                     filename)
                logger.warning(f'Скачиваем файл {filename}')
                try:
                    image_response = requests.get(img_url)
                    image_response.raise_for_status()
                except requests.exceptions.RequestException:
                    continue
                content_file = ContentFile(image_response.content)
                new_place_photo = PlacePhoto.objects.create(
                    place=new_place_object)
                new_place_photo.photo.save(filename, content_file, save=True)
