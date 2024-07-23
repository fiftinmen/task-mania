from django.conf import settings
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.messages import error


class CustomUserTestMixin:
    """Verify that the current user is authenticated."""

    permission_required = []
    permission_test = {}
    permission_denied_action = {}
    permission_denied_message = {}
    login_url = None
    next_page = ""

    def dispatch(self, request, *args, **kwargs):
        for perm in self.permission_required:
            if not self.permission_test[perm](request, perm, *args, **kwargs):
                return self.permission_denied_action[perm](
                    perm, request, *args, **kwargs
                )
        return super().dispatch(request, *args, **kwargs)

    def get_message(self, perm):
        return self.permission_denied_message.get(perm, _("not_permitted"))


class CustomLoginRequiredMixin(CustomUserTestMixin):

    login_url = None

    def __init__(self):
        super().__init__()
        perm = "login_required"
        self.permission_required = [perm]
        self.permission_test[perm] = self.is_user_authenticated
        self.permission_denied_action[perm] = self.redirect_to_login
        self.permission_denied_message[perm] = _(perm)

    def get_login_url(self):
        return self.login_url or settings.LOGIN_URL

    def is_user_authenticated(self, request, perm, *args, **kwargs):
        return request.user.is_authenticated

    def redirect_to_login(self, perm, request, *args, **kwargs):
        message = self.get_message(perm)
        error(request, message)
        return redirect(self.get_login_url(), *args, **kwargs)


class NotOwnObjectPermissionMixin(CustomLoginRequiredMixin):

    owner_field = "owner"

    def __init__(self):
        super().__init__()
        self.permission_required.extend(self.perms)
        for perm in self.perms:
            self.permission_test[perm] = self.is_user_permitted
            self.permission_denied_action[perm] = self.redirect_to_next_page
            if self.permission_denied_message.get(perm) is None:
                self.permission_denied_message[perm] = _(
                    "Not_permitted_to_modify_object"
                )

    def is_user_object_owner(self, request):
        obj = self.model.objects.get(pk=self.kwargs["pk"])
        return request.user.pk == getattr(obj, self.owner_field).pk

    def is_user_permitted(self, request, perm, *args, **kwargs):
        return self.is_user_object_owner(request) or request.user.has_perm(perm)

    def redirect_to_next_page(self, perm, request, *args, **kwargs):
        message = self.get_message(perm)
        error(request, message)
        return redirect(self.next_page, *args, **kwargs)


class UsersModifyPermissionMixin(NotOwnObjectPermissionMixin):

    next_page = "index"
    owner_field = "username"

    def is_user_object_owner(self, request):
        return request.user.pk == self.kwargs["pk"]
