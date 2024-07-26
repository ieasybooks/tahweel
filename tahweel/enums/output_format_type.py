from enum import Enum


class OutputFormatType(Enum):
  TXT = 'txt'
  DOCX = 'docx'

  def __str__(self):
    return self.value
