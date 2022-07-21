# Generated by Django 4.0.6 on 2022-07-21 05:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0005_alter_place_description_long_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placephoto',
            name='place',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='places.place', verbose_name='Компания'),
            preserve_default=False,
        ),
    ]