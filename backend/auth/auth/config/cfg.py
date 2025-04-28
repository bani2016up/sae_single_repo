from dotenv import load_dotenv
from os import getenv


load_dotenv()


SUPABASE_URL = getenv("SUPABASE_URL")
if not SUPABASE_URL:
    raise ValueError("SUPABASE_URL is not set in the .env file")

SUPABASE_KEY = getenv("SUPABASE_KEY")
if not SUPABASE_KEY:
    raise ValueError("SUPABASE_KEY is not set in the .env file")

JWT_ALGORITHM = getenv("JWT_ALGORITHM")
if not JWT_ALGORITHM:
    raise ValueError("JWT_ALGORITHM is not set in the .env file")

JWT_SECRET = getenv("JWT_SECRET")
if not JWT_SECRET:
    raise ValueError("JWT_SECRET is not set in the .env file")