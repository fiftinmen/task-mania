from urllib.parse import urlparse

from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.messages import error
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import resolve_url
from django.contrib.auth.mixins import PermissionRequiredMixin


class UsersPermissionRequiredMixin(PermissionRequiredMixin):

    authentication_required_message = _("authorization_required")
    permission_denied_message = ""

    def has_permission(self):
        return super().has_permission()

    def handle_no_permission(self):
        print(self.request.user.groups)
        if self.request.user.is_authenticated:
            error(
                self.request,
                self.get_permission_denied_message(),
            )
            return redirect(self.next_page)

        error(
            self.request,
            self.authentication_required_message,
        )
        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())
        # If the login url is the same scheme and net location then use the
        # path as the "next" url.
        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (not login_scheme or login_scheme == current_scheme) and (
            not login_netloc or login_netloc == current_netloc
        ):
            path = self.request.get_full_path()
        return redirect_to_login(
            path,
            resolved_login_url,
            self.get_redirect_field_name(),
        )
