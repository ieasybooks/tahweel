from pathlib import Path


PAGE_SEPARATOR = 'PAGE_SEPARATOR'


class TxtWriter:
  def __init__(self, file_path: Path):
    self.file_path = file_path

    self.file_path.parent.mkdir(parents=True, exist_ok=True)

  def write(self, texts: list[str]):
    self.file_path.write_text(f'\n{PAGE_SEPARATOR}\n'.join(texts))
