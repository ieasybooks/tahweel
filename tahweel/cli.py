import logging
import os

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import platformdirs

from tqdm import tqdm

from tahweel import TahweelArgumentParser
from tahweel.enums import TahweelType, TransformationType
from tahweel.enums.output_format_type import OutputFormatType
from tahweel.managers import FileManagersFactory
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

  processors: list[BaseOcrProcessor] = []
  if IS_COLAB:
    processors = [GoogleDriveOnColabOcrProcessor()]
  else:
    processors = [GoogleDriveOcrProcessor(credentials) for credentials in args.service_account_credentials]

  prepare_package_dirs(args.output_dir)
  files_to_process = get_files_to_process(args.files_or_dirs_paths, args.file_extensions)

  with ThreadPoolExecutor(max_workers=len(processors)) as executor:
    futures = []

    for index, file_to_process in enumerate(files_to_process):
      processor = processors[index % len(processors)]
      file_path, dir_path, tahweel_type = file_to_process

      futures.append(
        executor.submit(
          process_file,
          args,
          processor,
          dir_path,
          file_path,
          tahweel_type,
        ),
      )
    for future in tqdm(futures, desc='Processing files'):
      try:
        future.result()
      except Exception as e:
        logging.error(f'Error processing file: {e}', exc_info=True)


def prepare_package_dirs(output_dir: Path | None = None) -> None:
  if output_dir is not None:
    output_dir.mkdir(parents=True, exist_ok=True)

  Path(platformdirs.user_cache_dir('Tahweel')).mkdir(parents=True, exist_ok=True)


def get_files_to_process(
  files_or_dirs_paths: list[Path],
  file_extensions: list[str] | None = None,
) -> list[tuple[Path, Path, TahweelType]]:
  if file_extensions:
    supported_extensions = file_extensions
  else:
    supported_extensions = supported_image_formats() + ['.pdf']

  files_to_process = []

  for file_or_dir_path in files_or_dirs_paths:
    if file_or_dir_path.is_file():
      files_to_process.append((file_or_dir_path, file_or_dir_path.parent, TahweelType.FILE))
    else:
      files_to_process.extend(
        [
          (path, file_or_dir_path, TahweelType.DIR)
          for extension in supported_extensions
          for path in file_or_dir_path.rglob(f'*{extension}')
        ]
      )

  return files_to_process


def process_file(
  args: TahweelArgumentParser,
  processor: BaseOcrProcessor,
  dir_path: Path,
  file_path: Path,
  tahweel_type: TahweelType,
) -> None:
  try:
    file_manager = FileManagersFactory.from_file_path(file_path, args.pdf2image_thread_count)

    if not args.skip_output_check and file_manager.output_exists(
      tahweel_type,
      dir_path,
      args.dir_output_type,
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
      TxtWriter(file_manager.txt_file_path(tahweel_type, dir_path, args.dir_output_type, args.output_dir)).write(
        content,
        args.txt_page_separator,
      )

    if OutputFormatType.DOCX in args.output_formats:
      DocxWriter(file_manager.docx_file_path(tahweel_type, dir_path, args.dir_output_type, args.output_dir)).write(
        content,
        args.docx_remove_newlines,
      )
  except Exception as e:
    logging.error(f'Failed to process "{file_manager.file_path}" due to {e}, continuing...', exc_info=True)
