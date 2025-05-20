from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import JWTError, jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from app.models.user import User
from app.utils.config_loader import load_jwt_config

# Load JWT configuration
jwt_config = load_jwt_config()
SECRET_KEY = jwt_config.get("SECRET_KEY", "mysecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = jwt_config.get("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
REFRESH_TOKEN_EXPIRE_DAYS = jwt_config.get("REFRESH_TOKEN_EXPIRE_DAYS", 7)

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_access_token(data: dict) -> str:
    """Generate a new access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Debugging to ensure the key is correctly loaded
    print(f"Using SECRET_KEY: {SECRET_KEY}")

    # Validate that the secret key is a non-empty string
    if not isinstance(SECRET_KEY, str) or not SECRET_KEY:
        raise ValueError(f"SECRET_KEY must be a non-empty string, got {type(SECRET_KEY)}")

    # Encode the JWT
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        print(f"Error encoding JWT: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Token generation failed")


def create_refresh_token(data: dict) -> str:
    """Generate a new refresh token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})

    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        print(f"Error encoding refresh token: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Refresh token generation failed")


def verify_token(token: str) -> Dict:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        print(f"Token verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Extract and validate the current user from the token."""
    try:
        payload = verify_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise ValueError("Username not found in token")
        return User(username=username)
    except Exception as e:
        print(f"Error extracting current user: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def refresh_access_token(refresh_token: str) -> str:
    """Generate a new access token from a valid refresh token."""
    try:
        payload = verify_token(refresh_token)
        username: str = payload.get("sub")
        if username is None:
            raise ValueError("Username not found in refresh token")
        new_access_token = create_access_token(data={"sub": username})
        return new_access_token
    except Exception as e:
        print(f"Error refreshing access token: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
