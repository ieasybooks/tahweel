from pathlib import Path

import pdf2image
import platformdirs

from tahweel.managers import BaseFileManager
from tahweel.utils.image_utils import compress_image


class PdfFileManager(BaseFileManager):
  def __init__(self, file_path: Path, pdf2image_thread_count: int = 8):
    super().__init__(file_path)

    self.pdf2image_thread_count = pdf2image_thread_count

  def pages_count(self) -> int:
    return pdf2image.pdfinfo_from_path(self.file_path)['Pages']

  def to_images(self) -> None:
    self.images_paths.extend(
      map(
        lambda path: Path(path),
        pdf2image.convert_from_path(
          self.file_path,
          output_folder=platformdirs.user_cache_dir('Tahweel', ensure_exists=True),
          fmt='jpeg',
          jpegopt={'quality': 100, 'progressive': True, 'optimize': True},
          thread_count=self.pdf2image_thread_count,
          paths_only=True,
        ),
      )
    )

    for path in self.images_paths:
      compress_image(path)
