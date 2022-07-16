from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from places.models import Place


def main_page(request):
    places_for_page = {
        'type': 'FeatureCollection',
        'features': []
    }
    for place in Place.objects.all():
        place_for_page = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [place.longitude, place.latitude]
            },
            'properties': {
                'title': place.title,
                'placeId': place.id,
                'detailsUrl': f'/places/{place.id}/'
            }
        }
        places_for_page['features'].append(place_for_page)
    context = {'places_for_page': places_for_page}
    return render(request, 'index.html', context=context)


def place_detail_view(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    context = {
        'title': place.title,
        'imgs': [photo.photo.url for photo in
                 place.photos.all().order_by('priority')],
        'description_short': place.description_short,
        'description_long': place.description_long,
        'coordinates': {
            'lng': place.longitude,
            'lat': place.latitude
        }
    }
    return JsonResponse(context, safe=False,
                        json_dumps_params={'ensure_ascii': False, 'indent': 4})
