from abc import ABC, abstractmethod
from pathlib import Path


class BaseOcrProcessor(ABC):
  @abstractmethod
  def process(self, file_path: Path) -> str:
    pass
