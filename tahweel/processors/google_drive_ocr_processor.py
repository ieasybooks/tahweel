from pathlib import Path

from google.oauth2.service_account import Credentials

from tahweel.processors.google_drive_base_ocr_processor import GoogleDriveBaseOcrProcessor


class GoogleDriveOcrProcessor(GoogleDriveBaseOcrProcessor):
  def __init__(self, service_account_credentials: Path):
    credentials = Credentials.from_service_account_file(
      service_account_credentials,
      scopes=['https://www.googleapis.com/auth/drive'],
    )

    super().__init__(credentials)
