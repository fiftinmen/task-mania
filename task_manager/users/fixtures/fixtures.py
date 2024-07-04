from ..models import CustomUser

VALID_USERNAMES = (
    "Alex",
    "Trentor",
    "Gaya",
    "Bliss",
    "GarrySeldon",
    "Academy",
    "Foundation",
    "1",
)
INVALID_USERNAMES = (
    "",
    "!drakula",
    ";somebody",
    "()",
    "*()!1" "Ya_ne^",
    """1111111111111111111111111111111111111111111111111111111111111111111
    1111111111111111111111111111111111111111111111111111111111111111111111
    111111111111111111111111111111111111111111111111111111111111111111""",
)
FIRST_NAMES = (
    "Alex",
    "Garry",
    "Harry",
    "Hermiona",
    "Ronald",
    "Donny",
    "Donald",
    "Sauron",
    "Saruman",
)
LAST_NAMES = (
    "Andreas",
    "Seldon",
    "Cooper",
    "Strange",
    "Potter",
    "Darko",
    "Duck",
    "Mayar",
    "White",
)
VALID_PASSWORDS = (
    "123",
    "231",
    "321",
    "333",
    "345",
    "355",
    "3566",
    "haHa",
    "SoManyLetters",
)
INVALID_PASSWORDS = ("1", "2", "aaa", "", "zz")


def user_factory(
    usernames=[], first_names=[], last_names=[], passwords1=[], passwords2=[]
):
    data = [
        usernames,
        first_names,
        last_names,
        passwords1,
        passwords2 if passwords2 else passwords1,
    ]
    length = min(map(len, data))
    users = []
    for i in range(length):
        user, created = CustomUser.objects.get_or_create(
            username=data[0][i],
            first_name=data[1][i],
            last_name=data[2][i],
            password=data[3][i],
        )
        users.append(user)
    return users


def valid_user_factory():
    return user_factory(
        usernames=VALID_USERNAMES,
        first_names=FIRST_NAMES,
        last_names=LAST_NAMES,
        passwords1=VALID_PASSWORDS,
    )


def invalid_user_factory():
    return user_factory(
        usernames=INVALID_USERNAMES,
        first_names=FIRST_NAMES,
        last_names=LAST_NAMES,
        passwords1=INVALID_PASSWORDS,
    )
