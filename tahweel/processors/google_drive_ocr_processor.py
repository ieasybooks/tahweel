from io import BytesIO
from pathlib import Path

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload


class GoogleDriveOcrProcessor:
  def __init__(self, service_account_credentials: Path):
    self._drive_service = build(
      'drive',
      'v3',
      credentials=Credentials.from_service_account_file(service_account_credentials),
      cache_discovery=False,
    )

  def process(self, file_path: Path, retries: int = 5) -> str:
    download_buffer = None

    while download_buffer is None and retries > 0:
      file_id = self._upload_file(file_path)
      download_buffer = self._download_file(file_id)
      self._delete_file(file_id)
      retries -= 1

    if download_buffer is None:
      return ''

    return download_buffer.getvalue().decode('utf-8')

  def _upload_file(self, file_path: Path) -> str:
    return self._drive_service.files().create(
      body={'name': file_path.name, 'mimeType': 'application/vnd.google-apps.document'},
      media_body=MediaFileUpload(file_path, mimetype='image/jpeg'),
    ).execute().get('id')

  def _download_file(self, file_id: str) -> BytesIO | None:
    download_buffer = BytesIO()
    download = MediaIoBaseDownload(
      download_buffer,
      self._drive_service.files().export_media(fileId=file_id, mimeType='text/plain'),
    )

    downloaded, status = False, False
    while downloaded is False:
      status, downloaded = download.next_chunk()

    if status:
      return download_buffer

    return None

  def _delete_file(self, file_id: str) -> None:
    self._drive_service.files().delete(fileId=file_id).execute()
