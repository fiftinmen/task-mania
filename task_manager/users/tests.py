from django.urls import reverse_lazy
from django.test import TestCase, Client
from .models import CustomUser
from .fixtures.fixtures import valid_users, invalid_users


# Create your tests here.
class TestUserCRUDs(TestCase):
    def setUp(self):
        self.client = Client()
        self.tests_to_success = (
            ("_test_users_create_post_success", valid_users),
            ("_test_users_update_post_success", valid_users),
            ("_test_users_delete_post_success", valid_users),
        )
        self.tests_to_fail = (
            ("_test_users_create_post_fail", invalid_users),
            (
                "_test_users_update_post_fail",
                tuple(zip(valid_users * 3, invalid_users)),
            ),
            ("_test_users_delete_post_fail", valid_users),
        )

    def delete_user(self, username):
        if username:
            if user := CustomUser.objects.filter(username=username):
                user.delete()

    def delete_users(self, users):
        [self.delete_user(user["username"]) for user in users]

    def make_user(self, user_data):
        user = CustomUser.objects.get_or_create(
            username=user_data["username"],
            password=user_data["password1"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
        )
        return user

    def _test_users(self, test_data):
        for test_name, data in test_data:
            test = getattr(self, test_name)
            [test(user) for user in data]

    def test_users_to_success(self):
        print("Starting tests for users post views to succeed.")
        self._test_users(self.tests_to_success)
        print("")

    def test_users_to_fail(self):
        print("Starting tests for users post views to fail.")
        self._test_users(self.tests_to_fail)
        print("")

    def _test_users_create_post_success(self, user):
        data = {
            "username": user["username"],
            "password1": user["password1"],
            "password2": user["password1"],
        }
        print("Test create user with data: ", data, end=" => ")
        self.client.login(username=user["username"], password=user["password1"])
        self.assertFalse(
            CustomUser.objects.filter(username=user["username"]).exists()
        )
        response = self.client.post(reverse_lazy("users_create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            CustomUser.objects.filter(username=user["username"]).exists()
        )
        print("succeeded.")

    def _test_users_update_post_success(self, user):
        data = {
            "username": user["username"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "new_password1": user["password1"],
            "new_password2": user["password2"],
        }
        print("Test update user with data: ", data, end=" => ")
        self.client.login(username=user["username"], password=user["password1"])
        url = reverse_lazy("users_update", args=(user["id"],))
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        updated_user = CustomUser.objects.get(username=user["username"])
        self.assertEqual(
            (updated_user.first_name, updated_user.last_name),
            (user["first_name"], user["last_name"]),
        )
        print("succeeded.")

    def _test_users_delete_post_success(self, user):
        id = user["id"]
        print("Test delete user with id: ", id, end=" => ")
        self.client.login(username=user["username"], password=user["password1"])
        url = reverse_lazy("users_delete", args=(id,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
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
        self.client.login(username=user["username"], password=user["password1"])
        self.assertFalse(
            CustomUser.objects.filter(username=user["username"]).exists()
        )
        response = self.client.post(reverse_lazy("users_create"), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            CustomUser.objects.filter(username=user["username"]).exists()
        )
        print("successfully failed.")

    def _test_users_update_post_fail(self, data):
        valid_user_data = data[0]
        valid_user, _ = self.make_user(valid_user_data)
        invalid_user_data = data[1]
        test_data = {
            "username": invalid_user_data["username"],
            "first_name": invalid_user_data["first_name"],
            "last_name": invalid_user_data["last_name"],
            "new_password1": invalid_user_data["password1"],
            "new_password2": invalid_user_data["password1"],
        }
        print("Test update user with broken data: ", test_data, end=" => ")

        # test updating data without authentication
        url = reverse_lazy("users_update", args=(valid_user.id,))
        response = self.client.post(url, test_data)
        self.assertEqual(response.status_code, 302)
        updated_user = CustomUser.objects.get(username=valid_user.username)
        self.assertEqual(
            (updated_user.first_name, updated_user.last_name),
            (valid_user.first_name, valid_user.last_name),
        )

        # test updating data with bad data
        self.client.login(
            username=valid_user.username, password=valid_user.password
        )
        url = reverse_lazy("users_update", args=(valid_user.id,))
        response = self.client.post(url, test_data)
        self.assertEqual(response.status_code, 302)
        updated_user = CustomUser.objects.get(username=valid_user.username)
        self.assertEqual(
            (updated_user.first_name, updated_user.last_name),
            (valid_user.first_name, valid_user.last_name),
        )

        # test updating other user's data
        self.client.login(
            username=valid_user.username, password=valid_user.password
        )
        invalid_id = list({1, 2, 3} ^ {valid_user.id})[0]
        url = reverse_lazy("users_update", args=(invalid_id,))
        response = self.client.post(url, test_data)
        self.assertEqual(response.status_code, 302)
        updated_user = CustomUser.objects.get(username=valid_user.username)
        self.assertEqual(
            (updated_user.first_name, updated_user.last_name),
            (valid_user.first_name, valid_user.last_name),
        )
        print("successfully failed.")

    def _test_users_delete_post_fail(self, user_data):
        valid_user, _ = self.make_user(user_data)

        print("Test delete user: ", user_data, end=" => ")

        # test updating data without authentication
        url = reverse_lazy("users_delete", args=(valid_user.id,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        updated_user = CustomUser.objects.get(username=valid_user.username)
        self.assertEqual(
            (updated_user.first_name, updated_user.last_name),
            (valid_user.first_name, valid_user.last_name),
        )

        # test updating data with bad data
        self.client.login(
            username=valid_user.username, password=valid_user.password
        )
        url = reverse_lazy("users_delete", args=(valid_user.id,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        updated_user = CustomUser.objects.get(username=valid_user.username)
        self.assertEqual(
            (updated_user.first_name, updated_user.last_name),
            (valid_user.first_name, valid_user.last_name),
        )

        # test updating other user's data
        self.client.login(
            username=valid_user.username, password=valid_user.password
        )
        invalid_id = list({1, 2, 3} ^ {valid_user.id})[0]
        url = reverse_lazy("users_delete", args=(invalid_id,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        updated_user = CustomUser.objects.get(username=valid_user.username)
        self.assertEqual(
            (updated_user.first_name, updated_user.last_name),
            (valid_user.first_name, valid_user.last_name),
        )
        print("successfully failed.")
