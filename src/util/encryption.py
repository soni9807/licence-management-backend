from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
load_dotenv()
# Load the key from the environment variable
key = os.getenv('SECRET_KEY')
print("key", key)

# Check if the key is None or not in the correct format
if key is None:
    raise ValueError("SECRET_KEY is not set in the environment variables.")
    
# Ensure the key is in bytes format
try:
    cipher = Fernet(key.encode())  # Encode the key to bytes
except (TypeError, ValueError) as e:
    raise ValueError("Invalid SECRET_KEY format. Ensure it is a valid base64 URL-safe encoded string.") from e

def encrypt_data(data):
    """Encrypt data before saving to the database."""
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(data):
    """Decrypt data before exposing it via API."""
    return cipher.decrypt(data.encode()).decode()
