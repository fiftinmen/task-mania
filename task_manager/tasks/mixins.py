from task_manager.users.mixins import NotOwnObjectPermissionMixin


class TasksModifyPermissionMixin(NotOwnObjectPermissionMixin):

    next_page = "tasks_index"
    owner_field = "author"
