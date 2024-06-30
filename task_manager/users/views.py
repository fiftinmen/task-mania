from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


class UsersIndexView(ListView):
    model = User
    pagination = 50
    template_name = "users/users_index.html"


class UsersDetailView(DetailView):
    model = User
    template_name = "users/users_detail.html"


def users_index(request):
    return render(request, "index.html")


def login(request):
    return render(request, "index.html")


def users_create(request):
    return render(request, "index.html")
