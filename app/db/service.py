from werkzeug.security import generate_password_hash, check_password_hash


def password_hashing(password: str, salt_len: int=16):
    return generate_password_hash(
        password=password,
        salt_length=salt_len
        )
