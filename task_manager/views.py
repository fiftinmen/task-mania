from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def users_index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'index.html')


def users_create(request):
    return render(request, 'index.html')
