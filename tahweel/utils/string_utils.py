def truncate(text: str, length: int, from_end: bool = False) -> str:
  if len(text) <= length:
    return text

  if from_end:
    return f'...{text[-length:]}'
  else:
    return f'...{text[:length]}'
