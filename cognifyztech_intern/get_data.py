import os
import sys
import logging
from typing import Any, Dict, List, Union
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from requests.exceptions import SSLError

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Define scopes
SCOPES: List[str] = ['https://www.googleapis.com/auth/drive.readonly']

# Specify the path to the credentials file
CREDS_FILE: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'credential.json')

def authenticate() -> Credentials:
    """
    Authenticate user with Google Drive API using OAuth 2.0.

    Returns:
        Credentials: Authenticated credentials object.
    """
    creds: Union[None, Credentials] = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_drive_service() -> Any:
    """
    Build and return Google Drive API service.

    Returns:
        googleapiclient.discovery.Resource: Google Drive API service object.
    """
    creds: Credentials = authenticate()
    service: Any = build('drive', 'v3', credentials=creds)
    return service

def download_file(file_id: str, destination: str) -> None:
    """
    Download a file from Google Drive.

    Args:
        file_id (str): ID of the file to download.
        destination (str): Path where the downloaded file will be saved.

    Examples:
        >>> download_file('abc123', 'downloads/example_file.txt')
        Download 100%.
    """
    service: Any = get_drive_service()
    request: Any = service.files().get_media(fileId=file_id)
    fh: Any = open(destination, 'wb')
    downloader: Any = MediaIoBaseDownload(fh, request)
    done: bool = False
    while done is False:
        try:
            status, done = downloader.next_chunk()
            logging.debug("Download %d%%." % int(status.progress() * 100))
        except SSLError as e:
            logging.error("SSL Error occured: %s", e)
            raise
    fh.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        file_id = "1eS-q31uXdtdpSOg15g7SZ65rZjBM7gBO"  # Default file ID
    else:
        file_id = sys.argv[1]

    if len(sys.argv) < 3:
        destination = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'raw')  # Default destination path
    else:
        destination = sys.argv[2]

    download_file(file_id, destination)