from django.urls import reverse_lazy
from django.test import TestCase, Client
from .models import Label
from .fixtures.fixtures import (
    urls_data,
    valid_labels,
    new_valid_labels,
    invalid_labels,
    user_fixture,
    default_label_fixture,
    default_status_fixture,
)
from task_manager._test_utils._test_utils import _TestUtilsMixin
from task_manager.statuses.models import Status


class _TestLabelsUtilsMixin(_TestUtilsMixin):
    def delete_label(self, name):
        if name:
            if label := Label.objects.filter(name=name):
                label.delete()

    def delete_labels(self, labels=None):
        if labels is None:
            labels = ({"name": label.name} for label in Label.objects.all())
        [self.delete_label(label["name"]) for label in labels]

    def create_label(self, data, force=False):
        if force:
            self.delete_label(data["name"])
        label, _ = Label.objects.get_or_create(
            name=data["name"],
        )
        return label


class TestsLabels(TestCase, _TestLabelsUtilsMixin):
    def setUp(self):
        self.subject = "Labels app"
        self.client = Client()
        self._tests_to_success_tuple = (
            ("_test_labels_get_success", urls_data),
            ("_test_labels_create_post_success", valid_labels),
            ("_test_labels_update_post_success", new_valid_labels),
            ("_test_labels_delete_post_success", new_valid_labels),
        )
        self._tests_to_fail_tuple = (
            ("_test_labels_get_fail", urls_data),
            ("_test_labels_post_no_auth_fail", urls_data),
            ("_test_labels_create_post_fail", invalid_labels),
            ("_test_labels_update_post_fail", invalid_labels),
            (
                "_test_labels_delete_with_related_task_post_fail",
                valid_labels,
            ),
        )
        self.default_user = self.create_user(user_fixture)
        self.default_label = self.create_label(default_label_fixture)
        self.default_status, _ = Status.objects.get_or_create(
            name=default_status_fixture["name"]
        )

    def _test_labels_get_success(self, url_data: dict) -> None:
        self.client.force_login(self.default_user)
        response = self.client.get(reverse_lazy(**url_data))
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def _test_labels_create_post_success(self, label: dict) -> None:
        label = {"name": label["name"]}
        self.client.force_login(self.default_user)
        self.assertFalse(Label.objects.filter(name=label["name"]).exists())
        response = self.client.post(reverse_lazy("labels_create"), label)
        self.assertTrue(Label.objects.filter(name=label["name"]).exists())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("labels_index"))
        response = self.client.get(reverse_lazy("labels_index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, label["name"])
        self.client.logout()

    def _test_labels_update_post_success(self, new_label: dict) -> None:
        self.client.force_login(self.default_user)
        self.assertFalse(Label.objects.filter(name=new_label["name"]).exists())
        response = self.client.post(
            reverse_lazy("labels_update", args=[new_label["pk"]]),
            {"name": new_label["name"]},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name=new_label["name"]).exists())
        redirect_url = reverse_lazy("labels_index")
        self.assertRedirects(response, redirect_url)
        response = self.client.get(redirect_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, new_label["name"])
        self.client.logout()

    def _test_labels_delete_post_success(self, label: dict) -> None:
        self.client.force_login(self.default_user)
        self.assertTrue(Label.objects.filter(name=label["name"]).exists())
        response = self.client.post(
            reverse_lazy("labels_delete", args=[label["pk"]])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("labels_index"))
        self.assertFalse(Label.objects.filter(name=label["name"]).exists())
        response = self.client.get(reverse_lazy("labels_index"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, f'>{label["name"]}<')
        self.client.logout()

    def _test_labels_get_fail(self, url_data: dict) -> None:
        response = self.client.get(reverse_lazy(**url_data))
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse_lazy("users_login")
        self.assertRedirects(response, redirect_url)

    def _test_labels_post_no_auth_fail(self, url_data: dict) -> None:
        data = {"name": self.default_label.name}
        response = self.client.post(reverse_lazy(**url_data), data)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse_lazy("users_login")
        self.assertRedirects(response, redirect_url)

    def _test_labels_create_post_fail(self, invalid_label: dict) -> None:
        self.client.force_login(self.default_user)
        self.assertFalse(
            Label.objects.filter(name=invalid_label["name"]).exists()
        )
        response = self.client.post(
            reverse_lazy("labels_create"), invalid_label
        )
        self.assertFalse(
            Label.objects.filter(name=invalid_label["name"]).exists()
        )
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def _test_labels_update_post_fail(self, invalid_label: dict) -> None:
        self.client.force_login(self.default_user)
        self.assertTrue(
            Label.objects.filter(name=self.default_label.name).exists()
        )
        response = self.client.post(
            reverse_lazy("labels_update", args=(self.default_label.pk,)),
            invalid_label,
        )
        self.assertFalse(
            Label.objects.filter(name=invalid_label["name"]).exists()
        )
        self.assertTrue(
            Label.objects.filter(name=self.default_label.name).exists()
        )
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def _test_labels_delete_with_related_task_post_fail(self, data):
        user = self.default_user
        self.client.force_login(user)
        label = self.create_label(data)
        label.task_set.create(
            name=f'{data["name"]}_task', author=user, status=self.default_status
        )
        response = self.client.post(
            reverse_lazy("labels_delete", args=(label.pk,))
        )
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse_lazy("labels_index")
        self.assertRedirects(response, redirect_url)
        self.client.logout()
