import re

from typing import Callable, cast

from tahweel.enums import TransformationType
from tahweel.models import Transformation


def truncate(text: str, length: int, from_end: bool = False) -> str:
  if len(text) <= length:
    return text

  if from_end:
    return f'...{text[-length:]}'
  else:
    return f'...{text[:length]}'


def apply_transformations(text: str, transformations: list[Transformation]) -> str:
  for transformation in transformations:
    match transformation.transformation_type:
      case TransformationType.REGEX:
        text = re.sub(cast(str, transformation.source), cast(str, transformation.target), text)
      case TransformationType.REPLACE:
        text = text.replace(cast(str, transformation.source), cast(str, transformation.target))
      case TransformationType.FUNCTION:
        text = cast(Callable, transformation.source)(text)

  return text
