from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.messages import info, error, warning
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from . import forms
from .mixins import CustomLoginRequiredMixin, UsersModifyPermissionMixin


class UsersIndexView(ListView):
    model = get_user_model()
    pagination = 10
    template_name = "users/index.html"
    extra_context = {"page_header": _("Users")}


class UsersDetailView(DetailView):
    model = get_user_model()
    template_name = "users/detail.html"

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            return self.request.user
        return redirect("index")


class UsersLoginView(SuccessMessageMixin, LoginView):
    model = get_user_model()
    template_name = "users/login.html"
    next_page = success_url = reverse_lazy("index")
    success_message = _("Logged_in")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            warning(request, _("Already_logged_in"))
            return redirect("index")
        return super().get(request, *args, **kwargs)


class UsersCreateView(SuccessMessageMixin, CreateView):
    form_class = forms.UsersRegisterForm
    template_name = "users/create.html"
    next_page = success_url = reverse_lazy("index")
    success_message = _("Registration_success")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            error(request, _("Not_enough_permissions"))
            return redirect("index")
        return super().dispatch(request, *args, **kwargs)


class UsersUpdateView(
    UsersModifyPermissionMixin, SuccessMessageMixin, UpdateView
):
    model = get_user_model()
    perms = ["users.update_all"]
    form_class = forms.UsersUpdateForm
    template_name = "users/update.html"
    next_page = success_url = reverse_lazy("users_index")
    success_message = _("User_update_success")


class UsersDeleteView(
    UsersModifyPermissionMixin, SuccessMessageMixin, DeleteView
):
    model = get_user_model()
    perms = ["users.delete_all"]
    template_name = "users/delete.html"
    next_page = success_url = reverse_lazy("users_index")
    success_message = _("User_deletion_success")


class UsersLogoutView(CustomLoginRequiredMixin, LogoutView):
    next_page = success_url = reverse_lazy("index")
    template_name = "index.html"

    def post(self, request, *args, **kwargs):
        info(request, _("Logout"))
        return super().post(request, *args, **kwargs)


o = [
    "Вы разлогинены",
    "Пользователь успешно зарегистрирован",
    "Вы залогинены",
    "У вас нет прав для изменения другого пользователя.",
    "Пользователь успешно изменен",
    "Вы не авторизованы! Пожалуйста, выполните вход.",
]
