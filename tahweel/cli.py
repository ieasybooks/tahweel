import logging
import os

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List, Optional, Tuple, Union

import platformdirs

from tqdm import tqdm

from tahweel import TahweelArgumentParser
from tahweel.enums import TahweelType, TransformationType
from tahweel.enums.output_format_type import OutputFormatType
from tahweel.managers import BaseFileManager, FileManagersFactory
from tahweel.models import Transformation
from tahweel.processors import BaseOcrProcessor, GoogleDriveOcrProcessor, GoogleDriveOnColabOcrProcessor
from tahweel.utils.image_utils import supported_image_formats
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

  processors: List[BaseOcrProcessor] = []
  if IS_COLAB:
    processors = [GoogleDriveOnColabOcrProcessor()]
  else:
    processors = [GoogleDriveOcrProcessor(cred) for cred in args.service_account_credentials]

  prepare_package_dirs(args)
  files_to_process = get_files_to_process(args)

  with ThreadPoolExecutor(max_workers=len(processors)) as executor:
    futures = []

    for index, file_to_process in enumerate(files_to_process):
      processor = processors[index % len(processors)]

      if len(file_to_process) == 2:
        dir_path = None
        file_path, tahweel_type = file_to_process
      else:
        file_path, dir_path, tahweel_type = file_to_process

      futures.append(executor.submit(process_file_with_processor, args, processor, file_path, tahweel_type, dir_path))

    for future in tqdm(futures, desc='Processing files'):
      try:
        future.result()
      except Exception as e:
        logging.error(f'Error processing file: {e}', exc_info=True)


def prepare_package_dirs(args: TahweelArgumentParser) -> None:
  if args.output_dir is not None:
    args.output_dir.mkdir(parents=True, exist_ok=True)

  Path(platformdirs.user_cache_dir('Tahweel')).mkdir(parents=True, exist_ok=True)


def get_files_to_process(
  args: TahweelArgumentParser,
) -> List[Union[Tuple[Path, TahweelType], Tuple[Path, Path, TahweelType]]]:
  supported_extensions = supported_image_formats() + ['.pdf']

  files_to_process: List[Union[Tuple[Path, TahweelType], Tuple[Path, Path, TahweelType]]] = []

  for file_or_dir_path in args.files_or_dirs_paths:
    if file_or_dir_path.is_file():
      files_to_process.append((file_or_dir_path, TahweelType.FILE))
    else:
      files_to_process.extend(
        [
          (path, file_or_dir_path, TahweelType.DIR)
          for extension in supported_extensions
          for path in file_or_dir_path.rglob(f'*{extension}')
        ]
      )

  return files_to_process


def process_file_with_processor(
  args: TahweelArgumentParser,
  processor: BaseOcrProcessor,
  file_path: Path,
  tahweel_type: TahweelType,
  dir_path: Optional[Path] = None,
) -> None:
  """Process a single file with the given processor."""
  try:
    reference_path = dir_path if dir_path is not None else file_path
    process_file(
      args,
      processor,
      FileManagersFactory.from_file_path(file_path, args.pdf2image_thread_count),
      reference_path,
      tahweel_type,
    )
  except Exception as e:
    logging.error(f'Failed to process "{file_path}" due to {e}, continuing...', exc_info=True)


def process_file(
  args: TahweelArgumentParser,
  processor: BaseOcrProcessor,
  file_manager: BaseFileManager,
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
