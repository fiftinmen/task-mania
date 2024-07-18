from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Task
from task_manager.mixins import CustomLoginRequiredMixin

# Create your views here.


class TasksIndexView(CustomLoginRequiredMixin, ListView):
    model = Task
    pagination = 10
    template_name = "tasks/index.html"
    next_page = reverse_lazy("index")


class TasksCreateView(
    CustomLoginRequiredMixin, SuccessMessageMixin, CreateView
):
    model = Task
    template_name = "tasks/create.html"
    next_page = success_url = reverse_lazy("tasks_index")
    success_message = _("Task_creation_success")
    fields = ["name"]


class TasksUpdateView(
    CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = Task
    template_name = "tasks/update.html"
    next_page = success_url = reverse_lazy("tasks_index")
    success_message = _("Task_update_success")
    fields = ["name"]


class TasksDeleteView(
    CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView
):
    model = Task
    template_name = "tasks/delete.html"
    next_page = success_url = reverse_lazy("tasks_index")
    success_message = _("Task_deletion_success")
