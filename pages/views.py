from django.shortcuts import render


def tariffs(request):
    return render(request, 'pages/tariffs.html')


def reviews(request):
    return render(request, 'pages/reviews.html')


def contacts(request):
    return render(request, 'pages/contacts.html')
