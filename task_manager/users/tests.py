from django.urls import reverse_lazy
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from .models import CustomUser
from . import views
from .fixtures import fixtures
import pytest


# Create your tests here.
class TestUserCRUDs(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.tests = ("test_index",)

    def tests_parametrize(self):
        for test in self.tests:
            users = [
                *fixtures.valid_user_factory(),
                *fixtures.invalid_user_factory(),
                AnonymousUser(),
            ]
            test = getattr(self, test)
            for user in users:
                test(user)

    def test_index(self, user=None):
        if user is None:
            return
        request = self.factory.get(reverse_lazy("users_index"))
        request.user = user
        response = views.UsersIndexView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        if not isinstance(user, AnonymousUser):
            self.assertContains(response, f"{user.first_name} {user.last_name}")
