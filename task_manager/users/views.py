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
from . import forms, mixins
from django.contrib.auth.models import Group, Permission


class UsersIndexView(ListView):
    model = get_user_model()
    pagination = 5
    template_name = "users/index.html"


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

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            error(request, _("Not_enough_permissions"))
            return redirect("index")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        users_group, created = Group.objects.get_or_create(name="users_group")
        if created:
            users_group.permissions.add(
                Permission.objects.get(codename="self_update"),
                Permission.objects.get(codename="self_delete"),
            )
        response = super().form_valid(form)
        self.object.groups.set([users_group])
        self.object.save()
        return response


class UsersUpdateView(
    mixins.UsersPermissionRequiredMixin, SuccessMessageMixin, UpdateView
):
    permission_required = "users.self_update"
    permission_denied_message = _("Not_permitted_to_update_other_users")
    model = get_user_model()
    form_class = forms.UsersUpdateForm
    template_name = "users/update.html"
    next_page = success_url = reverse_lazy("users_index")
    success_message = _("Update_success")

    def get(self, request, *args, **kwargs):
        if request.user.pk != kwargs["pk"]:
            error(request, _("No_permissions_to_change_other_user"))
            return redirect("index")
        return super().get(request, *args, **kwargs)


class UsersDeleteView(
    mixins.UsersPermissionRequiredMixin, SuccessMessageMixin, DeleteView
):
    permission_required = "users.self_delete"
    permission_denied_message = _("Not_permitted_to_delete_other_users")
    model = get_user_model()
    template_name = "users/delete.html"
    next_page = success_url = reverse_lazy("users_index")
    success_message = _("Deletion_success")

    def get(self, request, *args, **kwargs):
        if request.user.pk != kwargs["pk"]:
            error(request, _("No_permissions_to_delete_other_user"))
            return redirect("index")
        return super().get(request, *args, **kwargs)


class UsersLogoutView(LogoutView):
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
