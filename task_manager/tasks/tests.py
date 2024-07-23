from django.test import TestCase, Client
from task_manager._test_utils._test_utils import _TestUtilsMixin
from django.urls import reverse_lazy
from .models import Task
from task_manager.statuses.models import Status
from task_manager.users.models import CustomUser

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

HEADER_ROWS_NUMBER = 1


class _TestTasksUtilsMixin(_TestUtilsMixin):

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
        if data.get("author") is None:
            data["author"] = self.default_user1
        if data.get("status") is None:
            data["status"] = self.default_status
        task, _ = self.default_user1.task_author.get_or_create(**data)
        return task


class TestTasksFilters(TestCase, _TestUtilsMixin):
    fixtures = ("fixtures.json.gz",)

    def setUp(self):
        self.users = CustomUser.objects.all()
        self.current_user = self.users[0]
        self.current_user_tasks = self.current_user.task_author
        self.client = Client()
        self._tests_to_success_tuple = (
            ("_test_tasks_filter_by_own_tasks", (None,)),
            ("_test_tasks_filter_by_executor", self.users),
        )

    def _test_tasks_filter_by_own_tasks(self, *arg):
        self.client.force_login(self.current_user)
        url = reverse_lazy("tasks_index")
        data = {"only_own_tasks": True}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f"{self.current_user.username}",
        )
        self.assertTrue(
            response,
            all(
                self.assertContains(response, task.name)
                for task in self.current_user_tasks.all()
            ),
        )
        expected_rows_number = (
            self.current_user_tasks.all().count() + HEADER_ROWS_NUMBER
        )
        self.assertContains(response, "<tr", expected_rows_number)

    def _test_tasks_filter_by_executor(self, executor):
        self.client.force_login(self.current_user)
        tasks = executor.task_executor
        url = reverse_lazy("tasks_index")
        data = {"executor": executor.pk}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f"{executor.username}",
        )
        self.assertTrue(
            response,
            all(
                self.assertContains(response, task.name) for task in tasks.all()
            ),
        )
        expected_rows_number = tasks.all().count() + HEADER_ROWS_NUMBER
        self.assertContains(response, "<tr", expected_rows_number)


class TestsTasks(
    _TestTasksUtilsMixin,
    TestCase,
):
    def setUp(self):
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
            ("_test_tasks_delete_not_own_task_post_fail", valid_tasks),
        )
        self.default_user1 = self.create_user(user_fixture1)
        self.default_user2 = self.create_user(user_fixture2)
        self.default_status = Status.objects.create(
            name=default_status_fixture["name"]
        )
        self.default_task = self.get_or_create_task(default_task_fixture)

    def _test_tasks_get_success(self, url_data: dict) -> None:
        self.client.force_login(self.default_user1)
        response = self.client.get(reverse_lazy(**url_data))
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def _test_tasks_create_post_success(self, task: dict) -> None:
        user = self.default_user1
        task = {"name": task["name"], "status": self.default_status.pk}
        self.client.force_login(user)
        self.assertFalse(Task.objects.filter(name=task["name"]).exists())
        response = self.client.post(reverse_lazy("tasks_create"), task)
        self.assertTrue(Task.objects.filter(name=task["name"]).exists())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("tasks_index"))
        response = self.client.get(reverse_lazy("tasks_index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, task["name"])
        self.client.logout()

    def _test_tasks_update_post_success(self, new_task: dict) -> None:
        self.client.force_login(self.default_user1)
        self.assertFalse(Task.objects.filter(name=new_task["name"]).exists())
        response = self.client.post(
            reverse_lazy("tasks_update", args=[new_task["pk"]]),
            {
                "name": new_task["name"],
                "status": self.default_status.pk,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name=new_task["name"]).exists())
        redirect_url = reverse_lazy("tasks_index")
        self.assertRedirects(response, redirect_url)
        response = self.client.get(redirect_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, new_task["name"])
        self.client.logout()

    def _test_tasks_delete_post_success(self, task: dict) -> None:
        self.client.force_login(self.default_user1)
        self.assertTrue(Task.objects.filter(name=task["name"]).exists())
        response = self.client.post(
            reverse_lazy("tasks_delete", args=[task["pk"]])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("tasks_index"))
        self.assertFalse(Task.objects.filter(name=task["name"]).exists())
        self.client.logout()

    def _test_tasks_get_fail(self, url_data: dict) -> None:
        response = self.client.get(reverse_lazy(**url_data))
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse_lazy("users_login")
        self.assertRedirects(response, redirect_url)

    def _test_tasks_post_no_auth_fail(self, url_data: dict) -> None:
        data = {"name": self.default_task.name}
        response = self.client.post(reverse_lazy(**url_data), data)
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse_lazy("users_login")
        self.assertRedirects(response, redirect_url)

    def _test_tasks_create_post_fail(self, invalid_task: dict) -> None:
        self.client.force_login(self.default_user1)
        data = {"name": invalid_task["name"]}
        self.assertFalse(Task.objects.filter(name=data["name"]).exists())
        response = self.client.post(reverse_lazy("tasks_create"), data)
        self.assertFalse(Task.objects.filter(name=data["name"]).exists())
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def _test_tasks_update_post_fail(self, invalid_task: dict) -> None:
        self.client.force_login(self.default_user1)
        data = {"name": invalid_task["name"]}
        self.assertTrue(
            Task.objects.filter(name=default_task_fixture["name"]).exists()
        )
        response = self.client.post(
            reverse_lazy("tasks_update", args=(self.default_task.pk,)), data
        )
        self.assertFalse(Task.objects.filter(name=data["name"]).exists())
        self.assertTrue(
            Task.objects.filter(name=default_task_fixture["name"]).exists()
        )
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def _test_tasks_delete_not_own_task_post_fail(self, task_data):
        task = self.get_or_create_task(task_data)
        self.client.force_login(self.default_user2)
        response = self.client.post(
            reverse_lazy("tasks_delete", args=(task.pk,))
        )
        self.assertEqual(response.status_code, 302)
        redirect_url = reverse_lazy("tasks_index")
        self.assertRedirects(response, redirect_url)
        self.assertTrue(Task.objects.filter(name=task_data["name"]).exists())
        self.client.logout()
