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
            users_passes_test = self.permission_test[perm]
            action = self.permission_denied_action[perm]
            if not users_passes_test(request, perm, *args, **kwargs):
                return action(perm, request, *args, **kwargs)
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


class UsersModifyPermissionMixin(CustomLoginRequiredMixin):

    next_page = "index"

    def __init__(self):
        super().__init__()
        perms = [
            "users.update_others",
            "users.delete_others",
        ]
        self.permission_required.extend(perms)
        for perm in perms:
            self.permission_test[perm] = self.is_user_permitted_to_modify_others
            self.permission_denied_action[perm] = self.redirect_to_next_page
            self.permission_denied_message[perm] = _(
                "Not_permitted_to_modify_other_users"
            )

    def is_user_permitted_to_modify_others(
        self, request, perm, *args, **kwargs
    ):
        user_pk = request.user.pk
        target_user_pk = self.kwargs.get("pk")
        if user_pk != target_user_pk:
            return request.user.has_perms((perm,))
        return True

    def redirect_to_next_page(self, perm, request, *args, **kwargs):
        message = self.get_message(perm)
        error(request, message)
        return redirect(self.next_page, *args, **kwargs)
