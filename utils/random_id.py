import secrets, string

ALPHABET = string.ascii_letters + string.digits
def generate_random_id(length=10):
    return ''.join(secrets.choice(ALPHABET) for _ in range(length))
