"""
Google Drive Integration - File Storage
Store and manage documents in Google Drive

Note: Free Google Drive API (15GB free storage)
Documentation: https://developers.google.com/drive
"""

from typing import Dict, Any, Optional, List
import httpx
from ..base import BaseIntegration, IntegrationConfig, IntegrationMetadata, IntegrationResponse


class GoogleDriveIntegration(BaseIntegration):
    """
    Integration with Google Drive API for file storage

    Note: Requires OAuth2 credentials from Google Cloud Console
    Free tier: 15GB storage
    """

    BASE_URL = "https://www.googleapis.com/drive/v3"
    UPLOAD_URL = "https://www.googleapis.com/upload/drive/v3"

    def __init__(self, config: IntegrationConfig):
        config.is_free = True  # 15GB free
        config.requires_api_key = True  # OAuth2 access token
        super().__init__(config)

    def get_metadata(self) -> IntegrationMetadata:
        return IntegrationMetadata(
            name="Google Drive",
            category="tools",
            description="Store and manage property documents and financial reports",
            is_free=True,
            requires_api_key=True,
            documentation_url="https://developers.google.com/drive",
            features=[
                "Document storage",
                "File sharing",
                "Folder organization",
                "Version history",
                "15GB free storage",
                "Collaborative editing"
            ]
        )

    async def test_connection(self) -> IntegrationResponse:
        """Test Google Drive API connection"""
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="Google Drive integration not configured. Set GOOGLE_DRIVE_ACCESS_TOKEN."
            )

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/about",
                    params={"fields": "user,storageQuota"},
                    headers={"Authorization": f"Bearer {self.config.api_key}"},
                    timeout=10.0
                )
                response.raise_for_status()

                data = response.json()

                return self._success_response({
                    "message": "Successfully connected to Google Drive API",
                    "user": data.get("user", {}).get("emailAddress"),
                    "storage": data.get("storageQuota")
                })

        except Exception as e:
            return self._handle_error(e, "Google Drive connection test")

    async def list_files(
        self,
        folder_id: Optional[str] = None,
        page_size: int = 100,
        query: Optional[str] = None
    ) -> IntegrationResponse:
        """
        List files in Google Drive

        Args:
            folder_id: Optional folder ID to list files from
            page_size: Number of files to return
            query: Search query
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="Google Drive integration not configured"
            )

        try:
            params = {
                "pageSize": page_size,
                "fields": "files(id, name, mimeType, createdTime, modifiedTime, size, webViewLink)"
            }

            # Build query
            q_parts = []
            if folder_id:
                q_parts.append(f"'{folder_id}' in parents")
            if query:
                q_parts.append(query)

            if q_parts:
                params["q"] = " and ".join(q_parts)

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/files",
                    params=params,
                    headers={"Authorization": f"Bearer {self.config.api_key}"},
                    timeout=30.0
                )
                response.raise_for_status()

                data = response.json()

                return self._success_response({
                    "files": data.get("files", []),
                    "count": len(data.get("files", []))
                })

        except Exception as e:
            return self._handle_error(e, "list_files")

    async def create_folder(
        self,
        name: str,
        parent_folder_id: Optional[str] = None
    ) -> IntegrationResponse:
        """
        Create a folder in Google Drive

        Args:
            name: Folder name
            parent_folder_id: Optional parent folder ID
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="Google Drive integration not configured"
            )

        try:
            metadata = {
                "name": name,
                "mimeType": "application/vnd.google-apps.folder"
            }

            if parent_folder_id:
                metadata["parents"] = [parent_folder_id]

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.BASE_URL}/files",
                    json=metadata,
                    headers={"Authorization": f"Bearer {self.config.api_key}"},
                    timeout=10.0
                )
                response.raise_for_status()

                data = response.json()

                return self._success_response({
                    "folder": data
                })

        except Exception as e:
            return self._handle_error(e, "create_folder")

    async def upload_file(
        self,
        file_path: str,
        file_name: str,
        mime_type: str,
        folder_id: Optional[str] = None
    ) -> IntegrationResponse:
        """
        Upload a file to Google Drive

        Args:
            file_path: Local file path
            file_name: Name for the file in Drive
            mime_type: MIME type of the file
            folder_id: Optional folder ID to upload to
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="Google Drive integration not configured"
            )

        try:
            import os
            from pathlib import Path

            if not os.path.exists(file_path):
                return IntegrationResponse(
                    success=False,
                    error=f"File not found: {file_path}"
                )

            metadata = {
                "name": file_name,
                "mimeType": mime_type
            }

            if folder_id:
                metadata["parents"] = [folder_id]

            # Read file content
            with open(file_path, "rb") as f:
                file_content = f.read()

            async with httpx.AsyncClient() as client:
                # Create multipart upload
                import json
                from io import BytesIO

                # First request: Create file metadata
                response = await client.post(
                    f"{self.UPLOAD_URL}/files?uploadType=multipart",
                    files={
                        "metadata": (None, json.dumps(metadata), "application/json"),
                        "file": (file_name, file_content, mime_type)
                    },
                    headers={"Authorization": f"Bearer {self.config.api_key}"},
                    timeout=60.0
                )
                response.raise_for_status()

                data = response.json()

                return self._success_response({
                    "file": data,
                    "uploaded": True
                })

        except Exception as e:
            return self._handle_error(e, "upload_file")

    async def get_file_metadata(self, file_id: str) -> IntegrationResponse:
        """
        Get file metadata

        Args:
            file_id: Google Drive file ID
        """
        if not self.is_available:
            return IntegrationResponse(
                success=False,
                error="Google Drive integration not configured"
            )

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/files/{file_id}",
                    params={"fields": "*"},
                    headers={"Authorization": f"Bearer {self.config.api_key}"},
                    timeout=10.0
                )
                response.raise_for_status()

                data = response.json()

                return self._success_response({
                    "file": data
                })

        except Exception as e:
            return self._handle_error(e, "get_file_metadata")
