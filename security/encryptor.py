from cryptography.fernet import Fernet
import os

KEY_PATH = "secret.key"
if not os.path.exists(KEY_PATH):
    with open(KEY_PATH, "wb") as key_file:
        key_file.write(Fernet.generate_key())

with open(KEY_PATH, "rb") as key_file:
    key = key_file.read()
fernet = Fernet(key)

def encrypt_file(filepath):
    with open(filepath, "rb") as file:
        encrypted = fernet.encrypt(file.read())
    with open(filepath, "wb") as file:
        file.write(encrypted)

def decrypt_file(filepath):
    with open(filepath, "rb") as file:
        decrypted = fernet.decrypt(file.read())
    with open(filepath, "wb") as file:
        file.write(decrypted)
