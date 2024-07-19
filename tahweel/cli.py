from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import platformdirs

from tahweel import TahweelArgumentParser
from tahweel.enums import TahweelType
from tahweel.managers import PdfFileManager
from tahweel.processors import GoogleDriveOcrProcessor
from tahweel.writers import DocxWriter, TxtWriter


def main() -> None:
  args = TahweelArgumentParser(underscores_to_dashes=True).parse_args()
  processor = GoogleDriveOcrProcessor(args.service_account_credentials)

  prepare_package_dirs()

  match args.tahweel_type:
    case TahweelType.FILE:
      pdf_file_manager = PdfFileManager(args.file_or_dir_path, args.pdf2image_thread_count)

      process_file(args, processor, pdf_file_manager)
    case TahweelType.DIR:
      for pdf_file_path in args.file_or_dir_path.rglob('*.pdf'):
        pdf_file_manager = PdfFileManager(pdf_file_path, args.pdf2image_thread_count)

        process_file(args, processor, pdf_file_manager)


def prepare_package_dirs() -> None:
  Path(platformdirs.user_cache_dir('Tahweel')).mkdir(parents=True, exist_ok=True)


def process_file(args: TahweelArgumentParser, processor: GoogleDriveOcrProcessor, file_manager: PdfFileManager) -> None:
  if (not args.skip_output_check and
          file_manager.output_exists(args.tahweel_type, args.dir_output_type, args.file_or_dir_path)):
    return

  file_manager.to_images()

  with ThreadPoolExecutor(max_workers=args.processor_max_workers) as executor:
    content = list(executor.map(processor.process, file_manager.images_paths))

  content = list(map(lambda text: text.replace('﻿________________', ''), content))
  content = list(map(lambda text: text.replace('﻿', ''), content))
  content = list(map(str.strip, content))

  TxtWriter(file_manager.txt_file_path(args.tahweel_type, args.dir_output_type, args.file_or_dir_path)).write(content)
  DocxWriter(file_manager.docx_file_path(args.tahweel_type, args.dir_output_type, args.file_or_dir_path)).write(content)
