from django.urls import reverse_lazy
from django.test import TestCase, Client
from .models import Status
from .fixtures.fixtures import (
    urls_data,
    valid_statuses,
    new_valid_statuses,
    invalid_statuses,
    user_fixture,
    default_status_fixture,
)
from task_manager._test_utils._test_utils import _TestUtilsMixin


class _TestStatusesUtilsMixin(_TestUtilsMixin):
    def delete_status(self, name):
        if name:
            if status := Status.objects.filter(name=name):
                status.delete()

    def delete_statuses(self, statuses=[]):
        if not statuses:
            statuses = (
                {"name": status.name} for status in Status.objects.all()
            )
        [self.delete_status(status["name"]) for status in statuses]

    def create_status(self, data, force=False):
        if force:
            self.delete_status(data["name"])
        status, _ = Status.objects.get_or_create(
            name=data["name"],
        )
        return status


class TestsStatuses(TestCase, _TestStatusesUtilsMixin):
    def setUp(self):
        self.subject = "Statuses app"
        self.client = Client()
        self._tests_to_success_tuple = (
            ("_test_statuses_get_success", urls_data),
            ("_test_statuses_create_post_success", valid_statuses),
            ("_test_statuses_update_post_success", new_valid_statuses),
            ("_test_statuses_delete_post_success", new_valid_statuses),
        )
        self._tests_to_fail_tuple = (
            ("_test_statuses_get_fail", urls_data),
            ("_test_statuses_post_no_auth_fail", urls_data),
            ("_test_statuses_create_post_fail", invalid_statuses),
            ("_test_statuses_update_post_fail", invalid_statuses),
        )
        self.default_user = self.create_user(user_fixture)
        self.default_status = self.create_status(default_status_fixture)

    def _test_statuses_get_success(self, url_data: dict) -> None:
        user = self.default_user
        self.client.force_login(user)
        response = self.client.get(reverse_lazy(**url_data))
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def _test_statuses_create_post_success(self, status: dict) -> None:
        user = self.default_user
        status = {"name": status["name"]}
        self.client.force_login(user)
        self.assertFalse(Status.objects.filter(name=status["name"]).exists())
        response = self.client.post(reverse_lazy("statuses_create"), status)
        self.assertTrue(Status.objects.filter(name=status["name"]).exists())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("statuses_index"))
        response = self.client.get(reverse_lazy("statuses_index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, status["name"])
        self.client.logout()

    def _test_statuses_update_post_success(self, new_status: dict) -> None:
        user = self.default_user
        self.client.force_login(user)
        self.assertFalse(
            Status.objects.filter(name=new_status["name"]).exists()
        )
        response = self.client.post(
            reverse_lazy("statuses_update", args=[new_status["pk"]]),
            {"name": new_status["name"]},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name=new_status["name"]).exists())
        redirect_url = reverse_lazy("statuses_index")
        self.assertRedirects(response, redirect_url)
        response = self.client.get(redirect_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, new_status["name"])
        self.client.logout()

    def _test_statuses_delete_post_success(self, status: dict) -> None:
        user = self.default_user
        self.client.force_login(user)
        self.assertTrue(Status.objects.filter(name=status["name"]).exists())
        response = self.client.post(
            reverse_lazy("statuses_delete", args=[status["pk"]])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("statuses_index"))
        self.assertFalse(Status.objects.filter(name=status["name"]).exists())
        response = self.client.get(reverse_lazy("statuses_index"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, status["name"])
        self.client.logout()

    def _test_statuses_get_fail(self, url_data: dict) -> None:
        response = self.client.get(reverse_lazy(**url_data))
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse_lazy("users_login")
        self.assertRedirects(response, redirect_url)

    def _test_statuses_post_no_auth_fail(self, url_data: dict) -> None:
        data = {"name": self.default_status.name}
        response = self.client.post(reverse_lazy(**url_data), data)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse_lazy("users_login")
        self.assertRedirects(response, redirect_url)

    def _test_statuses_create_post_fail(self, invalid_status: dict) -> None:
        user = self.default_user
        self.client.force_login(user)
        self.assertFalse(
            Status.objects.filter(name=invalid_status["name"]).exists()
        )
        response = self.client.post(
            reverse_lazy("statuses_create"), invalid_status
        )
        self.assertFalse(
            Status.objects.filter(name=invalid_status["name"]).exists()
        )
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def _test_statuses_update_post_fail(self, invalid_status: dict) -> None:
        user = self.default_user
        self.client.force_login(user)
        self.assertTrue(
            Status.objects.filter(name=self.default_status.name).exists()
        )
        response = self.client.post(
            reverse_lazy("statuses_update", args=(self.default_status.pk,)),
            invalid_status,
        )
        self.assertFalse(
            Status.objects.filter(name=invalid_status["name"]).exists()
        )
        self.assertTrue(
            Status.objects.filter(name=self.default_status.name).exists()
        )
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def _test_statuses_delete_with_related_task_post_fail(self, status):
        user = self.default_user
        self.client.force_login(user)
        status = self.create_status(status["name"])
        status.task_set.create(f'{status["name"]}_task')
        response = self.client.post(
            reverse_lazy("statuses_delete", args=(status.pk,))
        )
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse_lazy("users_login")
        self.assertRedirects(response, redirect_url)
        self.client.logout()
