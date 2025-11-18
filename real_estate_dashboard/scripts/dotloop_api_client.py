#!/usr/bin/env python3
"""
Dotloop API Client

A client for interacting with the Dotloop Public API v2.
Handles OAuth2 authentication, token refresh, and data fetching.

Prerequisites:
    1. Register your application at https://info.dotloop.com/developers
    2. Obtain client_id and client_secret
    3. Set environment variables or use .env file

Usage:
    python dotloop_api_client.py --authorize
    python dotloop_api_client.py --get-profiles
    python dotloop_api_client.py --get-loops

Documentation:
    https://dotloop.github.io/public-api/
"""

import os
import sys
import json
import time
import logging
import webbrowser
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.parse import urlencode, parse_qs, urlparse

import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

# Configuration
API_BASE_URL = "https://api-gateway.dotloop.com/public/v2"
AUTH_URL = "https://auth.dotloop.com/oauth/authorize"
TOKEN_URL = "https://auth.dotloop.com/oauth/token"

DEFAULT_STORAGE_PATH = Path(__file__).parent.parent / "storage" / "dotloop"
TOKEN_FILE = "dotloop_tokens.json"

# Default scopes
DEFAULT_SCOPES = [
    "profile:*",
    "loop:*",
    "contact:*",
    "template:*"
]


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """HTTP handler for OAuth callback."""

    def do_GET(self):
        """Handle OAuth callback GET request."""
        query = parse_qs(urlparse(self.path).query)

        if 'code' in query:
            self.server.auth_code = query['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
                <html>
                <body style="font-family: Arial; text-align: center; margin-top: 50px;">
                    <h1>Authorization Successful!</h1>
                    <p>You can close this window and return to the terminal.</p>
                </body>
                </html>
            """)
        else:
            error = query.get('error', ['Unknown error'])[0]
            self.server.auth_code = None
            self.server.error = error
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f"<html><body><h1>Error: {error}</h1></body></html>".encode())

    def log_message(self, format, *args):
        """Suppress HTTP log messages."""
        pass


class DotloopAPIClient:
    """Client for Dotloop Public API v2."""

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        redirect_uri: str = "http://localhost:8080/callback",
        storage_path: Optional[Path] = None
    ):
        """
        Initialize Dotloop API client.

        Args:
            client_id: OAuth client ID (or set DOTLOOP_CLIENT_ID env var)
            client_secret: OAuth client secret (or set DOTLOOP_CLIENT_SECRET env var)
            redirect_uri: OAuth redirect URI
            storage_path: Path to store tokens and data
        """
        self.client_id = client_id or os.getenv("DOTLOOP_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("DOTLOOP_CLIENT_SECRET")
        self.redirect_uri = redirect_uri
        self.storage_path = Path(storage_path) if storage_path else DEFAULT_STORAGE_PATH

        self.session = requests.Session()
        self._setup_logging()

        # Ensure storage directory exists
        self.storage_path.mkdir(parents=True, exist_ok=True)

        # Load existing tokens
        self.tokens = self._load_tokens()

        if not self.client_id or not self.client_secret:
            self.logger.warning(
                "Client ID and/or secret not configured. "
                "Set DOTLOOP_CLIENT_ID and DOTLOOP_CLIENT_SECRET environment variables."
            )

    def _setup_logging(self):
        """Configure logging."""
        log_file = self.storage_path / "dotloop.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _load_tokens(self) -> Dict[str, Any]:
        """Load tokens from storage."""
        token_path = self.storage_path / TOKEN_FILE

        if token_path.exists():
            with open(token_path, 'r') as f:
                tokens = json.load(f)
                self.logger.info("Loaded existing tokens from storage")
                return tokens

        return {}

    def _save_tokens(self, tokens: Dict[str, Any]):
        """Save tokens to storage."""
        self.tokens = tokens
        token_path = self.storage_path / TOKEN_FILE

        with open(token_path, 'w') as f:
            json.dump(tokens, f, indent=2)

        self.logger.info("Saved tokens to storage")

    def _is_token_expired(self) -> bool:
        """Check if access token is expired."""
        if not self.tokens:
            return True

        expires_at = self.tokens.get("expires_at")
        if not expires_at:
            return True

        # Add 5 minute buffer
        return datetime.now() > datetime.fromisoformat(expires_at) - timedelta(minutes=5)

    def authorize(self, scopes: Optional[List[str]] = None) -> bool:
        """
        Start OAuth2 authorization flow.

        Opens browser for user to authorize, then starts local server
        to receive the callback with authorization code.

        Args:
            scopes: List of OAuth scopes to request.

        Returns:
            True if authorization successful, False otherwise.
        """
        if not self.client_id:
            self.logger.error("Client ID not configured")
            return False

        scopes = scopes or DEFAULT_SCOPES
        scope_str = " ".join(scopes)

        # Build authorization URL
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": scope_str
        }

        auth_url = f"{AUTH_URL}?{urlencode(params)}"

        self.logger.info("Opening browser for authorization...")
        print(f"\nAuthorization URL: {auth_url}\n")

        # Open browser
        webbrowser.open(auth_url)

        # Start local server to receive callback
        parsed_uri = urlparse(self.redirect_uri)
        port = parsed_uri.port or 8080

        server = HTTPServer(('localhost', port), OAuthCallbackHandler)
        server.auth_code = None
        server.error = None

        print(f"Waiting for authorization callback on port {port}...")
        print("(Press Ctrl+C to cancel)\n")

        # Wait for callback
        server.handle_request()

        if server.auth_code:
            self.logger.info("Received authorization code")
            return self._exchange_code(server.auth_code)
        else:
            self.logger.error(f"Authorization failed: {server.error}")
            return False

    def _exchange_code(self, code: str) -> bool:
        """
        Exchange authorization code for access token.

        Args:
            code: Authorization code from OAuth callback.

        Returns:
            True if exchange successful, False otherwise.
        """
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        try:
            response = requests.post(TOKEN_URL, data=payload, timeout=30)

            if response.status_code == 200:
                tokens = response.json()

                # Calculate expiration time
                expires_in = tokens.get("expires_in", 43200)  # Default 12 hours
                expires_at = datetime.now() + timedelta(seconds=expires_in)
                tokens["expires_at"] = expires_at.isoformat()

                self._save_tokens(tokens)
                self.logger.info("Successfully obtained access token")
                return True
            else:
                self.logger.error(f"Token exchange failed: {response.status_code}")
                self.logger.error(response.text)
                return False

        except Exception as e:
            self.logger.error(f"Error exchanging code: {str(e)}")
            return False

    def refresh_token(self) -> bool:
        """
        Refresh the access token using refresh token.

        Returns:
            True if refresh successful, False otherwise.
        """
        if not self.tokens.get("refresh_token"):
            self.logger.error("No refresh token available")
            return False

        payload = {
            "grant_type": "refresh_token",
            "refresh_token": self.tokens["refresh_token"],
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        try:
            response = requests.post(TOKEN_URL, data=payload, timeout=30)

            if response.status_code == 200:
                tokens = response.json()

                # Calculate expiration time
                expires_in = tokens.get("expires_in", 43200)
                expires_at = datetime.now() + timedelta(seconds=expires_in)
                tokens["expires_at"] = expires_at.isoformat()

                self._save_tokens(tokens)
                self.logger.info("Successfully refreshed access token")
                return True
            else:
                self.logger.error(f"Token refresh failed: {response.status_code}")
                return False

        except Exception as e:
            self.logger.error(f"Error refreshing token: {str(e)}")
            return False

    def _ensure_valid_token(self) -> bool:
        """
        Ensure we have a valid access token.

        Refreshes token if expired.

        Returns:
            True if valid token available, False otherwise.
        """
        if not self.tokens.get("access_token"):
            self.logger.error("No access token. Please authorize first.")
            return False

        if self._is_token_expired():
            self.logger.info("Access token expired, refreshing...")
            if not self.refresh_token():
                self.logger.error("Failed to refresh token. Please re-authorize.")
                return False

        return True

    def _get_headers(self) -> Dict[str, str]:
        """Get API request headers with authorization."""
        return {
            "Authorization": f"Bearer {self.tokens.get('access_token', '')}",
            "Content-Type": "application/json"
        }

    def _api_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Make an API request with automatic token refresh.

        Args:
            method: HTTP method (GET, POST, PATCH, DELETE)
            endpoint: API endpoint path
            params: Query parameters
            data: Request body data

        Returns:
            API response data.
        """
        if not self._ensure_valid_token():
            return {"error": "Authentication required"}

        url = f"{API_BASE_URL}{endpoint}"
        headers = self._get_headers()

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=data,
                timeout=30
            )

            # Handle token expiration during request
            if response.status_code == 401:
                self.logger.info("Token expired during request, refreshing...")
                if self.refresh_token():
                    headers = self._get_headers()
                    response = self.session.request(
                        method=method,
                        url=url,
                        headers=headers,
                        params=params,
                        json=data,
                        timeout=30
                    )
                else:
                    return {"error": "Token refresh failed"}

            if response.status_code in [200, 201]:
                return response.json()
            else:
                return {
                    "error": f"API error: {response.status_code}",
                    "message": response.text
                }

        except Exception as e:
            self.logger.error(f"API request error: {str(e)}")
            return {"error": str(e)}

    # Profile endpoints
    def get_account(self) -> Dict[str, Any]:
        """Get current user account information."""
        return self._api_request("GET", "/account")

    def get_profiles(self) -> Dict[str, Any]:
        """Get all profiles for current user."""
        return self._api_request("GET", "/profile")

    def get_profile(self, profile_id: int) -> Dict[str, Any]:
        """Get specific profile by ID."""
        return self._api_request("GET", f"/profile/{profile_id}")

    # Loop endpoints
    def get_loops(self, profile_id: int, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Get loops for a profile.

        Args:
            profile_id: Profile ID
            params: Query parameters (filter, sort, etc.)
        """
        return self._api_request("GET", f"/profile/{profile_id}/loop", params=params)

    def get_loop(self, profile_id: int, loop_id: int) -> Dict[str, Any]:
        """Get specific loop by ID."""
        return self._api_request("GET", f"/profile/{profile_id}/loop/{loop_id}")

    def create_loop(self, profile_id: int, loop_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new loop."""
        return self._api_request("POST", f"/profile/{profile_id}/loop", data=loop_data)

    def update_loop(self, profile_id: int, loop_id: int, loop_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing loop."""
        return self._api_request("PATCH", f"/profile/{profile_id}/loop/{loop_id}", data=loop_data)

    # Loop details
    def get_loop_details(self, profile_id: int, loop_id: int) -> Dict[str, Any]:
        """Get loop details including all metadata."""
        return self._api_request("GET", f"/profile/{profile_id}/loop/{loop_id}/detail")

    def get_loop_participants(self, profile_id: int, loop_id: int) -> Dict[str, Any]:
        """Get participants in a loop."""
        return self._api_request("GET", f"/profile/{profile_id}/loop/{loop_id}/participant")

    def get_loop_folders(self, profile_id: int, loop_id: int) -> Dict[str, Any]:
        """Get folders in a loop."""
        return self._api_request("GET", f"/profile/{profile_id}/loop/{loop_id}/folder")

    def get_loop_tasks(self, profile_id: int, loop_id: int) -> Dict[str, Any]:
        """Get tasks in a loop."""
        return self._api_request("GET", f"/profile/{profile_id}/loop/{loop_id}/tasklist")

    def get_loop_activities(self, profile_id: int, loop_id: int) -> Dict[str, Any]:
        """Get activity history for a loop."""
        return self._api_request("GET", f"/profile/{profile_id}/loop/{loop_id}/activity")

    # Document endpoints
    def get_documents(self, profile_id: int, loop_id: int, folder_id: int) -> Dict[str, Any]:
        """Get documents in a folder."""
        return self._api_request(
            "GET",
            f"/profile/{profile_id}/loop/{loop_id}/folder/{folder_id}/document"
        )

    # Contact endpoints
    def get_contacts(self, profile_id: int, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get contacts for a profile."""
        return self._api_request("GET", f"/profile/{profile_id}/contact", params=params)

    def get_contact(self, profile_id: int, contact_id: int) -> Dict[str, Any]:
        """Get specific contact by ID."""
        return self._api_request("GET", f"/profile/{profile_id}/contact/{contact_id}")

    # Template endpoints
    def get_templates(self, profile_id: int) -> Dict[str, Any]:
        """Get loop templates for a profile."""
        return self._api_request("GET", f"/profile/{profile_id}/loop-template")

    # Utility methods
    def save_data(self, data: Dict[str, Any], filename: str) -> str:
        """Save data to storage."""
        file_path = self.storage_path / filename

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

        self.logger.info(f"Saved data to {file_path}")
        return str(file_path)

    def fetch_all_data(self) -> Dict[str, Any]:
        """
        Fetch all available data and save to storage.

        Returns:
            Dictionary with all fetched data.
        """
        all_data = {
            "timestamp": datetime.now().isoformat(),
            "account": None,
            "profiles": [],
            "loops": {},
            "contacts": {}
        }

        # Get account info
        account = self.get_account()
        all_data["account"] = account

        # Get profiles
        profiles_response = self.get_profiles()
        profiles = profiles_response.get("data", [])
        all_data["profiles"] = profiles

        # For each profile, get loops and contacts
        for profile in profiles:
            profile_id = profile.get("profile_id")
            if profile_id:
                # Get loops
                loops = self.get_loops(profile_id)
                all_data["loops"][profile_id] = loops

                # Get contacts
                contacts = self.get_contacts(profile_id)
                all_data["contacts"][profile_id] = contacts

        # Save all data
        filename = f"dotloop_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.save_data(all_data, filename)

        return all_data


def print_setup_instructions():
    """Print setup instructions for new users."""
    print("\n" + "="*60)
    print("DOTLOOP API SETUP INSTRUCTIONS")
    print("="*60)
    print("""
1. Register your application:
   Go to https://info.dotloop.com/developers
   Fill out the registration form to get credentials

2. Set environment variables:
   export DOTLOOP_CLIENT_ID="your_client_id"
   export DOTLOOP_CLIENT_SECRET="your_client_secret"

   Or create a .env file with these values

3. Run authorization:
   python dotloop_api_client.py --authorize

4. Fetch data:
   python dotloop_api_client.py --get-profiles
   python dotloop_api_client.py --get-loops --profile-id <id>
   python dotloop_api_client.py --fetch-all

Token Management:
- Access tokens expire after 12 hours
- Tokens are automatically refreshed when needed
- Tokens are stored in storage/dotloop/dotloop_tokens.json
""")
    print("="*60 + "\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Dotloop API Client")
    parser.add_argument(
        "--storage",
        type=str,
        help="Storage directory path",
        default=str(DEFAULT_STORAGE_PATH)
    )
    parser.add_argument(
        "--client-id",
        type=str,
        help="OAuth client ID",
        default=os.getenv("DOTLOOP_CLIENT_ID")
    )
    parser.add_argument(
        "--client-secret",
        type=str,
        help="OAuth client secret",
        default=os.getenv("DOTLOOP_CLIENT_SECRET")
    )

    # Commands
    parser.add_argument("--setup", action="store_true", help="Show setup instructions")
    parser.add_argument("--authorize", action="store_true", help="Start OAuth authorization flow")
    parser.add_argument("--refresh", action="store_true", help="Refresh access token")
    parser.add_argument("--get-account", action="store_true", help="Get account information")
    parser.add_argument("--get-profiles", action="store_true", help="Get all profiles")
    parser.add_argument("--get-loops", action="store_true", help="Get loops for profile")
    parser.add_argument("--get-contacts", action="store_true", help="Get contacts for profile")
    parser.add_argument("--fetch-all", action="store_true", help="Fetch all data")

    # Parameters
    parser.add_argument("--profile-id", type=int, help="Profile ID for queries")
    parser.add_argument("--loop-id", type=int, help="Loop ID for queries")

    args = parser.parse_args()

    if args.setup:
        print_setup_instructions()
        sys.exit(0)

    # Initialize client
    client = DotloopAPIClient(
        client_id=args.client_id,
        client_secret=args.client_secret,
        storage_path=Path(args.storage)
    )

    # Execute commands
    if args.authorize:
        success = client.authorize()
        if success:
            print("\nAuthorization successful! You can now use the API.")
        else:
            print("\nAuthorization failed. Please check your credentials.")

    elif args.refresh:
        success = client.refresh_token()
        if success:
            print("\nToken refreshed successfully!")
        else:
            print("\nToken refresh failed. Please re-authorize.")

    elif args.get_account:
        result = client.get_account()
        print(json.dumps(result, indent=2))

    elif args.get_profiles:
        result = client.get_profiles()
        print(json.dumps(result, indent=2))

    elif args.get_loops:
        if not args.profile_id:
            print("Error: --profile-id required for --get-loops")
            sys.exit(1)
        result = client.get_loops(args.profile_id)
        print(json.dumps(result, indent=2))

    elif args.get_contacts:
        if not args.profile_id:
            print("Error: --profile-id required for --get-contacts")
            sys.exit(1)
        result = client.get_contacts(args.profile_id)
        print(json.dumps(result, indent=2))

    elif args.fetch_all:
        result = client.fetch_all_data()
        print(f"\nFetched all data. Saved to storage.")
        print(f"Profiles: {len(result.get('profiles', []))}")
        print(f"Loops: {sum(len(v.get('data', [])) for v in result.get('loops', {}).values())}")

    else:
        print_setup_instructions()
