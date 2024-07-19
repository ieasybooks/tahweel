from enum import Enum


class TahweelType(Enum):
  FILE = 'file'
  DIR = 'dir'

  def __str__(self):
    return self.value
