import importlib.metadata

from pathlib import Path

from tap import Tap

from tahweel.enums import DirOutputType, TahweelType


class TahweelArgumentParser(Tap):
  file_or_dir_path: Path

  service_account_credentials: Path
  """Path to the service account credentials JSON file."""

  pdf2image_thread_count: int = 8
  """Number of threads to use for PDF to image conversion using `pdf2image` package."""

  processor_max_workers: int = 8
  """Number of threads to use while performing OCR on PDF pages."""

  dir_output_type: DirOutputType = DirOutputType.TREE_TO_TREE

  txt_page_separator: str = 'PAGE_SEPARATOR'
  """Separator to use between pages in the output TXT file."""

  docx_remove_newlines: bool = False
  """Remove newlines from the output DOCX file. Useful if you want DOCX and PDF to have the same page count."""

  skip_output_check: bool = False
  """Use this flag in development only to skip the output check."""

  tahweel_type: TahweelType = TahweelType.FILE

  def configure(self):
    self.add_argument('file_or_dir_path', type=Path, help='Path to the file or directory to be processed.')

    self.add_argument(
      '--dir-output-type',
      type=DirOutputType,
      default=DirOutputType.TREE_TO_TREE,
      choices=list(DirOutputType),
      help='Use this argument when processing a directory. '
      '`tree_to_tree` means the output will be in a new directory beside the input directory with the same structure, '
      'while `side_by_side` means the output will be in the same input directory beside each file.',
    )

    self.add_argument(
      '--tahweel-type',
      type=TahweelType,
      default=TahweelType.FILE,
      choices=list(TahweelType),
      help="Don't use this argument, it will be auto-set based on `file_or_dir_path`.",
    )

    self.add_argument(
      '--version',
      action='version',
      version=importlib.metadata.version('tahweel'),
      help="show program's version number and exit",
    )

  def process_args(self):
    self.tahweel_type = TahweelType.FILE if self.file_or_dir_path.is_file() else TahweelType.DIR
