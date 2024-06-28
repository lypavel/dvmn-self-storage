from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .coordinates import get_nearest_storage
from .forms import ConsultationForm, OrderForm
from .models import Storage, Box


def index(request):
    nearest_storage_id = get_nearest_storage(request)
    if not nearest_storage_id:
        nearest_storage_id = Storage.objects \
            .select_related('city') \
            .order_by('?') \
            .first() \
            .id

    nearest_storage = Storage.objects.filter(id=nearest_storage_id)
    nearest_storage = nearest_storage.annotate_min_price()
    nearest_storage = nearest_storage.annotate_boxes_available()

    serialized_nearest_storage = serialize_storage(nearest_storage.first())
    context = {
        'nearest_storage': serialized_nearest_storage,
        'consultation_form': ConsultationForm()
    }

    return render(request, 'storage/index.html', context)


def storages(request):
    storages = Storage.objects.annotate_min_price()
    storages = storages.annotate_boxes_available()
    serialized_storages = [
        serialize_storage(storage) for storage in storages.iterator()
    ]

    context = {
        'storages': serialized_storages,
        'consultation_form': ConsultationForm(),
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
        'boxes': categorized_boxes,
        'consultation_form': ConsultationForm(),
    }

    return render(request, 'storage/boxes.html', context)


def faq(request):
    return render(
        request,
        'storage/faq.html',
        context={'consultation_form': ConsultationForm()}
    )


@login_required
def profile(request):
    user = request.user

    return render(
        request,
        'storage/profile.html',
        context={
            'user': user
        }
    )


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
        'id': box.id,
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


def order_consultation(request):
    return render(
        request,
        'storage/order-consultation.html',
        context={'consultation_form': ConsultationForm()}
    )


@transaction.atomic()
def process_consultation(request):
    form = ConsultationForm()
    if not request.method == 'POST':
        return render(
            request,
            'storage/forms/success.html',
            context={'consultation_form': form}
        )

    form = ConsultationForm(request.POST)
    if not form.is_valid():
        return render(
            request,
            'storage/forms/success.html',
            context={'consultation_form': form}
        )

    form.save()
    return render(request, 'storage/forms/success.html')


@transaction.atomic()
def order_box(request, box_id):
    if request.user.is_anonymous:
        return redirect(reverse('user:login'))

    box = Box.objects.select_related('storage', 'owner').get(id=box_id)

    serialized_box = {
        'id': box.id,
        'number': box.number,
        'sizes': box.sizes,
        'price': box.price,
        'storage': f'{box.storage.city}, {box.storage.address}'
    }

    if box.owner is not None:
        if box.owner.id != request.user.id:
            return HttpResponse('Ячейка уже занята.')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            rent = form.save(commit=False)
            period = form.cleaned_data['period']
            start_date = form.cleaned_data['start_date']
            rent.user = request.user
            rent.box = box
            rent.price = serialized_box['price'] * period
            rent.start_date = start_date
            rent.end_date = start_date + relativedelta(months=period)
            rent.save()

            Box.objects.filter(pk=box.id).update(owner=request.user)

        context = {
            'box': serialized_box,
            'rent': rent,
            'rent_period': period,
            'order_form': None
        }

        return render(request, 'storage/order-box.html', context)

    context = {
        'box': serialized_box,
        'order_form': OrderForm()
    }

    return render(request, 'storage/order-box.html', context)


def confirm_box_order(request, box_id):
    print(request.POST)

    box = Box.objects.select_related('storage', 'owner').get(id=box_id)

    serialized_box = {
        'id': box.id,
        'number': box.number,
        'sizes': box.sizes,
        'price': box.price,
        'storage': f'{box.storage.city}, {box.storage.address}'
    }

    context = {
        'box': serialized_box,
        'total_price': 0
    }
    return (request, 'storage/order-confirm.html', context)
