urls_data = (
    {
        "viewname": "labels_index",
    },
    {
        "viewname": "labels_create",
    },
    {"viewname": "labels_update", "kwargs": {"pk": "1"}},
    {"viewname": "labels_delete", "kwargs": {"pk": "1"}},
)
default_label_fixture = {"id": 1, "name": "Default_Task"}
default_label_fixture = {"id": 1, "name": "Default_Label"}

# default label must be created in TestsLabels.setUp;
valid_labels = (
    # id 1 is reserved for default label
    {"pk": 2, "name": "Do something"},
    {"pk": 3, "name": "Do something else"},
    {"pk": 4, "name": "Do nothing"},
    {"pk": 5, "name": "Do thing"},
    {"pk": 6, "name": "Do anything"},
    {"pk": 7, "name": "Do everything"},
)
new_valid_labels = (
    {"pk": 2, "name": "1Do something"},
    {"pk": 3, "name": "1Do something else"},
    {"pk": 4, "name": "1Do nothing"},
    {"pk": 5, "name": "1Do thing"},
    {"pk": 6, "name": "1Do anything"},
    {"pk": 7, "name": "1Do everything"},
)
invalid_labels = (
    {
        "name": """too long label name too long label name too long label
        name too long label name too long label too loong too long""",
    },
)
user_fixture = {
    "username": "User1",
    "first_name": "Us",
    "last_name": "Er",
    "password": "pass",
}
default_status_fixture = {"id": 1, "name": "Default"}
