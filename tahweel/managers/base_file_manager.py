from abc import ABC, abstractmethod
from pathlib import Path
from typing import cast

from tahweel.enums import DirOutputType, TahweelType


TXT_DIR_SUFFIX = ' - Tahweel TXT'
DOCX_DIR_SUFFIX = ' - Tahweel DOCX'


class BaseFileManager(ABC):
  def __init__(self, file_path: Path):
    self.file_path = file_path
    self.images_paths: list[Path] = []

  @abstractmethod
  def pages_count(self) -> int:
    pass

  @abstractmethod
  def to_images(self) -> None:
    pass

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
