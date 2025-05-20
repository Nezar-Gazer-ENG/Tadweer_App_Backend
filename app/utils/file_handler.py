import os
import shutil
from fastapi import UploadFile
from app.utils.config_loader import get_config
from datetime import datetime

# Get file storage path from configuration
UPLOAD_DIRECTORY = get_config("UPLOAD_DIRECTORY", "./uploads")

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

from fastapi.responses import FileResponse

def save_file(file_path: str) -> FileResponse:
    """
    Return a file response for downloading.
    """
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='application/pdf', filename=os.path.basename(file_path))
    else:
        raise FileNotFoundError(f"File not found: {file_path}")



def save_uploaded_file(file: UploadFile, subdir: str = "") -> str:
    """
    Save an uploaded file to the specified subdirectory.
    Returns the file path where the file is saved.
    """
    try:
        # Create subdirectory if specified
        directory = os.path.join(UPLOAD_DIRECTORY, subdir)
        os.makedirs(directory, exist_ok=True)

        # Construct unique file name with timestamp
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(directory, filename)

        # Save the file to the specified location
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return file_path
    except Exception as e:
        raise RuntimeError(f"Error saving file: {str(e)}")

def delete_file(file_path: str) -> bool:
    """
    Delete a file from the system.
    Returns True if successful, False otherwise.
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        raise RuntimeError(f"Error deleting file: {str(e)}")

def move_file(src: str, dest: str) -> bool:
    """
    Move a file from source to destination.
    Returns True if successful, False otherwise.
    """
    try:
        if os.path.exists(src):
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.move(src, dest)
            return True
        return False
    except Exception as e:
        raise RuntimeError(f"Error moving file: {str(e)}")

def list_files(directory: str = UPLOAD_DIRECTORY) -> list:
    """
    List all files in the given directory.
    Returns a list of file paths.
    """
    try:
        files = []
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                files.append(os.path.join(root, filename))
        return files
    except Exception as e:
        raise RuntimeError(f"Error listing files: {str(e)}")
