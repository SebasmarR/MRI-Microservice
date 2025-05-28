import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()
fernet = Fernet(os.getenv("FERNET_KEY"))

def encrypt(text: str) -> str:
    return fernet.encrypt(text.encode()).decode()

def decrypt(cipher_text: str) -> str:
    return fernet.decrypt(cipher_text.encode()).decode()
