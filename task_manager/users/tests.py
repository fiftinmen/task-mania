from django.urls import reverse_lazy
from django.test import TestCase, Client
from .models import CustomUser
from .fixtures.fixtures import (
    valid_users,
    invalid_users,
    extended_valid_users,
    other_user_data,
)
from task_manager._test_utils._test_utils import _TestUtilsMixin


class _TestUsersUtilsMixin(_TestUtilsMixin):
    def delete_user(self, username):
        if username:
            if user := CustomUser.objects.filter(username=username):
                user.delete()

    def delete_users(self, users=None):
        if not users:
            users = (
                {"username": user.username} for user in CustomUser.objects.all()
            )
        [self.delete_user(user["username"]) for user in users]

    def get_or_create_user(self, user_data, force_recreate=False):
        if force_recreate:
            self.delete_user(user_data["username"])
        user, _ = CustomUser.objects.get_or_create(
            username=user_data["username"],
            password=user_data.get("password")
            or user_data.get("password1")
            or user_data.get("new_password1"),
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
        )
        return user


# Create your tests here.
class TestUsersPostCRUDSs(TestCase, _TestUsersUtilsMixin):
    def setUp(self):
        self.subject = "Users app (post method)"
        self.client = Client()
        self._tests_to_success_tuple = (
            ("_test_users_create_post_success", valid_users),
            ("_test_users_update_post_success", valid_users),
            ("_test_users_delete_post_success", valid_users),
        )
        self._tests_to_fail_tuple = (
            ("_test_users_create_post_fail", invalid_users),
            ("_test_users_create_by_user_post_fail", valid_users),
            ("_test_users_create_existing_user_post_fail", valid_users),
            (
                "_test_users_update_post_fail",
                tuple(zip(extended_valid_users, invalid_users)),
            ),
            ("_test_users_delete_post_fail", valid_users),
        )

    def _test_users_create_post_success(self, user):
        data = {
            "username": user["username"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "password1": user["password1"],
            "password2": user["password2"],
        }

        self.assertFalse(
            CustomUser.objects.filter(username=data["username"]).exists()
        )
        response = self.client.post(reverse_lazy("users_create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("index"))
        self.assertTrue(
            CustomUser.objects.filter(username=data["username"]).exists()
        )

    def _test_users_update_post_success(self, user):
        data = {
            "username": user["username"],
            "first_name": user["last_name"],
            "last_name": user["first_name"],
            "new_password1": user["password1"],
            "new_password2": user["password2"],
        }

        self.client.force_login(
            user=CustomUser.objects.get(username=user["username"])
        )
        url = reverse_lazy("users_update", args=(user["pk"],))
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users_index"))
        updated_user = CustomUser.objects.get(username=data["username"])
        self.assertEqual(
            (updated_user.first_name, updated_user.last_name),
            (data["first_name"], data["last_name"]),
        )

    def _test_users_delete_post_success(self, user):
        pk = user["pk"]

        self.client.force_login(
            user=CustomUser.objects.get(username=user["username"])
        )
        url = reverse_lazy("users_delete", args=(pk,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users_index"))
        self.assertFalse(
            CustomUser.objects.filter(username=user["username"]).exists()
        )

    def _test_users_create_post_fail(self, user_data):
        user_data = {
            "username": user_data["username"],
            "password1": user_data["new_password1"],
            "password2": user_data["new_password2"],
        }

        self.assertFalse(
            CustomUser.objects.filter(username=user_data["username"]).exists()
        )
        response = self.client.post(reverse_lazy("users_create"), user_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            CustomUser.objects.filter(username=user_data["username"]).exists()
        )

    def _test_users_create_existing_user_post_fail(self, user):
        self.client.logout()
        data = {
            "username": user["username"],
            "first_name": user["last_name"],
            "last_name": user["first_name"],
            "new_password1": user["password1"],
            "new_password2": user["password2"],
        }
        self.get_or_create_user(data, force_recreate=True)
        self.assertTrue(
            CustomUser.objects.filter(username=data["username"]).exists()
        )
        self.client.logout()
        response = self.client.post(reverse_lazy("users_create"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            CustomUser.objects.filter(username=data["username"]).count(), 1
        )

    def _test_users_create_by_user_post_fail(self, user):
        data = user | {"username": user["username"] + "x"}
        self.get_or_create_user(user, force_recreate=True)

        self.assertTrue(
            CustomUser.objects.filter(username=user["username"]).exists()
        )
        self.assertFalse(
            CustomUser.objects.filter(username=data["username"]).exists()
        )
        self.client.force_login(
            user=CustomUser.objects.get(username=user["username"])
        )
        response = self.client.post(reverse_lazy("users_create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("index"))
        self.assertTrue(
            CustomUser.objects.filter(username=user["username"]).exists()
        )

    def _test_users_update_post_fail(self, data):
        valid_user_data = data[0]
        valid_user = self.get_or_create_user(
            valid_user_data, force_recreate=True
        )
        invalid_user_data = data[1]

        self.client.logout()
        url = reverse_lazy("users_update", args=(valid_user.id,))
        response = self.client.post(url, invalid_user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users_login"))
        updated_user = CustomUser.objects.get(username=valid_user.username)
        self.assertEqual(
            (
                updated_user.username,
                updated_user.first_name,
                updated_user.last_name,
            ),
            (
                valid_user.username,
                valid_user.first_name,
                valid_user.last_name,
            ),
        )

        self.client.force_login(user=valid_user)
        url = reverse_lazy("users_update", args=(valid_user.id,))
        response = self.client.post(url, invalid_user_data)
        self.assertEqual(response.status_code, 200)
        updated_user = CustomUser.objects.get(username=valid_user.username)
        self.assertEqual(
            (
                updated_user.username,
                updated_user.first_name,
                updated_user.last_name,
            ),
            (
                valid_user.username,
                valid_user.first_name,
                valid_user.last_name,
            ),
        )

        other_user = self.get_or_create_user(other_user_data)
        url = reverse_lazy("users_update", args=(other_user.id,))
        response = self.client.post(url, valid_user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users_index"))
        updated_user = CustomUser.objects.get(id=other_user.id)
        self.assertEqual(
            (
                updated_user.username,
                updated_user.first_name,
                updated_user.last_name,
            ),
            (
                other_user_data["username"],
                other_user_data["first_name"],
                other_user_data["last_name"],
            ),
        )

    def _test_users_delete_post_fail(self, user_data):
        valid_user = self.get_or_create_user(user_data, force_recreate=True)

        self.client.logout()
        url = reverse_lazy("users_delete", args=(valid_user.id,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users_login"))
        updated_user = CustomUser.objects.get(username=valid_user.username)
        self.assertEqual(
            (updated_user.first_name, updated_user.last_name),
            (valid_user.first_name, valid_user.last_name),
        )

        self.client.force_login(user=valid_user)
        other_user = self.get_or_create_user(other_user_data)
        url = reverse_lazy("users_delete", args=(other_user.id,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users_index"))
        self.assertTrue(CustomUser.objects.filter(id=other_user.id).exists())


class TestUsersGetCRUDSs(TestCase, _TestUsersUtilsMixin):
    def setUp(self):
        self.subject = "Users app (get method)"
        self.client = Client()
        self._tests_to_success_tuple = (
            ("_test_users_get_success", valid_users),
        )
        self._tests_to_fail_tuple = (("_test_users_get_fail", valid_users),)

    def _test_users_get_success(self, user):
        self.client.logout()
        response = self.client.get(reverse_lazy("users_index"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, user["username"])
        self.assertNotContains(response, user["first_name"])
        self.assertNotContains(response, user["last_name"])
        self.get_or_create_user(user, force_recreate=True)

        response = self.client.get(reverse_lazy("users_create"))
        self.assertEqual(response.status_code, 200)

        self.client.force_login(
            user=CustomUser.objects.get(username=user["username"])
        )
        response = self.client.get(
            reverse_lazy("users_update", args=(user["pk"],))
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            reverse_lazy("users_update", args=(user["pk"],))
        )
        self.assertEqual(response.status_code, 200)

    def _test_users_get_fail(self, user):
        valid_user = self.get_or_create_user(user)
        self.client.force_login(valid_user)
        response = self.client.get(reverse_lazy("users_create"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("index"))

        other_user = self.get_or_create_user(other_user_data)

        url = reverse_lazy("users_update", args=(other_user.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users_index"))

        url = reverse_lazy("users_delete", args=(other_user.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users_index"))

        self.client.logout()

        url = reverse_lazy("users_update", args=(valid_user.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users_login"))

        url = reverse_lazy("users_delete", args=(valid_user.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users_login"))
