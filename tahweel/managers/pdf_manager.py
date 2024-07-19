import subprocess

from pathlib import Path

import pdf2image
import platformdirs


MAX_FILE_SIZE_IN_BYTES = 4900000
MAX_FILE_SIZE_IN_KILO_BYTES = 4900


class PdfManager:
  def __init__(self, file_path: Path, pdf2image_thread_count: int = 8):
    self.file_path = file_path
    self.pdf2image_thread_count = pdf2image_thread_count
    self.images_paths: list[Path] = []

  def pages_count(self) -> int:
    return pdf2image.pdfinfo_from_path(self.file_path)['Pages']

  def to_images(self) -> None:
    self.images_paths = list(map(lambda path: Path(path), pdf2image.convert_from_path(
      self.file_path,
      output_folder=platformdirs.user_cache_dir('Tahweel'),
      fmt='jpeg',
      jpegopt={'quality': 100, 'progressive': True, 'optimize': True},
      thread_count=self.pdf2image_thread_count,
      paths_only=True,
    )))

    for path in self.images_paths:
      if path.stat().st_size > MAX_FILE_SIZE_IN_BYTES:
        subprocess.run(
          # https://www.fmwconcepts.com/imagemagick/downsize/index.php.
          ['./tahweel/downsize.sh', '-s', str(MAX_FILE_SIZE_IN_KILO_BYTES), str(path), str(path)],
          stdout=subprocess.DEVNULL,
        )

  def __del__(self) -> None:
    for path in self.images_paths:
      path.unlink(missing_ok=True)
