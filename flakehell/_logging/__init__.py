from logging.config import dictConfig

from ._config import LOGGING


__all__ = ['LOGGING', 'configure_logging']


def configure_logging(level: str = 'INFO') -> None:
    LOGGING['loggers']['flakehell']['level'] = level
    dictConfig(LOGGING)
