from dataclasses import dataclass
from typing import Callable

from tahweel.enums import TransformationType


@dataclass
class Transformation:
  transformation_type: TransformationType
  source: str | Callable
  target: str | None = None
