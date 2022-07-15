from django.db import models

# Create your models here.
class Place(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название компании')
    description_short = models.TextField(verbose_name='Краткое описание',
                                        null=True)
    description_long = models.TextField(verbose_name='Полное описание',
                                       null=True, blank=True)
    longitude = models.FloatField(verbose_name='Долгота')
    latitude = models.FloatField(verbose_name='Широта')
    
    def __str__(self):
        return self.title
