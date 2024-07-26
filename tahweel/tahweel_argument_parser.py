import importlib.metadata

from pathlib import Path

from tap import Tap

from tahweel.enums import DirOutputType, OutputFormatType


class TahweelArgumentParser(Tap):
  files_or_dirs_paths: list[Path]

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

  output_formats: list[OutputFormatType] = [OutputFormatType.TXT, OutputFormatType.DOCX]

  output_dir: Path | None = None
  """Path to the output directory. This overrides the default output directory behavior."""

  skip_output_check: bool = False
  """Use this flag in development only to skip the output check."""

  def configure(self):
    self.add_argument('files_or_dirs_paths', nargs='+', help='Path to the file or directory to be processed.')

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
      '--output-formats',
      nargs='+',
      type=OutputFormatType,
      default=[OutputFormatType.TXT, OutputFormatType.DOCX],
      choices=list(OutputFormatType),
      help='Format of the output files; if not specified, `txt` and `docx` formats will be produced.',
    )

    self.add_argument(
      '--version',
      action='version',
      version=importlib.metadata.version('tahweel'),
      help="show program's version number and exit",
    )
