import importlib.metadata as importlib_metadata


try:
    __version__ = importlib_metadata.version('django-cruditor')
except Exception:
    __version__ = 'HEAD'
