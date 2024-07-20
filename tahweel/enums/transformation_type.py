from enum import Enum


class TransformationType(Enum):
  REGEX = 'regex'
  REPLACE = 'replace'
  FUNCTION = 'function'

  def __str__(self):
    return self.value
