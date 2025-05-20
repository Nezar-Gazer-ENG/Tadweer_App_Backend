import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

def get_config(key: str, default: str = None) -> str:
    """
    Retrieve a configuration value from environment variables.
    If not found, return the provided default value.
    """
    return os.getenv(key, default)

def load_database_config() -> dict:
    """
    Load the database configuration from environment variables.
    Returns a dictionary with database connection details.
    """
    return {
        "DB_HOST": get_config("DB_HOST", "localhost"),
        "DB_PORT": get_config("DB_PORT", "3306"),
        "DB_USER": get_config("DB_USER", "root"),
        "DB_PASSWORD": get_config("DB_PASSWORD", "password"),
        "DB_NAME": get_config("DB_NAME", "tire_app"),
    }

def load_google_maps_config() -> str:
    """
    Load the Google Maps API key.
    """
    return get_config("GOOGLE_MAPS_API_KEY")

def load_logging_config() -> dict:
    """
    Load the logging configuration from environment variables.
    Returns a dictionary with log file path and log level.
    """
    return {
        "LOG_DIRECTORY": get_config("LOG_DIRECTORY", "./logs"),
        "LOG_LEVEL": get_config("LOG_LEVEL", "INFO"),
    }

def load_jwt_config() -> dict:
    """
    Load JWT configuration details.
    """
    secret_key = get_config("SECRET_KEY", "mysecretkey")
    print(f"Loaded JWT Secret Key: {secret_key}")  # Debugging line
    return {
        "SECRET_KEY": secret_key,
        "ACCESS_TOKEN_EXPIRE_MINUTES": int(get_config("ACCESS_TOKEN_EXPIRE_MINUTES", "60")),
        "REFRESH_TOKEN_EXPIRE_DAYS": int(get_config("REFRESH_TOKEN_EXPIRE_DAYS", "7")),
    }


def load_notification_config() -> dict:
    """
    Load notification-related configuration.
    """
    return {
        "PUSHER_APP_ID": get_config("PUSHER_APP_ID"),
        "PUSHER_KEY": get_config("PUSHER_KEY"),
        "PUSHER_SECRET": get_config("PUSHER_SECRET"),
        "PUSHER_CLUSTER": get_config("PUSHER_CLUSTER"),
    }
