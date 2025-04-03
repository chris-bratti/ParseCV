from argon2 import PasswordHasher
import os
from dotenv import load_dotenv

load_dotenv()

ph = PasswordHasher()

# Load in hashed password
hashed_password = ph.hash(os.getenv("API_KEY"))
