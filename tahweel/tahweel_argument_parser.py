import importlib.metadata

from pathlib import Path

from tap import Tap

from tahweel.enums import TahweelType


class TahweelArgumentParser(Tap):
  file_or_dir_path: Path
  """Path to the file or directory to be processed."""

  service_account_credentials: Path
  """Path to the service account credentials JSON file."""

  pdf2image_thread_count: int = 8
  """Number of threads to use for PDF to image conversion using `pdf2image` package."""

  processor_max_workers: int = 8
  """Number of threads to use while performing OCR on PDF pages."""

  skip_output_check: bool = False
  """Use this flag in development only to skip the output check."""

  tahweel_type: TahweelType = TahweelType.FILE
  """Don't use this argument, it will be auto-set based on `file_or_dir_path`."""

  def configure(self):
    self.add_argument('file_or_dir_path', type=Path, help='Path to the file or directory to be processed.')

    self.add_argument(
      '--version',
      action='version',
      version=importlib.metadata.version('tahweel'),
      help="show program's version number and exit",
    )

  def process_args(self):
    self.tahweel_type = TahweelType.FILE if self.file_or_dir_path.is_file() else TahweelType.DIR
