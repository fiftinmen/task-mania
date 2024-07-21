from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.messages import error
from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from task_manager.users.mixins import CustomLoginRequiredMixin

from .models import Label

# Create your views here.


class LabelsIndexView(CustomLoginRequiredMixin, ListView):
    model = Label
    pagination = 10
    template_name = "labels/index.html"
    next_page = reverse_lazy("index")


class LabelsDetailView(CustomLoginRequiredMixin, DetailView):
    model = Label
    template_name = "labels/detail.html"


class LabelsCreateView(
    CustomLoginRequiredMixin, SuccessMessageMixin, CreateView
):
    model = Label
    template_name = "labels/create.html"
    next_page = success_url = reverse_lazy("labels_index")
    success_message = _("Label_creation_success")
    fields = ["name"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class LabelsUpdateView(
    CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = Label
    template_name = "labels/update.html"
    next_page = success_url = reverse_lazy("labels_index")
    success_message = _("Label_update_success")
    fields = ["name"]


class LabelsDeleteView(
    CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView
):
    model = Label
    owner_field = "author"
    template_name = "labels/delete.html"
    perms = ["labels.delete_all"]
    next_page = success_url = reverse_lazy("labels_index")
    success_message = _("Label_deletion_success")

    def form_valid(self, form):
        if self.object.task_set.exists():
            error(self.request, _("Can't_delete_status_in_use"))
            return redirect(self.next_page)
        return super().form_valid(form)
