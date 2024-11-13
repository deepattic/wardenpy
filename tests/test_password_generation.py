import random
from libwardenpy.passgen import generate_password


def test_default_password_generation() -> None:
    default_password = generate_password()
    assert len(default_password) == 14


def test_password_generation_with_length() -> None:
    length = random.randint(1, 255)
    password = generate_password(length)
    assert len(password) == length
