"""
File Validation Utilities

This module provides utilities for validating uploaded files including size limits,
file type validation, and filename sanitization.
"""

import os
import magic
from typing import List, Optional
from fastapi import UploadFile, HTTPException, status
from app.settings import settings


# Allowed file extensions and MIME types
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
ALLOWED_DOCUMENT_EXTENSIONS = {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".txt"}
ALLOWED_PDF_EXTENSIONS = {".pdf"}

ALLOWED_IMAGE_MIMES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
ALLOWED_DOCUMENT_MIMES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "text/plain",
}
ALLOWED_PDF_MIMES = {"application/pdf"}


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal attacks.

    Removes any directory paths and special characters.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename safe for file system

    Example:
        >>> sanitize_filename("../../etc/passwd")
        'etc_passwd'
        >>> sanitize_filename("my file (1).pdf")
        'my_file_1.pdf'
    """
    # Get just the filename (no directory paths)
    safe_name = os.path.basename(filename)

    # Define allowed characters (alphanumeric, underscore, hyphen, dot)
    safe_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-")

    # Replace unsafe characters with underscore
    sanitized = ''.join(c if c in safe_chars else '_' for c in safe_name)

    # Remove leading/trailing dots and underscores
    sanitized = sanitized.strip('._')

    # If filename is empty after sanitization, use a default
    if not sanitized:
        sanitized = "unnamed_file"

    return sanitized


async def validate_file_size(
    file: UploadFile,
    max_size_mb: Optional[int] = None
) -> None:
    """
    Validate that uploaded file size doesn't exceed limit.

    Args:
        file: FastAPI UploadFile object
        max_size_mb: Maximum file size in megabytes (default from settings)

    Raises:
        HTTPException: If file size exceeds limit

    Example:
        >>> await validate_file_size(file, max_size_mb=10)
    """
    if max_size_mb is None:
        max_size_mb = settings.MAX_UPLOAD_SIZE_MB

    max_size_bytes = max_size_mb * 1024 * 1024

    # Read file content to check size
    contents = await file.read()
    file_size = len(contents)

    # Reset file position for subsequent reads
    await file.seek(0)

    if file_size > max_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size ({file_size / 1024 / 1024:.2f} MB) exceeds maximum allowed size ({max_size_mb} MB)"
        )


def validate_file_extension(
    filename: str,
    allowed_extensions: List[str]
) -> None:
    """
    Validate file extension against allowed list.

    Args:
        filename: File name to validate
        allowed_extensions: List of allowed extensions (e.g., [".pdf", ".docx"])

    Raises:
        HTTPException: If file extension not allowed

    Example:
        >>> validate_file_extension("document.pdf", [".pdf", ".docx"])
    """
    file_ext = os.path.splitext(filename)[1].lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File extension '{file_ext}' not allowed. Allowed extensions: {', '.join(allowed_extensions)}"
        )


async def validate_file_mime_type(
    file: UploadFile,
    allowed_mimes: List[str]
) -> None:
    """
    Validate file MIME type using python-magic (reads file content).

    This prevents users from just renaming files to bypass extension checks.

    Args:
        file: FastAPI UploadFile object
        allowed_mimes: List of allowed MIME types

    Raises:
        HTTPException: If MIME type not allowed

    Example:
        >>> await validate_file_mime_type(file, ["application/pdf"])
    """
    # Read file content
    contents = await file.read()

    # Reset file position
    await file.seek(0)

    # Detect MIME type from content
    mime = magic.from_buffer(contents, mime=True)

    if mime not in allowed_mimes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type '{mime}' not allowed. Allowed types: {', '.join(allowed_mimes)}"
        )


async def validate_image_file(
    file: UploadFile,
    max_size_mb: int = 10
) -> str:
    """
    Comprehensive validation for image uploads.

    Args:
        file: FastAPI UploadFile object
        max_size_mb: Maximum file size in MB

    Returns:
        Sanitized filename

    Raises:
        HTTPException: If validation fails

    Example:
        >>> safe_filename = await validate_image_file(file, max_size_mb=5)
    """
    # Validate file size
    await validate_file_size(file, max_size_mb)

    # Validate extension
    validate_file_extension(file.filename, list(ALLOWED_IMAGE_EXTENSIONS))

    # Validate MIME type
    await validate_file_mime_type(file, list(ALLOWED_IMAGE_MIMES))

    # Sanitize filename
    safe_filename = sanitize_filename(file.filename)

    return safe_filename


async def validate_pdf_file(
    file: UploadFile,
    max_size_mb: int = 50
) -> str:
    """
    Comprehensive validation for PDF uploads.

    Args:
        file: FastAPI UploadFile object
        max_size_mb: Maximum file size in MB

    Returns:
        Sanitized filename

    Raises:
        HTTPException: If validation fails

    Example:
        >>> safe_filename = await validate_pdf_file(file, max_size_mb=50)
    """
    # Validate file size
    await validate_file_size(file, max_size_mb)

    # Validate extension
    validate_file_extension(file.filename, list(ALLOWED_PDF_EXTENSIONS))

    # Validate MIME type
    await validate_file_mime_type(file, list(ALLOWED_PDF_MIMES))

    # Sanitize filename
    safe_filename = sanitize_filename(file.filename)

    return safe_filename


async def validate_document_file(
    file: UploadFile,
    max_size_mb: int = 50
) -> str:
    """
    Comprehensive validation for document uploads.

    Args:
        file: FastAPI UploadFile object
        max_size_mb: Maximum file size in MB

    Returns:
        Sanitized filename

    Raises:
        HTTPException: If validation fails

    Example:
        >>> safe_filename = await validate_document_file(file, max_size_mb=50)
    """
    # Validate file size
    await validate_file_size(file, max_size_mb)

    # Validate extension
    validate_file_extension(file.filename, list(ALLOWED_DOCUMENT_EXTENSIONS))

    # Validate MIME type
    await validate_file_mime_type(file, list(ALLOWED_DOCUMENT_MIMES))

    # Sanitize filename
    safe_filename = sanitize_filename(file.filename)

    return safe_filename


# Export all utilities
__all__ = [
    'sanitize_filename',
    'validate_file_size',
    'validate_file_extension',
    'validate_file_mime_type',
    'validate_image_file',
    'validate_pdf_file',
    'validate_document_file',
    'ALLOWED_IMAGE_EXTENSIONS',
    'ALLOWED_DOCUMENT_EXTENSIONS',
    'ALLOWED_PDF_EXTENSIONS',
]
