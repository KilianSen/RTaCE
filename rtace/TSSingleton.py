import threading
import weakref
import logging


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Singleton:
    _instances = weakref.WeakValueDictionary()
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        try:
            if cls not in cls._instances:
                with cls._lock:
                    if cls not in cls._instances:
                        logger.info(f"Creating a new instance of {cls.__name__}")
                        cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            else:
                logger.info(f"Fetching existing instance of {cls.__name__}")

            return cls._instances[cls]
        except Exception as e:
            logger.error(f"Exception occurred while creating/fetching an instance of {cls.__name__}: {e.args}")
            raise

    def __del__(self):
        try:
            logger.debug(f"Deleting instance of {self.__class__.__name__}")
        except Exception as e:
            logger.error(f"Exception occurred while deleting an instance of {self.__class__.__name__}: {e.args}")
            raise
