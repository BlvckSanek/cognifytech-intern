import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Define credentials file path
CREDENTIALS_FILE = 'credentials.json'

def download_file(file_id: str, destination: str) -> None:
    """
    Download a file from Google Drive using service account credentials.

    Args:
        file_id (str): ID of the file to download.
        destination (str): Path where the downloaded file will be saved.
    """
    # Authenticate with service account credentials
    creds = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE)
    service = build('drive', 'v3', credentials=creds)

    # Download the file
    request = service.files().get_media(fileId=file_id)
    with open(destination, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

if __name__ == '__main__':
    # Default file ID and destination path
    default_file_id = "1eS-q31uXdtdpSOg15g7SZ65rZjBM7gBO"
    default_destination = "data/raw/Dataset.csv"

    # Use default values if no command-line arguments are provided
    file_id = default_file_id
    destination = default_destination

    # Download the file
    download_file(file_id, destination)
