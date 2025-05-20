import uuid
from datetime import datetime
from passlib.context import CryptContext
import hashlib

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_uuid() -> str:
    """
    Generate a unique UUID string.
    """
    return str(uuid.uuid4())

def current_timestamp() -> str:
    """
    Return the current timestamp in ISO format.
    """
    return datetime.utcnow().isoformat()

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)

def generate_checksum(data: str) -> str:
    """
    Generate an MD5 checksum of the given data.
    """
    return hashlib.md5(data.encode('utf-8')).hexdigest()

def generate_filename(prefix: str, extension: str) -> str:
    """
    Generate a unique filename using a prefix and file extension.
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"

def is_valid_uuid(value: str) -> bool:
    """
    Check if a given value is a valid UUID.
    """
    try:
        uuid_obj = uuid.UUID(value, version=4)
        return str(uuid_obj) == value
    except ValueError:
        return False

def dict_to_camel_case(data: dict) -> dict:
    """
    Convert dictionary keys from snake_case to camelCase.
    """
    def camel_case(s):
        parts = s.split('_')
        return parts[0] + ''.join(word.capitalize() for word in parts[1:])
    
    return {camel_case(key): value for key, value in data.items()}
