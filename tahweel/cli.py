import os

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import platformdirs

from tqdm import tqdm

from tahweel import TahweelArgumentParser
from tahweel.enums import TahweelType, TransformationType
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

  prepare_package_dirs()

  match args.tahweel_type:
    case TahweelType.FILE:
      pdf_file_paths = [args.file_or_dir_path]
    case TahweelType.DIR:
      pdf_file_paths = list(args.file_or_dir_path.rglob('*.pdf'))

  for pdf_file_path in tqdm(pdf_file_paths, desc='Files'):
    pdf_file_manager = PdfFileManager(pdf_file_path, args.pdf2image_thread_count)

    try:
      process_file(args, processor, pdf_file_manager)
    except Exception:
      print(f'Failed to process "{pdf_file_manager.file_path}", continuing...')
      continue


def prepare_package_dirs() -> None:
  Path(platformdirs.user_cache_dir('Tahweel')).mkdir(parents=True, exist_ok=True)


def process_file(args: TahweelArgumentParser, processor: BaseOcrProcessor, file_manager: PdfFileManager) -> None:
  if not args.skip_output_check and file_manager.output_exists(
    args.tahweel_type, args.dir_output_type, args.file_or_dir_path
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

  TxtWriter(file_manager.txt_file_path(args.tahweel_type, args.dir_output_type, args.file_or_dir_path)).write(
    content,
    args.txt_page_separator,
  )

  DocxWriter(file_manager.docx_file_path(args.tahweel_type, args.dir_output_type, args.file_or_dir_path)).write(
    content,
    args.docx_remove_newlines,
  )
