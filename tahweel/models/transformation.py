from dataclasses import dataclass
from typing import Callable, Optional

from tahweel.enums import TransformationType


@dataclass
class Transformation:
  transformation_type: TransformationType
  source: str | Callable
  target: Optional[str] = None
