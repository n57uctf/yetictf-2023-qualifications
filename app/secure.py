import random
import string
import io
import pyAesCrypt
import hashlib
import jwt


def get_auth_token(login: str):
    in_file = open("./app/sp.txt", "r")
    kid = in_file.read()
    in_file.close()
    return jwt.encode({"login": login}, key=kid, algorithm="HS256",headers={"kid": "./app/sp.txt"})


def verify_auth_token(token: str):
    head = jwt.get_unverified_header(token)
    in_file = open(head['kid'], "r")
    kid = in_file.read()
    in_file.close()
    return jwt.decode(token, key=kid, algorithms=["HS256"], verify=False)["login"]


def hash_sha256(data: str):
    return hashlib.sha256(data.encode()).hexdigest()


def verify_hash(hash_string: str, data: str):
    return hashlib.sha256(data.encode()).hexdigest() == hash_string


def get_random_string(length=10):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


def encrypt_file_AES(file_data, passwd):
    bufferSize = 64 * 1024
    fIn = io.BytesIO(file_data)
    fCipher = io.BytesIO()
    pyAesCrypt.encryptStream(fIn,fCipher,passwd,bufferSize)
    return fCipher.getvalue()
    
    
def decrypt_file_AES(file_data, passwd):
    bufferSize = 64 * 1024
    fIn = io.BytesIO(file_data)
    fDeCipher = io.BytesIO()
    pyAesCrypt.decryptStream(fIn, fDeCipher, passwd, bufferSize, len(file_data))
    return fDeCipher.getvalue()
