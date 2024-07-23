valid_users = (
    {
        "pk": 1,
        "username": "Alex",
        "password1": "123",
        "password2": "123",
        "first_name": "Alex",
        "last_name": "Andreas",
    },
    {
        "pk": 2,
        "username": "HarryPotter",
        "password1": "3312",
        "password2": "3312",
        "first_name": "Harry",
        "last_name": "Potter",
    },
    {
        "pk": 3,
        "username": "Max1",
        "password1": "mmaxxx2_1",
        "password2": "mmaxxx2_1",
        "first_name": "Max",
        "last_name": "Smart",
    },
)

# extend list of valid users to use it with invalid_users in some tests
extended_valid_users = valid_users * 4


invalid_users = (
    {
        "pk": 1,
        "username": "!drakula",
        "new_password1": "333",
        "new_password2": "333",
        "first_name": "Harry",
        "last_name": "Potter",
    },
    {
        "pk": 2,
        "username": """111111111111111111111111111111111111111111111111111
        111111111111111111111111111111111111111111111111111111111111111111
        111111111111111111111111111111111111111111111111111111111111111111
        11111111111111111111111111111111111111111111111111111111111111""",
        "new_password1": "333",
        "new_password2": "333",
        "first_name": "Harry",
        "last_name": "Potter",
    },
    {
        "pk": 3,
        "username": "",
        "new_password1": "333",
        "new_password2": "333",
        "first_name": "Harry",
        "last_name": "Potter",
    },
    {
        "pk": 4,
        "username": "aaa",
        "new_password1": "33",
        "new_password2": "33",
        "first_name": "Harry",
        "last_name": "Potter",
    },
    {
        "pk": 5,
        "username": "aaa",
        "new_password1": "33",
        "new_password2": "333",
        "first_name": "Harry",
        "last_name": "Potter",
    },
    {
        "pk": 6,
        "username": "aaa",
        "new_password1": "333",
        "new_password2": "33",
        "first_name": "Harry",
        "last_name": "Potter",
    },
    {
        "pk": 7,
        "username": "aaa",
        "new_password1": "333",
        "new_password2": "3333",
        "first_name": "Harry",
        "last_name": "Potter",
    },
    {
        "pk": 8,
        "username": "aaa",
        "new_password1": "3333",
        "new_password2": "333",
        "first_name": "Harry",
        "last_name": "Potter",
    },
    {
        "pk": 9,
        "username": "aaa",
        "new_password1": "3333",
        "new_password2": "333",
        "first_name": "Harry",
        "last_name": "",
    },
    {
        "pk": 10,
        "username": "aaa",
        "new_password1": "3333",
        "new_password2": "333",
        "first_name": "",
        "last_name": "Potter",
    },
    {
        "pk": 11,
        "username": "aaa",
        "new_password1": "3333",
        "new_password2": "333",
        "first_name": "",
        "last_name": "",
    },
)

other_user_data = {
    "username": "Autobot",
    "first_name": "Prime",
    "last_name": "Optimus",
    "password1": "password",
    "password2": "password",
}
