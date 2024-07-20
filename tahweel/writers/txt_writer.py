from pathlib import Path


class TxtWriter:
  def __init__(self, file_path: Path):
    self.file_path = file_path

    self.file_path.parent.mkdir(parents=True, exist_ok=True)

  def write(self, texts: list[str], page_separator: str) -> None:
    self.file_path.write_text(f'\n{page_separator}\n'.join(texts))
