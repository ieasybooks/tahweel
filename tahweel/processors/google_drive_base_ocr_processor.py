from io import BytesIO
from pathlib import Path

import httplib2

from google_auth_httplib2 import AuthorizedHttp
from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest, MediaFileUpload, MediaIoBaseDownload

from tahweel.decorators import retry
from tahweel.processors.base_ocr_processor import BaseOcrProcessor


class GoogleDriveBaseOcrProcessor(BaseOcrProcessor):
  def __init__(self, credentials):
    self._credentials = credentials

    self._drive_service = build(
      'drive',
      'v3',
      requestBuilder=self._build_request,
      http=AuthorizedHttp(self._credentials, http=httplib2.Http()),
    )  # type: ignore

  def process(self, file_path: Path) -> str:
    file_id = self._upload_file(file_path)
    download_buffer = self._download_file(file_id)
    self._delete_file(file_id)

    return download_buffer.getvalue().decode('utf-8')

  @retry()
  def _upload_file(self, file_path: Path) -> str:
    return str(
      self._drive_service.files()
      .create(
        body={'name': file_path.name, 'mimeType': 'application/vnd.google-apps.document'},
        media_body=MediaFileUpload(file_path, mimetype='image/jpeg'),
      )
      .execute()
      .get('id')
    )

  @retry()
  def _download_file(self, file_id: str) -> BytesIO:
    download_buffer = BytesIO()
    download = MediaIoBaseDownload(
      download_buffer,
      self._drive_service.files().export_media(fileId=file_id, mimeType='text/plain'),
    )

    downloaded = False
    while downloaded is False:
      _, downloaded = download.next_chunk()

    return download_buffer

  @retry()
  def _delete_file(self, file_id: str) -> None:
    self._drive_service.files().delete(fileId=file_id).execute()

  def _build_request(self, _http, *args, **kwargs) -> HttpRequest:
    return HttpRequest(AuthorizedHttp(self._credentials, http=httplib2.Http()), *args, **kwargs)
