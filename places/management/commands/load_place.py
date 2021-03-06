from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import IntegrityError
from places.models import Place, PlacePhoto
from urllib.parse import urlsplit, unquote
from random import randint
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
            new_place_object, created = Place.objects.get_or_create(
                title=new_place.get('title')
            )
            if not created:
                logger.warning('Объект с таким заголовком уже существует')
                continue

            description_short = new_place.get('description_short')
            if description_short:
                new_place_object.description_short = description_short

            description_long = new_place.get('description_long')
            if description_long:
                new_place_object.description_long = description_long

            new_place_object.save()

            coordinates = new_place.get('coordinates')
            if coordinates:
                longitude = coordinates.get('lng')
                if longitude:
                    new_place_object.longitude = longitude
                latitude = coordinates.get('lat')
                if latitude:
                    new_place_object.latitude = latitude

            try:
                new_place_object.save()
            except IntegrityError:
                logger.warning('Объект с такими широтой и долготой уже '
                               'существует, будут установлены случайные '
                               'координаты вне существующего диапазона')
                new_place_object.longitude = randint(1000000, 9999999)
                new_place_object.latitude = randint(1000000, 9999999)
                new_place_object.save()

            img_urls = new_place.get('imgs')
            if not img_urls:
                continue

            for img_url in img_urls:
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
