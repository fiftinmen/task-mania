urls_data = (
    {
        "viewname": "statuses_index",
    },
    {
        "viewname": "statuses_create",
    },
    {"viewname": "statuses_update", "kwargs": {"pk": "1"}},
    {"viewname": "statuses_delete", "kwargs": {"pk": "1"}},
)
default_status_fixture = {"id": 1, "name": "Default"}
# default status must be created in TestsStatuses.setUp;
valid_statuses = (
    # id 1 is reserved for default status
    {"pk": 2, "name": "Status"},
    {"pk": 3, "name": "On delay"},
    {"pk": 4, "name": "Stopped"},
    {"pk": 5, "name": "In work"},
    {"pk": 6, "name": "In test"},
    {"pk": 7, "name": "Preparing"},
)
non_existent_statuses = (
    {
        "pk": 101,
    },
    {
        "pk": 102,
    },
)
new_valid_statuses = (
    {"pk": 2, "name": "1Status"},
    {"pk": 3, "name": "1On delay"},
    {"pk": 4, "name": "1Stopped"},
    {"pk": 5, "name": "1In work"},
    {"pk": 6, "name": "1In test"},
    {"pk": 7, "name": "1Preparing"},
)
invalid_statuses = [
    {
        "name": """too long status name too long status name too long status
        name too long status name too long status""",
    }
]
user_fixture = {
    "username": "User",
    "first_name": "Us",
    "last_name": "Er",
    "password": "pass",
}
