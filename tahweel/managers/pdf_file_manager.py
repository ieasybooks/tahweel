from pathlib import Path

import pdf2image
import platformdirs

from tahweel.enums import DirOutputType, TahweelType
from tahweel.utils.image_utils import compress_image


TXT_DIR_SUFFIX = ' - Tahweel TXT'
DOCX_DIR_SUFFIX = ' - Tahweel DOCX'


class PdfFileManager:
  def __init__(self, file_path: Path, pdf2image_thread_count: int = 8):
    self.file_path = file_path
    self.pdf2image_thread_count = pdf2image_thread_count
    self.images_paths: list[Path] = []

  def pages_count(self) -> int:
    return pdf2image.pdfinfo_from_path(self.file_path)['Pages']

  def to_images(self) -> None:
    self.images_paths = list(
      map(
        lambda path: Path(path),
        pdf2image.convert_from_path(
          self.file_path,
          output_folder=platformdirs.user_cache_dir('Tahweel'),
          fmt='jpeg',
          jpegopt={'quality': 100, 'progressive': True, 'optimize': True},
          thread_count=self.pdf2image_thread_count,
          paths_only=True,
        ),
      )
    )

    for path in self.images_paths:
      compress_image(path)

  def output_exists(
    self,
    tahweel_type: TahweelType,
    dir_output_type: DirOutputType | None = None,
    dir: Path | None = None,
  ) -> bool:
    return (
      self.txt_file_path(tahweel_type, dir_output_type, dir).exists()
      and self.docx_file_path(tahweel_type, dir_output_type, dir).exists()
    )

  def txt_file_path(
    self,
    tahweel_type: TahweelType,
    dir_output_type: DirOutputType | None = None,
    dir: Path | None = None,
  ) -> Path:
    return self._output_file_path('.txt', tahweel_type, dir_output_type, dir)

  def docx_file_path(
    self,
    tahweel_type: TahweelType,
    dir_output_type: DirOutputType | None = None,
    dir: Path | None = None,
  ) -> Path:
    return self._output_file_path('.docx', tahweel_type, dir_output_type, dir)

  def _output_file_path(
    self,
    suffix: str,
    tahweel_type: TahweelType,
    dir_output_type: DirOutputType | None = None,
    dir: Path | None = None,
  ) -> Path:
    match tahweel_type:
      case TahweelType.FILE:
        return self.file_path.with_suffix(suffix)
      case TahweelType.DIR:
        if dir_output_type == DirOutputType.SIDE_BY_SIDE:
          return self.file_path.with_suffix(suffix)

        if dir is None:
          raise ValueError(
            '`dir` is required when `tahweel_type` is `TahweelType.DIR` and `dir_output_type` is `DirOutputType.TREE_TO_TREE`'
          )

        match suffix:
          case '.txt':
            dir_name_suffix = TXT_DIR_SUFFIX
          case '.docx':
            dir_name_suffix = DOCX_DIR_SUFFIX

        return dir.parent / (dir.name + dir_name_suffix) / self.file_path.with_suffix(suffix).relative_to(dir)

  def __del__(self) -> None:
    for path in self.images_paths:
      path.unlink(missing_ok=True)
