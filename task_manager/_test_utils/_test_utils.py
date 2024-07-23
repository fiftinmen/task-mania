from task_manager.users.models import CustomUser


class _TestUtilsMixin:

    def _test(self, test_data):
        for test_name, data in test_data:
            test = getattr(self, test_name)
            [test(item) for item in data]

    def _tests_to_success(self, subject):
        print(f"\n\nStarting tests for {subject} to succeed.")
        self._test(self._tests_to_success_tuple)

    def _tests_to_fail(self, subject):
        print(f"\n\nStarting tests for {subject} to fail.")
        self._test(self._tests_to_fail_tuple)

    def tests_all(self):
        if getattr(self, "subject", None) is None:
            class_name = self.__class__
            print(
                f"Set self.subject in setUp method for {class_name}."
                " Temporarily using '{class_name}' as test subject."
            )
            subject = class_name
        else:
            subject = self.subject
        if getattr(self, "_tests_to_success_tuple", False):
            self._tests_to_success(subject or self.__class__)
        if getattr(self, "_tests_to_fail_tuple", False):
            self._tests_to_fail(subject or self.__class__)

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

    def create_user(self, user_data, force=False):
        if force:
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
