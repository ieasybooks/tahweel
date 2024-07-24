from pathlib import Path

from PIL import Image


def compress_image(image_path: Path, max_size_mb: int = 5, initial_quality: int = 85) -> bool:
  file_size = image_path.stat().st_size / (1024 * 1024)

  if file_size <= max_size_mb:
    return True

  with Image.open(image_path) as img:
    while file_size > max_size_mb and initial_quality > 10:
      img.save(image_path, optimize=True, quality=initial_quality)
      file_size = image_path.stat().st_size / (1024 * 1024)
      initial_quality -= 5

  if file_size <= max_size_mb:
    return True
  else:
    return False
