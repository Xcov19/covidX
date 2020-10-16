import enum
import logging


class EnumChoice(enum.Enum):
    """Generic Enum class to fill choices in model fields."""

    def __init__(self, *args, **kwargs):
        super().__init__()

    @classmethod
    def choices(cls):
        return [(field.name, field.value) for field in cls]


def createLogger(path: str) -> logging.Logger:
    # create logger
    LOGGER = logging.Logger("Logger", logging.DEBUG)
    # create log format
    log_fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # create log file handler
    file_handler = logging.FileHandler(path, delay=False)
    file_handler.setFormatter(log_fmt)
    # create log file streamer
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(log_fmt)

    LOGGER.addHandler(file_handler)
    LOGGER.addHandler(stream_handler)
    return LOGGER
