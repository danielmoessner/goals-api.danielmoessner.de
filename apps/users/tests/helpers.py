from apps._users.models import User


def create_user(
    email="dummy@abc.de",
    first_name="Awesome",
    last_name="Dummy",
    password="pass1234!",
    save=False,
) -> User:
    user = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    user.set_password(password)
    if save:
        user.save()
    return user
