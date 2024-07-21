urls_data = (
    {
        "viewname": "tasks_index",
    },
    {
        "viewname": "tasks_create",
    },
    {"viewname": "tasks_update", "kwargs": {"pk": "1"}},
    {"viewname": "tasks_delete", "kwargs": {"pk": "1"}},
)
default_task_fixture = {"id": 1, "name": "Default_Task"}
default_status_fixture = {"id": 1, "name": "Default_Status"}

# default task must be created in TestsStatuses.setUp;
valid_tasks = (
    # id 1 is reserved for default task
    {"pk": 2, "name": "Do something"},
    {"pk": 3, "name": "Do something else"},
    {"pk": 4, "name": "Do nothing"},
    {"pk": 5, "name": "Do thing"},
    {"pk": 6, "name": "Do anything"},
    {"pk": 7, "name": "Do everything"},
)
new_valid_tasks = (
    {"pk": 2, "name": "1Do something"},
    {"pk": 3, "name": "1Do something else"},
    {"pk": 4, "name": "1Do nothing"},
    {"pk": 5, "name": "1Do thing"},
    {"pk": 6, "name": "1Do anything"},
    {"pk": 7, "name": "1Do everything"},
)
invalid_tasks = (
    {
        "name": """too long task name too long task name too long task
        name too long task name too long task too loong too long""",
    },
)
user_fixture1 = {
    "username": "User1",
    "first_name": "Us",
    "last_name": "Er",
    "password": "pass",
}
user_fixture2 = {
    "username": "User2",
    "first_name": "Usir",
    "last_name": "Erus",
    "password": "pass",
}
