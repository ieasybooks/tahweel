import google.auth

from tahweel.processors.google_drive_base_ocr_processor import GoogleDriveBaseOcrProcessor


class GoogleDriveOnColabOcrProcessor(GoogleDriveBaseOcrProcessor):
  def __init__(self):
    credentials, _ = google.auth.default(scopes=['https://www.googleapis.com/auth/drive'])

    super().__init__(credentials)
