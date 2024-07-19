from pathlib import Path

import platformdirs

from tahweel import TahweelArgumentParser
from tahweel.enums import TahweelType
from tahweel.managers import PdfManager
from tahweel.processors import GoogleDriveOcrProcessor


def main() -> None:
  args = TahweelArgumentParser(underscores_to_dashes=True).parse_args()

  prepare_package_dirs()

  processor = GoogleDriveOcrProcessor(args.service_account_credentials)

  if args.tahweel_type == TahweelType.FILE:
    pdf_manager = PdfManager(args.file_or_dir_path, args.pdf2image_thread_count)
    pdf_manager.to_images()

    for image_path in pdf_manager.images_paths:
      print(processor.process(image_path))


def prepare_package_dirs() -> None:
  Path(platformdirs.user_cache_dir('Tahweel')).mkdir(parents=True, exist_ok=True)
