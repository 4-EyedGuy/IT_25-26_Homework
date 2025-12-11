import time
import hashlib
from passlib.hash import argon2

from user import User, UserStorage
from validation import validate_password


def register_user(storage: UserStorage, username: str, email: str, password: str) -> User:
    if User.exists(storage, username):
        raise ValueError("Пользователь с таким username уже существует")

    if not validate_password(password):
        raise ValueError("Пароль не соответствует требованиям")

    hashed = argon2.hash(password)

    user = User(
        username=username,
        email=email,
        password_hash=hashed,
        failed_attempts=0,
        backoff_seconds=0,
        last_failed_time=0
    )

    user.save(storage)
    return user


def verify_credentials(storage: UserStorage, username: str, password: str) -> bool:
    user = User.load(storage, username)
    if user is None:
        return False

    if user.backoff_seconds > 0:
        time.sleep(user.backoff_seconds)

    stored_hash = user.password_hash

    if _is_md5_hash(stored_hash):
        md5_hex = hashlib.md5(password.encode()).hexdigest()
        if md5_hex == stored_hash:
            new_hash = argon2.hash(password)
            user.password_hash = new_hash
            user.failed_attempts = 0
            user.backoff_seconds = 0
            user.last_failed_time = 0
            user.save(storage)
            return True
        else:
            return _register_failed_attempt(user, storage)

    try:
        ok = argon2.verify(password, stored_hash)
    except Exception:
        return _register_failed_attempt(user, storage)

    if ok:
        user.failed_attempts = 0
        user.backoff_seconds = 0
        user.last_failed_time = 0
        user.save(storage)
        return True

    return _register_failed_attempt(user, storage)


def _is_md5_hash(h: str) -> bool:
    return len(h) == 32 and all(c in "0123456789abcdef" for c in h.lower())


def _register_failed_attempt(user: User, storage: UserStorage) -> bool:
    user.failed_attempts += 1
    n = user.failed_attempts
    user.backoff_seconds = (1.5 ** n) + 1
    user.last_failed_time = time.time()

    user.save(storage)
    time.sleep(user.backoff_seconds)
    return False
