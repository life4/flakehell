"""Flake8 wrapper to make it nice and configurable
"""

from ._cli import entrypoint, flake8_entrypoint


__version__ = '0.2.0'
__all__ = ['entrypoint', 'flake8_entrypoint']
