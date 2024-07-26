import logging
import os

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import platformdirs

from tqdm import tqdm

from tahweel import TahweelArgumentParser
from tahweel.enums import TahweelType, TransformationType
from tahweel.enums.output_format_type import OutputFormatType
from tahweel.managers import PdfFileManager
from tahweel.models import Transformation
from tahweel.processors import BaseOcrProcessor, GoogleDriveOcrProcessor, GoogleDriveOnColabOcrProcessor
from tahweel.utils.string_utils import apply_transformations, truncate
from tahweel.writers import DocxWriter, TxtWriter


IS_COLAB = 'COLAB_RELEASE_TAG' in os.environ

TRANSFORMATIONS = [
  Transformation(TransformationType.REPLACE, '\ufeff________________', ''),
  Transformation(TransformationType.REPLACE, '\ufeff', ''),
  Transformation(TransformationType.FUNCTION, str.strip),
]


def main() -> None:
  args = TahweelArgumentParser(underscores_to_dashes=True).parse_args()

  processor: BaseOcrProcessor
  if IS_COLAB:
    processor = GoogleDriveOnColabOcrProcessor()
  else:
    processor = GoogleDriveOcrProcessor(args.service_account_credentials)

  prepare_package_dirs(args)

  for file_or_dir_path in tqdm(args.files_or_dirs_paths, desc='Paths'):
    process_path(args, processor, file_or_dir_path)


def prepare_package_dirs(args: TahweelArgumentParser) -> None:
  if args.output_dir is not None:
    args.output_dir.mkdir(parents=True, exist_ok=True)

  Path(platformdirs.user_cache_dir('Tahweel')).mkdir(parents=True, exist_ok=True)


def process_path(args: TahweelArgumentParser, processor: BaseOcrProcessor, file_or_dir_path: Path) -> None:
  if file_or_dir_path.is_file():
    process_single_file(args, processor, file_or_dir_path)
  else:
    process_directory(args, processor, file_or_dir_path)


def process_single_file(args: TahweelArgumentParser, processor: BaseOcrProcessor, file_path: Path) -> None:
  try:
    process_file(args, processor, PdfFileManager(file_path, args.pdf2image_thread_count), file_path, TahweelType.FILE)
  except Exception as e:
    logging.error(f'Failed to process "{file_path}" due to {e}, continuing...', exc_info=True)


def process_directory(args: TahweelArgumentParser, processor: BaseOcrProcessor, dir_path: Path) -> None:
  pdf_file_paths = list(dir_path.rglob('*.pdf'))

  for pdf_file_path in tqdm(pdf_file_paths, desc=f'Files ({truncate(str(dir_path), 50, from_end=True)})'):
    try:
      pdf_file_manager = PdfFileManager(pdf_file_path, args.pdf2image_thread_count)

      process_file(args, processor, pdf_file_manager, dir_path, TahweelType.DIR)
    except Exception as e:
      logging.error(f'Failed to process "{pdf_file_path}" due to {e}, continuing...', exc_info=True)


def process_file(
  args: TahweelArgumentParser,
  processor: BaseOcrProcessor,
  file_manager: PdfFileManager,
  file_or_dir_path: Path,
  tahweel_type: TahweelType,
) -> None:
  if not args.skip_output_check and file_manager.output_exists(
    tahweel_type,
    args.dir_output_type,
    file_or_dir_path,
    args.output_dir,
  ):
    return

  file_manager.to_images()

  with ThreadPoolExecutor(max_workers=args.processor_max_workers) as executor:
    content = list(
      tqdm(
        executor.map(processor.process, file_manager.images_paths),
        total=file_manager.pages_count(),
        desc=f'Pages ({truncate(str(file_manager.file_path), 50, from_end=True)})',
      ),
    )

  content = list(map(lambda text: apply_transformations(text, TRANSFORMATIONS), content))

  if OutputFormatType.TXT in args.output_formats:
    TxtWriter(file_manager.txt_file_path(tahweel_type, args.dir_output_type, file_or_dir_path, args.output_dir)).write(
      content,
      args.txt_page_separator,
    )

  if OutputFormatType.DOCX in args.output_formats:
    DocxWriter(
      file_manager.docx_file_path(tahweel_type, args.dir_output_type, file_or_dir_path, args.output_dir)
    ).write(
      content,
      args.docx_remove_newlines,
    )
