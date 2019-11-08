"""Flake8 wrapper to make it nice and configurable
"""

from ._cli import entrypoint, flake8_entrypoint


__version__ = '0.3.1'
__all__ = ['entrypoint', 'flake8_entrypoint']
