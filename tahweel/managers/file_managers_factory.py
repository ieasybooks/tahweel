from pathlib import Path

from PIL import Image

from tahweel.managers import BaseFileManager
from tahweel.managers.image_file_manager import ImageFileManager
from tahweel.managers.pdf_file_manager import PdfFileManager


class FileManagersFactory:
  @classmethod
  def from_file_path(cls, file_path: Path, pdf2image_thread_count: int) -> BaseFileManager:
    if file_path.suffix == '.pdf':
      return PdfFileManager(file_path, pdf2image_thread_count)
    elif cls._is_valid_image(file_path):
      return ImageFileManager(file_path)
    else:
      raise ValueError(f'Unsupported file type: `{file_path.suffix}`.')

  @classmethod
  def _is_valid_image(cls, file_name: Path) -> bool:
    try:
      with Image.open(file_name) as image:
        image.verify()

      return True
    except Exception:
      return False
