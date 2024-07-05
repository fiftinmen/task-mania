from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
)
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, password_validation
from django.forms.models import ModelForm
from django import forms
from django.utils.translation import gettext_lazy as _


class UsersAccountForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = [
            "first_name",
            "last_name",
            "username",
        ]


class UsersRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)

    class Meta(UserCreationForm.Meta, UsersAccountForm.Meta):
        model = get_user_model()
        fields = [
            "first_name",
            "last_name",
            "username",
        ]


class UsersUpdateForm(UserChangeForm):
    password = None

    class Meta(UsersAccountForm.Meta):
        model = get_user_model()

    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        password_validation.validate_password(password2, self.instance)
        return password2

    def save(self, commit=True):
        self.instance = super().save()
        password = self.cleaned_data["new_password1"]
        self.instance.set_password(password)
        if commit:
            self.instance.save()
        return self.instance
