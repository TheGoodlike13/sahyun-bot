"""
Contains general utilities that can be used in many contexts.
May also contain utilities that are too few to create a separate module for.
"""
import logging
from abc import ABC
from typing import TypeVar
from urllib.parse import urlparse, parse_qs

from cachetools import TTLCache

T = TypeVar('T')  # general purpose generic variable to be used in generic functions
V = TypeVar('V')  # generic variable for dict like situations, e.g. Dict[T, V]

NON_EXISTENT = object()  # if next(it, NON_EXISTENT) is NON_EXISTENT: <do stuff if 'it' was empty>


def identity(o: T) -> T:
    return o


# noinspection PyUnusedLocal
def always_true(o: T) -> bool:
    return True


# noinspection PyUnusedLocal
def always_false(o: T) -> bool:
    return False


def debug_ex(e: Exception,
             trying_to: str = 'do something (check traceback)',
             log: logging.Logger = None,
             silent: bool = False):
    log = log or logging.root
    if silent:
        log.debug('Error while trying to %s: %s: %s', trying_to, type(e).__name__, e, exc_info=True)
    else:
        log.error('Error while trying to %s: %s: %s', trying_to, type(e).__name__, e)
        log.debug('Traceback:', exc_info=True)


def clean_link(link: str) -> str:
    try:
        url_parts = urlparse(link or '')
        if 'youtube.com' in url_parts.netloc:
            video_id = parse_qs(url_parts.query).get('v', None)
            if video_id:
                return f'https://youtu.be/{video_id[0]}'
        elif url_parts.scheme == 'http':
            return link[:4] + 's' + link[4:]
    except ValueError:
        pass

    return link or ''


def choose(key: str, **kwargs):
    """
    :returns value associated with key in kwargs, None if no such value
    """
    return kwargs.get(key, None)


class Closeable(ABC):
    """
    To avoid making errors in the method signatures, just extend this class for objects that can be used as context.
    """
    def __enter__(self):
        pass

    def __exit__(self, *args):
        self.close()

    def close(self):
        pass


class NonelessCache(TTLCache):
    """
    TTLCache which does not store None values and returns None if a value is missing
    """
    def __setitem__(self, key, value, **kwargs):
        if value is not None:
            super().__setitem__(key, value, **kwargs)

    def __missing__(self, key):
        return None
