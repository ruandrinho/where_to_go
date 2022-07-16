from django.contrib import admin
from django.utils.html import format_html
from places.models import Place, PlacePhoto


# Register your models here.
class PhotoInline(admin.TabularInline):
    model = PlacePhoto
    extra = 1
    readonly_fields = ['photo_preview', ]
    fields = ('photo', 'photo_preview', 'priority')

    def photo_preview(self, obj):
        height = min(obj.photo.height, 200)
        width = int(obj.photo.width * height / obj.photo.height)
        return format_html(
            '<img src="{}" width="{}" height="{}">',
            obj.photo.url, width, height
        )


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [PhotoInline, ]


@admin.register(PlacePhoto)
class PlacePhotoAdmin(admin.ModelAdmin):
    pass
