import os

from argon2 import PasswordHasher
from dotenv import load_dotenv

load_dotenv()

ph = PasswordHasher()

# Load in hashed apiKey
hashed_password = ph.hash(os.getenv("API_KEY"))
