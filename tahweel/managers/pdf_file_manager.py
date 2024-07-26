from pathlib import Path
from typing import cast

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
    output_dir: Path | None = None,
  ) -> bool:
    return (
      self.txt_file_path(tahweel_type, dir_output_type, dir, output_dir).exists()
      and self.docx_file_path(tahweel_type, dir_output_type, dir, output_dir).exists()
    )

  def txt_file_path(
    self,
    tahweel_type: TahweelType,
    dir_output_type: DirOutputType | None = None,
    dir: Path | None = None,
    output_dir: Path | None = None,
  ) -> Path:
    return self._output_file_path('.txt', tahweel_type, dir_output_type, dir, output_dir)

  def docx_file_path(
    self,
    tahweel_type: TahweelType,
    dir_output_type: DirOutputType | None = None,
    dir: Path | None = None,
    output_dir: Path | None = None,
  ) -> Path:
    return self._output_file_path('.docx', tahweel_type, dir_output_type, dir, output_dir)

  def _output_file_path(
    self,
    suffix: str,
    tahweel_type: TahweelType,
    dir_output_type: DirOutputType | None = None,
    dir: Path | None = None,
    output_dir: Path | None = None,
  ) -> Path:
    match tahweel_type:
      case TahweelType.FILE:
        return self._file_output_path(suffix, output_dir)
      case TahweelType.DIR:
        return self._dir_output_path(suffix, cast(DirOutputType, dir_output_type), cast(Path, dir), output_dir)

  def _file_output_path(self, suffix: str, output_dir: Path | None) -> Path:
    if output_dir is not None:
      return output_dir / self.file_path.with_suffix(suffix).name

    return self.file_path.with_suffix(suffix)

  def _dir_output_path(self, suffix: str, dir_output_type: DirOutputType, dir: Path, output_dir: Path | None) -> Path:
    match dir_output_type:
      case DirOutputType.SIDE_BY_SIDE:
        return self._side_by_side_output_path(suffix, dir, output_dir)
      case DirOutputType.TREE_TO_TREE:
        return self._tree_to_tree_output_path(suffix, dir, output_dir)

  def _side_by_side_output_path(self, suffix: str, dir: Path, output_dir: Path | None) -> Path:
    if output_dir is not None:
      return output_dir / self.file_path.with_suffix(suffix).relative_to(dir)

    return self.file_path.with_suffix(suffix)

  def _tree_to_tree_output_path(self, suffix: str, dir: Path, output_dir: Path | None) -> Path:
    dir_name_suffix = self._get_dir_name_suffix(suffix)

    if output_dir is not None:
      return output_dir / dir_name_suffix[3:] / self.file_path.with_suffix(suffix).relative_to(dir)

    return dir.parent / (dir.name + dir_name_suffix) / self.file_path.with_suffix(suffix).relative_to(dir)

  def _get_dir_name_suffix(self, suffix: str) -> str:
    match suffix:
      case '.txt':
        return TXT_DIR_SUFFIX
      case '.docx':
        return DOCX_DIR_SUFFIX
      case _:
        raise ValueError(f'Unsupported suffix: `{suffix}`.')

  def __del__(self) -> None:
    for path in self.images_paths:
      path.unlink(missing_ok=True)
