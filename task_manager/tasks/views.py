from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

# from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from task_manager.users.mixins import CustomLoginRequiredMixin
from .filters import TasksFilter
from .models import Task
from .mixins import TasksModifyPermissionMixin
from django_filters.views import FilterView

# Create your views here.


""" class TasksIndexView(CustomLoginRequiredMixin, ListView):
    model = Task
    pagination = 10
    template_name = "tasks/index.html"
    next_page = reverse_lazy("index") """


class TasksIndexView(CustomLoginRequiredMixin, FilterView):
    model = Task
    pagination = 10
    template_name = "tasks/index.html"
    next_page = reverse_lazy("index")
    filterset_class = TasksFilter
    extra_context = {"page_header": _("Tasks")}


class TasksDetailView(CustomLoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/detail.html"


class TasksCreateView(
    CustomLoginRequiredMixin, SuccessMessageMixin, CreateView
):
    model = Task
    template_name = "tasks/create.html"
    next_page = success_url = reverse_lazy("tasks_index")
    success_message = _("Task_creation_success")
    fields = ["name", "description", "status", "executor", "labels"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TasksUpdateView(
    CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = Task
    template_name = "tasks/update.html"
    next_page = success_url = reverse_lazy("tasks_index")
    success_message = _("Task_update_success")
    fields = ["name", "description", "status", "executor", "labels"]


class TasksDeleteView(
    TasksModifyPermissionMixin, SuccessMessageMixin, DeleteView
):
    model = Task
    owner_field = "author"
    template_name = "tasks/delete.html"
    perms = ["tasks.delete_all"]
    next_page = success_url = reverse_lazy("tasks_index")
    success_message = _("Task_deletion_success")
