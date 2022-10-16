import random
import string
import hashlib

import jwt


def get_auth_token(login: str):
    return jwt.encode({"login": login}, "2J*z583j&7tXF61z", algorithm="HS256")


def verify_auth_token(token: str):
    return jwt.decode(token, "2J*z583j&7tXF61z", algorithms=["HS256"])["login"]


def hash_sha256(data: str):
    return hashlib.sha256(data.encode()).hexdigest()


def verify_hash(hash_string: str, data: str):
    return hashlib.sha256(data.encode()).hexdigest() == hash_string


def get_random_string(length=10):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))
