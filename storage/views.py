from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .coordinates import get_nearest_storage
from .models import Storage


def index(request):
    nearest_storage_id = get_nearest_storage(request)
    if not nearest_storage_id:
        nearest_storage_id = Storage.objects\
            .select_related('city')\
            .order_by('?')\
            .first()\
            .id

    nearest_storage = Storage.objects.filter(id=nearest_storage_id)
    nearest_storage = nearest_storage.annotate_min_price()
    nearest_storage = nearest_storage.annotate_boxes_available()

    serialized_nearest_storage = serialize_storage(nearest_storage.first())
    context = {
        'nearest_storage': serialized_nearest_storage
    }

    return render(request, 'storage/index.html', context)


def storages(request):
    storages = Storage.objects.annotate_min_price()
    storages = storages.annotate_boxes_available()
    serialized_storages = [
        serialize_storage(storage) for storage in storages.iterator()
    ]

    context = {
        'storages': serialized_storages
    }

    return render(request, 'storage/storages.html', context)


def boxes(request, storage_id):
    try:
        current_storage = get_object_or_404(
            Storage.objects.prefetch_related('boxes'),
            id=storage_id
        )
    except Http404:
        return redirect('storage:storages')

    all_boxes = current_storage.boxes.filter(owner=None)
    serialized_boxes = [serialize_box(box) for box in all_boxes]

    categorized_boxes = categorize_boxes(serialized_boxes)

    storages = Storage.objects.prefetch_related('images').annotate_min_price()
    storages = storages.annotate_boxes_available()

    serialized_storages = []
    for storage in storages.iterator():
        serialized_storage = serialize_storage(storage)
        if storage.id == storage_id:
            serialized_storage['images'] = [
                image.image.url for image in storage.images.all()
                if image.image.url != serialized_storage['image']
            ]
            current_storage_serialized = serialized_storage
        serialized_storages.append(serialized_storage)

    context = {
        'storages': serialized_storages,
        'current_storage': current_storage_serialized,
        'boxes': categorized_boxes
    }

    return render(request, 'storage/boxes.html', context)


def faq(request):
    return render(request, 'storage/faq.html')


def profile(request):
    return render(request, 'storage/profile.html')


def serialize_storage(storage):
    if storage.images.count():
        image = storage.images.first().image.url
    else:
        image = None

    return {
        'id': storage.id,
        'city': storage.city.name,
        'address': storage.address,
        'max_boxes': storage.max_boxes,
        'boxes_available': storage.boxes_available,
        'min_price': storage.min_price,
        'contacts': storage.contacts,
        'description': storage.description,
        'route': storage.route,
        'image': image,
        'temperature': round(storage.temperature),
        'ceiling_height': storage.ceiling_height,
        'feature': storage.feature if storage.feature else None
    }


def serialize_box(box):
    return {
        'number': box.number,
        'type': box.type,
        'floor': box.floor,
        'sizes': box.sizes,
        'volume': box.volume,
        'price': box.price
    }


def categorize_boxes(boxes):
    boxes_to_3 = []
    boxes_to_10 = []
    boxes_from_10 = []

    for box in boxes:
        match box['type']:
            case '3':
                boxes_to_3.append(box)
            case '10':
                boxes_to_10.append(box)
            case '10+':
                boxes_from_10.append(box)

    return {
        'boxes_to_3': boxes_to_3,
        'boxes_to_10': boxes_to_10,
        'boxes_from_10': boxes_from_10,
        'all_boxes': boxes
    }
