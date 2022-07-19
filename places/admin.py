from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminBase, SortableTabularInline
from places.models import Place, PlacePhoto


class PhotoInline(SortableTabularInline):
    model = PlacePhoto
    extra = 1
    readonly_fields = ['photo_preview', ]
    fields = ('priority', 'photo', 'photo_preview')

    def photo_preview(self, obj):
        height = min(obj.photo.height, 200)
        width = int(obj.photo.width * height / obj.photo.height)
        return format_html(
            '<img src="{}" width="{}" height="{}">',
            obj.photo.url, width, height
        )


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [PhotoInline, ]
    search_fields = ['title', ]
    list_display = ['title', 'longitude', 'latitude']


# Uncomment this to show "Place Photos" in admin menu
# @admin.register(PlacePhoto)
# class PlacePhotoAdmin(admin.ModelAdmin):
#     pass
