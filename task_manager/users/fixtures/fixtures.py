from ..models import CustomUser

valid_users = (
    {
        "id": 1,
        "username": "Alex",
        "password1": "123",
        "password2": "123",
        "first_name": "Alex",
        "last_name": "Andreas",
    },
    {
        "id": 2,
        "username": "HarryPotter",
        "password1": "3312",
        "password2": "3312",
        "first_name": "Harry",
        "last_name": "Potter",
    },
    {
        "id": 3,
        "username": "Max1",
        "password1": "mmaxxx2_1",
        "password2": "mmaxxx2_1",
        "first_name": "Max",
        "last_name": "Smart",
    },
)
invalid_users = (
    {
        "id": 1,
        "username": "!drakula",
        "password1": "333",
        "password2": "333",
        "first_name": "Harry",
        "last_name": "Potter",
    },
    {
        "id": 2,
        "username": """111111111111111111111111111111111111111111111111111
        111111111111111111111111111111111111111111111111111111111111111111
        111111111111111111111111111111111111111111111111111111111111111111
        11111111111111111111111111111111111111111111111111111111111111""",
        "password1": "333",
        "password2": "333",
        "first_name": "Harry",
        "last_name": "Potter",
    },
    {
        "id": 3,
        "username": "",
        "password1": "333",
        "password2": "333",
        "first_name": "Harry",
        "last_name": "Potter",
    },
    {
        "id": 4,
        "username": "aaa",
        "password1": "33",
        "password2": "33",
        "first_name": "Harry",
        "last_name": "Potter",
    },
    {
        "id": 5,
        "username": "aaa",
        "password1": "33",
        "password2": "333",
        "first_name": "Harry",
        "last_name": "Potter",
    },
    {
        "id": 6,
        "username": "aaa",
        "password1": "333",
        "password2": "33",
        "first_name": "Harry",
        "last_name": "Potter",
    },
    {
        "id": 7,
        "username": "aaa",
        "password1": "333",
        "password2": "3333",
        "first_name": "Harry",
        "last_name": "Potter",
    },
    {
        "id": 8,
        "username": "aaa",
        "password1": "3333",
        "password2": "333",
        "first_name": "Harry",
        "last_name": "Potter",
    },
)


def make_user(user_data):
    if not isinstance(user_data, AnonymousUser):
        user = CustomUser.objects.get_or_create(
            username=user_data["username"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            password=user_data["password1"],
        )
        return user
    return user_data
