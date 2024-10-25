from pathlib import Path

import platformdirs

from PIL import Image

from tahweel.managers import BaseFileManager
from tahweel.utils.image_utils import compress_image


class ImageFileManager(BaseFileManager):
  def __init__(self, file_path: Path):
    super().__init__(file_path)

  def pages_count(self) -> int:
    return 1

  def to_images(self) -> None:
    user_cache_dir = Path(platformdirs.user_cache_dir('Tahweel', ensure_exists=True))

    self.images_paths.append((user_cache_dir / self.file_path.name).with_suffix('.jpg'))

    with Image.open(self.file_path) as image:
      image.convert('RGB').save(self.images_paths[0])

    for path in self.images_paths:
      compress_image(path)
