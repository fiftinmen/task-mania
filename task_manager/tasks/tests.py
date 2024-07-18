from django.db.models import Model
from django.test import TestCase, Client
from django.urls import reverse_lazy
from .models import Task
from .fixtures.fixtures import (
    urls_data,
    valid_tasks,
    new_valid_tasks,
    invalid_tasks,
    user_fixture1,
    user_fixture2,
    default_task_fixture,
    default_status_fixture,
)
from task_manager._test_utils._test_utils import _TestUtilsMixin
from task_manager.statuses.models import Status
from task_manager.users.models import CustomUser


class _TestTasksUtilsMixin(_TestUtilsMixin):
    model = None

    def delete_task(self, name):
        if name:
            if task := Task.objects.filter(name=name):
                task.delete()

    def delete_tasks(self, tasks: list | tuple = None):
        if tasks is None:
            tasks = ({"name": task.name} for task in Task.objects.all())
        [self.delete_task(task["name"]) for task in tasks]

    def get_or_create_task(self, data, force_recreate=False):
        if force_recreate:
            self.delete_task(data["name"])
        task, _ = self.default_user1.task_author.get_or_create(
            name=data["name"], status=self.default_status
        )
        return task


class TestsTasks(TestCase, _TestTasksUtilsMixin):
    def setUp(self):
        self.assertContains()
        self.subject = "tasks app"
        self.client = Client()
        self._tests_to_success_tuple = (
            ("_test_tasks_get_success", urls_data),
            ("_test_tasks_create_post_success", valid_tasks),
            ("_test_tasks_update_post_success", new_valid_tasks),
            ("_test_tasks_delete_post_success", new_valid_tasks),
        )
        self._tests_to_fail_tuple = (
            ("_test_tasks_get_fail", urls_data),
            ("_test_tasks_post_no_auth_fail", urls_data),
            ("_test_tasks_create_post_fail", invalid_tasks),
            ("_test_tasks_update_post_fail", invalid_tasks),
        )
        self.default_user1 = self.create_user(user_fixture1)
        self.default_user2 = self.create_user(user_fixture2)
        self.default_task = self.get_or_create_task(default_task_fixture)
        self.default_status = Status.objects.create(default_status_fixture)

    def _test_tasks_get_success(self, url_data: dict) -> None:
        user = self.default_user1
        self.client.force_login(user)
        response = self.client.get(reverse_lazy(**url_data))
        self.assertEqual(response.task_code, 200)
        self.client.logout()

    def _test_tasks_create_post_success(self, task: dict) -> None:
        user = self.default_user1
        task = {"name": task["name"]}
        self.client.force_login(user)
        self.assertFalse(Task.objects.filter(name=task["name"]).exists())
        response = self.client.post(reverse_lazy("tasks_create"), task)
        self.assertTrue(Task.objects.filter(name=task["name"]).exists())
        self.assertEqual(response.task_code, 302)
        self.assertRedirects(response, reverse_lazy("tasks_index"))
        response = self.client.get(reverse_lazy("tasks_index"))
        self.assertEqual(response.task_code, 200)
        self.assertContains(response, task["name"])
        self.client.logout()

    def _test_tasks_update_post_success(self, new_task: dict) -> None:
        user = self.default_user1
        self.client.force_login(user)
        self.assertFalse(Task.objects.filter(name=new_task["name"]).exists())
        response = self.client.post(
            reverse_lazy("tasks_update", args=[new_task["pk"]]),
            {"name": new_task["name"]},
        )
        self.assertEqual(response.task_code, 302)
        self.assertTrue(Task.objects.filter(name=new_task["name"]).exists())
        redirect_url = reverse_lazy("tasks_index")
        self.assertRedirects(response, redirect_url)
        response = self.client.get(redirect_url)
        self.assertEqual(response.task_code, 200)
        self.assertContains(response, new_task["name"])
        self.client.logout()

    def _test_tasks_delete_post_success(self, task: dict) -> None:
        user = self.default_user1
        self.client.force_login(user)
        self.assertTrue(Task.objects.filter(name=task["name"]).exists())
        response = self.client.post(
            reverse_lazy("tasks_delete", args=[task["pk"]])
        )
        self.assertEqual(response.task_code, 302)
        self.assertRedirects(response, reverse_lazy("tasks_index"))
        self.assertFalse(Task.objects.filter(name=task["name"]).exists())
        response = self.client.get(reverse_lazy("tasks_index"))
        self.assertEqual(response.task_code, 200)
        self.assertNotContains(response, task["name"])
        self.client.logout()

    def _test_tasks_get_fail(self, url_data: dict) -> None:
        response = self.client.get(reverse_lazy(**url_data))
        self.assertEqual(response.task_code, 302)
        redirect_url = reverse_lazy("users_login")
        self.assertRedirects(response, redirect_url)

    def _test_tasks_post_no_auth_fail(self, url_data: dict) -> None:
        data = {"name": self.default_task["name"]}
        response = self.client.post(reverse_lazy(**url_data), data)
        self.assertEqual(response.task_code, 302)
        redirect_url = reverse_lazy("users_login")
        self.assertRedirects(response, redirect_url)

    def _test_tasks_create_post_fail(self, invalid_task: dict) -> None:
        user = self.default_user1
        self.client.force_login(user)
        data = {"name": invalid_task["name"]}
        self.assertFalse(Task.objects.filter(name=data["name"]).exists())
        response = self.client.post(reverse_lazy("tasks_create"), data)
        self.assertFalse(Task.objects.filter(name=data["name"]).exists())
        self.assertEqual(response.task_code, 302)
        redirect_url = reverse_lazy("users_login")
        self.assertRedirects(response, redirect_url)
        self.client.logout()

    def _test_tasks_update_post_fail(self, invalid_task: dict) -> None:
        user = self.default_user1
        self.client.force_login(user)
        data = {"name": invalid_task["name"]}
        self.assertTrue(
            Task.objects.filter(name=self.default_task["pk"]).exists()
        )
        response = self.client.post(
            reverse_lazy("tasks_delete", pk=self.default_task["pk"]), data
        )
        self.assertFalse(Task.objects.filter(name=data["name"]).exists())
        self.assertTrue(
            Task.objects.filter(name=self.default_task["name"]).exists()
        )
        self.assertEqual(response.task_code, 302)
        redirect_url = reverse_lazy("users_login")
        self.assertRedirects(response, redirect_url)
        self.client.logout()

    def _test_tasks_delete_with_related_task_post_fail(self, task):
        user = self.default_user1
        self.client.force_login(user)
        task = self.get_or_create_task(task["name"])
        task.task_set.create(f'{task["name"]}_task')
        response = self.client.post(reverse_lazy("tasks_delete", pk=task.pk))
        self.assertEqual(response.task_code, 302)
        redirect_url = reverse_lazy("users_login")
        self.assertRedirects(response, redirect_url)
        self.client.logout()
