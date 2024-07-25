import functools
import random
import time

from typing import Callable

from googleapiclient.errors import HttpError


RETRY_ERRORS = {
  403: [
    'Usage limit exceeded',
    'Daily limit exceeded',
    'Number of items in folder',
    'User rate limit exceeded',
    'Rate limit exceeded',
    'Sharing rate limit exceeded',
    'The user has not granted the app access to the file',
    'The user does not have sufficient permissions for the file',
    "App cannot be used within the authenticated user's domain",
  ],
  404: ['File not found'],
  429: ['Too many requests'],
  500: ['Backend error'],
  502: ['Bad Gateway'],
  503: ['Service Unavailable'],
  504: ['Gateway Timeout'],
}


def retry(retries: int = 10, delay: int = 1, backoff: int = 2) -> Callable:
  def validate_params():
    if retries < 0:
      raise ValueError('`retries` must be greater than or equal to 0.')

    if delay <= 0:
      raise ValueError('`delay` must be greater than 0.')

    if backoff <= 1:
      raise ValueError('`backoff` must be greater than 1.')

  def should_retry(error: HttpError, remaining_retries: int) -> bool:
    return error.resp.status in RETRY_ERRORS and remaining_retries > 0

  def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      validate_params()

      _delay = delay

      for remaining_retries in range(retries, -1, -1):
        try:
          return func(*args, **kwargs)
        except HttpError as error:
          if should_retry(error, remaining_retries):
            time.sleep(_delay + random.random())
            _delay *= backoff
          else:
            raise

    return wrapper

  return decorator
