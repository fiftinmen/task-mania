from django import views
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.messages import info, error, warning
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Status
from task_manager.mixins import CustomLoginRequiredMixin

# Create your views here.


class StatusesIndexView(CustomLoginRequiredMixin, ListView):
    model = Status
    pagination = 10
    template_name = "statuses/index.html"
    next_page = reverse_lazy("index")


class StatusesCreateView(
    CustomLoginRequiredMixin, SuccessMessageMixin, CreateView
):
    model = Status
    template_name = "statuses/create.html"
    next_page = success_url = reverse_lazy("statuses_index")
    success_message = _("Status_creation_success")
    fields = ["name"]


class StatusesUpdateView(
    CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = Status
    template_name = "statuses/update.html"
    next_page = success_url = reverse_lazy("statuses_index")
    success_message = _("Status_update_success")
    fields = ["name"]


class StatusesDeleteView(
    CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView
):
    model = Status
    template_name = "statuses/delete.html"
    next_page = success_url = reverse_lazy("statuses_index")
    success_message = _("Status_deletion_success")
