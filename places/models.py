from django.db import models
from tinymce.models import HTMLField


# Create your models here.
class Place(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название компании',
                             unique=True)
    description_short = models.TextField(verbose_name='Краткое описание',
                                         blank=True, default='')
    description_long = HTMLField(verbose_name='Полное описание',
                                 blank=True, default='')
    longitude = models.FloatField(verbose_name='Долгота')
    latitude = models.FloatField(verbose_name='Широта')

    class Meta:
        ordering = ['title', ]
        unique_together = ['longitude', 'latitude']

    def __str__(self):
        return self.title


class PlacePhoto(models.Model):
    photo = models.ImageField(verbose_name='Фото')
    priority = models.IntegerField(verbose_name='Порядковый номер',
                                   default=0)
    place = models.ForeignKey(Place, verbose_name='Компания', null=True,
                              on_delete=models.SET_NULL, related_name='photos')

    class Meta:
        ordering = ['priority', ]

    def __str__(self):
        return f'{self.priority} {self.place.title}'
