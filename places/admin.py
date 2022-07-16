from django.contrib import admin
from places.models import Place, PlacePhoto

# Register your models here.
class PhotoInline(admin.TabularInline):
    model = PlacePhoto
    extra = 1
    
@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [PhotoInline,]

admin.site.register(PlacePhoto)