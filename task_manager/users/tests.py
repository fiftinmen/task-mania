from django.urls import reverse_lazy
from django.test import TestCase, Client
from .models import CustomUser
from .fixtures.fixtures import valid_users, invalid_users, extended_valid_users
from task_manager._test_utils._test_utils import _TestUtilsMixin


class _TestUsersUtilsMixin(_TestUtilsMixin):
    def delete_user(self, username):
        if username:
            if user := CustomUser.objects.filter(username=username):
                user.delete()

    def delete_users(self, users=[]):
        if not users:
            users = (
                {"username": user.username} for user in CustomUser.objects.all()
            )
        [self.delete_user(user["username"]) for user in users]

    def create_user(self, user_data, force=False):
        if force:
            self.delete_user(user_data["username"])
        user = CustomUser.objects.get_or_create(
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
        print("Test create user (POST) with data: ", data, end=" => ")
        self.assertFalse(
            CustomUser.objects.filter(username=data["username"]).exists()
        )
        response = self.client.post(reverse_lazy("users_create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("index"))
        self.assertTrue(
            CustomUser.objects.filter(username=data["username"]).exists()
        )
        print("succeeded.")

    def _test_users_update_post_success(self, user):
        data = {
            "username": user["username"],
            "first_name": user["last_name"],
            "last_name": user["first_name"],
            "new_password1": user["password1"],
            "new_password2": user["password2"],
        }
        print("Test update user with data: ", data, end=" => ")
        self.client.login(username=user["username"], password=user["password1"])
        url = reverse_lazy("users_update", args=(user["id"],))
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users_index"))
        updated_user = CustomUser.objects.get(username=data["username"])
        self.assertEqual(
            (updated_user.first_name, updated_user.last_name),
            (data["first_name"], data["last_name"]),
        )
        print("succeeded.")

    def _test_users_delete_post_success(self, user):
        id = user["id"]
        print("Test delete user with id: ", id, end=" => ")
        self.client.login(username=user["username"], password=user["password1"])
        url = reverse_lazy("users_delete", args=(id,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users_index"))
        self.assertFalse(
            CustomUser.objects.filter(username=user["username"]).exists()
        )
        print("succeeded.")

    def _test_users_create_post_fail(self, user):
        data = {
            "username": user["username"],
            "password1": user["password1"],
            "password2": user["password2"],
        }
        print("Test delete user with bad data: ", data, end=" => ")
        self.assertFalse(
            CustomUser.objects.filter(username=data["username"]).exists()
        )
        response = self.client.post(reverse_lazy("users_create"), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            CustomUser.objects.filter(username=data["username"]).exists()
        )
        print("successfully failed.")

    def _test_users_create_existing_user_post_fail(self, user):
        data = {
            "username": user["username"],
            "first_name": user["last_name"],
            "last_name": user["first_name"],
            "new_password1": user["password1"],
            "new_password2": user["password2"],
        }
        self.create_user(data, force=True)
        print(
            "Test create existing user (POST) with data to fail: ",
            data,
            end=" => ",
        )
        self.assertTrue(
            CustomUser.objects.filter(username=data["username"]).exists()
        )
        response = self.client.post(reverse_lazy("users_create"), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            CustomUser.objects.filter(username=data["username"]).exists()
        )
        print("successfully failed.")

    def _test_users_create_by_user_post_fail(self, user):
        data = user | {"username": user["username"] + "x"}
        self.create_user(user, force=True)
        print(
            "Test create existing user by user (POST) with data to fail: ",
            data,
            end=" => ",
        )
        self.assertTrue(
            CustomUser.objects.filter(username=user["username"]).exists()
        )
        self.assertFalse(
            CustomUser.objects.filter(username=data["username"]).exists()
        )
        self.client.login(username=user["username"], password=user["password1"])
        response = self.client.post(reverse_lazy("users_create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("index"))
        self.assertTrue(
            CustomUser.objects.filter(username=user["username"]).exists()
        )
        print("successfully failed.")

    def _test_users_update_post_fail(self, data):
        valid_user_data = data[0]
        valid_user, _ = self.create_user(valid_user_data, force=True)
        invalid_user_data = data[1]
        test_data = {
            "username": invalid_user_data["username"],
            "first_name": invalid_user_data["first_name"],
            "last_name": invalid_user_data["last_name"],
            "new_password1": invalid_user_data["password1"],
            "new_password2": invalid_user_data["password1"],
        }
        print("Test update user with broken data: ", test_data, end=" => ")

        print("Test updating data without authentication")
        self.client.logout()
        url = reverse_lazy("users_update", args=(valid_user.id,))
        response = self.client.post(url, test_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users_login"))
        updated_user = CustomUser.objects.get(username=valid_user.username)
        self.assertEqual(
            (updated_user.first_name, updated_user.last_name),
            (valid_user.first_name, valid_user.last_name),
        )

        print("Test updating data with bad data")
        self.client.login(
            username=valid_user.username, password=valid_user.password
        )
        url = reverse_lazy("users_update", args=(valid_user.id,))
        response = self.client.post(url, test_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users_update"))
        updated_user = CustomUser.objects.get(username=valid_user.username)
        self.assertEqual(
            (updated_user.first_name, updated_user.last_name),
            (valid_user.first_name, valid_user.last_name),
        )

        print("Test updating other user's data")
        self.client.login(
            username=valid_user.username, password=valid_user.password
        )
        other_users_id = list({1, 2, 3} ^ {valid_user.id})[0]
        url = reverse_lazy("users_update", args=(other_users_id,))
        response = self.client.post(url, test_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users_index"))
        updated_user = CustomUser.objects.get(username=valid_user.username)
        self.assertEqual(
            (updated_user.first_name, updated_user.last_name),
            (valid_user.first_name, valid_user.last_name),
        )
        print("All successfully failed.")

    def _test_users_delete_post_fail(self, user_data):
        valid_user, _ = self.create_user(user_data, force=True)

        print("Test delete user: ", user_data, end=" => ")

        print("Test deleting data without authentication")
        url = reverse_lazy("users_delete", args=(valid_user.id,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users_login"))
        updated_user = CustomUser.objects.get(username=valid_user.username)
        self.assertEqual(
            (updated_user.first_name, updated_user.last_name),
            (valid_user.first_name, valid_user.last_name),
        )

        print("Test deleting other user's data")
        self.client.login(
            username=valid_user.username, password=valid_user.password
        )
        invalid_id = list({1, 2, 3} ^ {valid_user.id})[0]
        url = reverse_lazy("users_delete", args=(invalid_id,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users_index"))
        updated_user = CustomUser.objects.get(username=valid_user.username)
        self.assertEqual(
            (updated_user.first_name, updated_user.last_name),
            (valid_user.first_name, valid_user.last_name),
        )
        print("All successfully failed.")


class TestUsersGetCRUDSs(TestCase, _TestUsersUtilsMixin):
    def setUp(self):
        self.subject = "Users app (get method)"
        self.client = Client()
        self._tests_to_success_tuple = (
            ("_test_users_index_get_success", valid_users),
        )
        self._tests_to_fail_tuple = []

    def _test_users_index_get_success(self, user):
        response = self.client.get(reverse_lazy("users_index"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, user["username"])
        self.assertNotContains(response, user["first_name"])
        self.assertNotContains(response, user["last_name"])
        self.create_user(user, force=True)
        print(
            "Test user registration page (GET) with user data ",
            user,
            end=" => ",
        )
        response = self.client.get(reverse_lazy("users_index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user["username"])
        self.assertContains(response, user["first_name"])
        self.assertContains(response, user["last_name"])
        print("succeeded.")
