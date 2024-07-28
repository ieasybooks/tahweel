import shutil

from pathlib import Path

import platformdirs

from tahweel.managers import BaseFileManager
from tahweel.utils.image_utils import compress_image


class ImageFileManager(BaseFileManager):
  def __init__(self, file_path: Path):
    super().__init__(file_path)

  def pages_count(self) -> int:
    return 1

  def to_images(self) -> None:
    self.images_paths.append(Path(platformdirs.user_cache_dir('Tahweel')) / self.file_path.name)

    shutil.copy(self.file_path, self.images_paths[0])

    for path in self.images_paths:
      compress_image(path)