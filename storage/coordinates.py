from geopy import distance
import requests

from .models import Storage


def get_location_by_ip(ip):
    url = f'http://ipwho.is/{ip}'
    response = requests.get(url)
    response.raise_for_status()

    location = response.json()
    lat, lng = location['latitude'], location['longitude']

    return lat, lng


def get_nearest_storage(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    try:
        user_coords = get_location_by_ip(ip)
    except Exception:
        return None

    nearest_storage = None
    minimal_distance = None

    storages = Storage.objects.select_related('city').iterator()
    for storage in storages:
        storage_coords = storage.latitude, storage.longitude
        if not storage.latitude or not storage.longitude:
            continue
        storage_distance = round(
            distance.distance(storage_coords, user_coords).km, 2
        )
        if not minimal_distance:
            minimal_distance = storage_distance
            nearest_storage = storage
        elif storage_distance < minimal_distance:
            minimal_distance = storage_distance
            nearest_storage = storage

    if not nearest_storage:
        return None
    return nearest_storage.id
