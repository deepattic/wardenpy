import secrets
import string

from libwardenpy.configuration import AppConfig

config = AppConfig()


### this create a password with default length 14 and has digis uppercase and lowecase letters
def generate_password(lenght: int = config.PASSWORD_LENGTH) -> str:
    alphabet = string.ascii_letters + string.digits
    while True:
        password = "".join(secrets.choice(alphabet) for _ in range(lenght))
        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and sum(c.isdigit() for c in password) >= 3
        ):
            break
    return password
